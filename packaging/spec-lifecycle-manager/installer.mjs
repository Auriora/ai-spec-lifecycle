// Copyright 2026 Auriora
//
// SPDX-License-Identifier: GPL-3.0-or-later

"use strict";

// Spec 028: cross-platform Node port of
// scripts/install-spec-lifecycle-manager-package.sh. It copies the plugin tree,
// registers the local marketplace, and (optionally) runs `codex plugin add`,
// using only node built-ins so it runs on Windows, macOS, and Linux without a
// POSIX shell.
//
// Phase 2 layering: this module reproduces the .sh steps faithfully (T004); the
// interpreter-pinning of installed .mcp.json/hooks.json is added on top (T002/
// T003) in pinInstalledConfigs().

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { resolvePython } from "./resolve-python.mjs";

const REQUIRED_PATHS = [
  "plugins/spec-lifecycle-manager/.codex-plugin/plugin.json",
  "plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/SKILL.md",
  "plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_runtime.py",
  "plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/spec_mcp_server.py",
  "plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py",
  "plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/traceability_lookup.py",
  "plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/prompts",
  "plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/references",
  "plugins/spec-lifecycle-manager/.mcp.json",
  "plugins/spec-lifecycle-manager/hooks/hooks.json",
  "packaging/spec-lifecycle-manager/package-manifest.json",
];

const EXECUTABLE_SCRIPTS = [
  "skills/spec-lifecycle-manager/scripts/spec_runtime.py",
  "skills/spec-lifecycle-manager/scripts/spec_mcp_server.py",
  "skills/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py",
  "skills/spec-lifecycle-manager/scripts/traceability_lookup.py",
];

const USAGE = `Usage: install-spec-lifecycle-manager-package.sh [options]

Options:
  --source <path>       Package source root. Defaults to the checkout root.
  --codex-home <path>   Codex home. Defaults to $CODEX_HOME or ~/.codex.
  --marketplace-root <path>
                        Local marketplace root. Defaults to ~.
  --repo-root <path>    Repository root exposed by the MCP server. Defaults to source root.
  --skip-codex-config   Do not remove old host-level Codex MCP config.
  --skip-codex-hooks    Do not remove old global Codex hook config.
  --skip-marketplace    Copy files without editing the local marketplace.
  --skip-plugin-add     Do not run \`codex plugin add\` after copying files.
  --dry-run             Print planned actions without writing files.
  -h, --help            Show this help.
`;

class InstallError extends Error {
  constructor(message, exitCode = 1) {
    super(message);
    this.exitCode = exitCode;
  }
}

/** Minimal bash `printf %q` equivalent: identity for shell-safe tokens. */
function shQuote(value) {
  return /^[A-Za-z0-9_@%+=:,./-]+$/.test(value)
    ? value
    : `'${value.replace(/'/g, "'\\''")}'`;
}

function parseArgs(argv) {
  const opts = {
    source: null,
    codexHome: process.env.CODEX_HOME || path.join(os.homedir(), ".codex"),
    marketplaceRoot: process.env.SPEC_LIFECYCLE_MARKETPLACE_ROOT || os.homedir(),
    marketplaceName: process.env.SPEC_LIFECYCLE_MARKETPLACE_NAME || "auriora-local",
    repoRoot: "",
    writeCodexConfig: true,
    writeCodexHooks: true,
    writeMarketplace: true,
    installCodexPlugin: true,
    dryRun: false,
    help: false,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    switch (arg) {
      case "--source": opts.source = argv[i += 1]; break;
      case "--codex-home": opts.codexHome = argv[i += 1]; break;
      case "--marketplace-root": opts.marketplaceRoot = argv[i += 1]; break;
      case "--repo-root": opts.repoRoot = argv[i += 1]; break;
      case "--skip-codex-config": opts.writeCodexConfig = false; break;
      case "--skip-codex-hooks": opts.writeCodexHooks = false; break;
      case "--skip-marketplace": opts.writeMarketplace = false; break;
      case "--skip-plugin-add": opts.installCodexPlugin = false; break;
      case "--dry-run": opts.dryRun = true; break;
      case "-h":
      case "--help": opts.help = true; break;
      default:
        throw new InstallError(`Unknown option: ${arg}`, 2);
    }
  }
  return opts;
}

/** Create the directory if missing, then return its canonical absolute path. */
function ensureDirResolved(dir) {
  fs.mkdirSync(dir, { recursive: true });
  return fs.realpathSync(dir);
}

function planOrRun(dryRun, display, action) {
  if (dryRun) {
    process.stdout.write(`dry-run:${display.map((a) => ` ${shQuote(a)}`).join("")}\n`);
  } else {
    action();
  }
}

function copyTree(source, destination, dryRun) {
  const parent = path.dirname(destination);
  planOrRun(dryRun, ["mkdir", "-p", parent], () => fs.mkdirSync(parent, { recursive: true }));
  planOrRun(dryRun, ["rm", "-rf", destination], () => fs.rmSync(destination, { recursive: true, force: true }));
  planOrRun(dryRun, ["cp", "-a", source, destination], () => fs.cpSync(source, destination, { recursive: true }));
}

/** Reproduce `chmod +x`: add execute bits to existing mode. No-op semantics on Windows. */
function chmodExecutable(target, dryRun) {
  planOrRun(dryRun, ["chmod", "+x", target], () => {
    if (process.platform === "win32") return;
    fs.chmodSync(target, fs.statSync(target).mode | 0o111);
  });
}

function ensurePython() {
  // R2/P4: resolve the host interpreter explicitly instead of assuming the
  // literal name `python3`, and enforce the 3.10 floor the runtime requires
  // (spec_runtime.py uses 3.10+ features such as zip(strict=) and PEP 604
  // unions) by composing the floor into the candidate probe so ordering and
  // floor agree.
  const probe = (command) => {
    const [bin, ...args] = command;
    if (!bin) return false;
    const result = spawnSync(bin, [...args, "--version"], { encoding: "utf8", windowsHide: true });
    if (result.error || result.status !== 0) return false;
    const text = `${result.stdout || ""}${result.stderr || ""}`;
    const match = text.match(/Python\s+(\d+)\.(\d+)/i);
    if (!match) return false;
    const [major, minor] = [Number(match[1]), Number(match[2])];
    return major > 3 || (major === 3 && minor >= 10);
  };
  try {
    return resolvePython({ probe });
  } catch {
    throw new InstallError(
      "Python 3.10 or newer is required. Install it (Windows: python.org or "
        + "'winget install Python.Python.3'; macOS: 'brew install python'; Linux: "
        + "your distribution's python3 package), or set SPEC_LIFECYCLE_PYTHON to a "
        + "Python 3.10+ interpreter.",
    );
  }
}

/** Shell-free PATH lookup (P1): true when `name` is an executable on PATH. */
function isOnPath(name) {
  const entries = (process.env.PATH || "").split(path.delimiter).filter(Boolean);
  const exts = process.platform === "win32"
    ? (process.env.PATHEXT || ".COM;.EXE;.BAT;.CMD").split(";").filter(Boolean)
    : [""];
  for (const dir of entries) {
    for (const ext of exts) {
      const candidate = path.join(dir, name + ext);
      try {
        if (fs.statSync(candidate).isFile()) return true;
      } catch { /* not here; keep looking */ }
    }
  }
  return false;
}

function requireCommand(name, hint) {
  if (!isOnPath(name)) {
    throw new InstallError(`Missing required dependency: ${name}. ${hint}`);
  }
}

function removeOldSkillInstall(codexHome, dryRun) {
  const oldSkillRoot = path.join(codexHome, "skills", "spec-lifecycle-manager");
  if (dryRun) {
    process.stdout.write(`dry-run: remove old standalone skill install from ${oldSkillRoot}\n`);
    return;
  }
  if (fs.existsSync(oldSkillRoot)) {
    fs.rmSync(oldSkillRoot, { recursive: true, force: true });
  }
}

function removeOldCodexConfig(codexHome, dryRun) {
  const configPath = path.join(codexHome, "config.toml");
  if (dryRun) {
    process.stdout.write(`dry-run: remove old Spec Lifecycle Manager MCP config block from ${configPath}\n`);
    return;
  }
  if (!fs.existsSync(configPath)) return;

  let lines = fs.readFileSync(configPath, "utf8").split(/\r?\n/);

  // Drop any "# BEGIN/END Spec Lifecycle Manager package install" block.
  const blockStripped = [];
  let skipping = false;
  for (const line of lines) {
    if (/# BEGIN Spec Lifecycle Manager package install/.test(line)) { skipping = true; continue; }
    if (/# END Spec Lifecycle Manager package install/.test(line)) { skipping = false; continue; }
    if (!skipping) blockStripped.push(line);
  }

  // Drop any [mcp_servers.spec-lifecycle-manager] table (and sub-tables).
  const headerPattern = /^\s*\[([^\]]+)\]\s*$/;
  const removePrefix = "mcp_servers.spec-lifecycle-manager";
  const kept = [];
  let removing = false;
  for (const line of blockStripped) {
    const match = line.match(headerPattern);
    if (match) {
      const table = match[1];
      removing = table === removePrefix || table.startsWith(`${removePrefix}.`);
    }
    if (!removing) kept.push(line);
  }

  const text = `${kept.join("\n").replace(/\s+$/, "")}\n`;
  fs.writeFileSync(configPath, text, "utf8");
}

function removeOldCodexHooksJson(codexHome, dryRun) {
  const hooksJson = path.join(codexHome, "hooks.json");
  if (dryRun) {
    process.stdout.write(`dry-run: remove old global Spec Lifecycle Manager hook from ${hooksJson}\n`);
    return;
  }
  if (!fs.existsSync(hooksJson)) return;

  let data = JSON.parse(fs.readFileSync(hooksJson, "utf8"));
  if (data === null || typeof data !== "object" || Array.isArray(data)) data = { hooks: {} };
  if (data.hooks === null || typeof data.hooks !== "object" || Array.isArray(data.hooks)) data.hooks = {};
  const hooks = data.hooks;

  const entries = hooks.PostToolUse;
  if (!Array.isArray(entries)) return; // matches the .sh SystemExit(0): no write

  const marker = "/spec-lifecycle-manager/scripts/codex_spec_lifecycle_hook.py";
  const keepEntry = (entry) => {
    if (entry === null || typeof entry !== "object") return false;
    const entryHooks = entry.hooks;
    if (!Array.isArray(entryHooks)) return true;
    entry.hooks = entryHooks.filter((hook) => !String(hook?.command ?? "").includes(marker));
    return entry.hooks.length > 0;
  };

  const remaining = entries.filter(keepEntry);
  if (remaining.length > 0) hooks.PostToolUse = remaining;
  else delete hooks.PostToolUse;

  fs.mkdirSync(path.dirname(hooksJson), { recursive: true });
  fs.writeFileSync(hooksJson, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function writeMarketplaceJson(marketplaceJson, marketplaceName, dryRun) {
  if (dryRun) {
    process.stdout.write(`dry-run: add Spec Lifecycle Manager to ${marketplaceJson}\n`);
    return;
  }

  const entry = {
    name: "spec-lifecycle-manager",
    source: { source: "local", path: "./plugins/spec-lifecycle-manager" },
    policy: { installation: "AVAILABLE", authentication: "ON_INSTALL" },
    category: "Developer Tools",
  };

  let data = {
    name: marketplaceName,
    interface: { displayName: "Auriora Local Plugins" },
    plugins: [],
  };
  if (fs.existsSync(marketplaceJson)) data = JSON.parse(fs.readFileSync(marketplaceJson, "utf8"));
  if (data === null || typeof data !== "object" || Array.isArray(data)) data = {};
  if (!("name" in data)) data.name = marketplaceName;
  if (!("interface" in data)) data.interface = { displayName: "Auriora Local Plugins" };
  if (data.interface === null || typeof data.interface !== "object" || Array.isArray(data.interface)) {
    data.interface = { displayName: "Auriora Local Plugins" };
  }
  if (!("displayName" in data.interface)) data.interface.displayName = "Auriora Local Plugins";

  let plugins = data.plugins;
  if (!Array.isArray(plugins)) plugins = [];
  plugins = plugins.filter((plugin) => plugin?.name !== entry.name);
  plugins.push(entry);
  data.plugins = plugins;

  fs.mkdirSync(path.dirname(marketplaceJson), { recursive: true });
  fs.writeFileSync(marketplaceJson, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

// --- T002/T003: pin the resolved interpreter into the installed configs ---

/** Pin `.mcp.json`: replace the interpreter, preserve the `*.py` script arg. */
function pinMcpFile(file, pythonCmd) {
  const data = JSON.parse(fs.readFileSync(file, "utf8"));
  const servers = data.mcpServers || {};
  for (const key of Object.keys(servers)) {
    const server = servers[key];
    const scriptArg = (server.args || []).find((arg) => String(arg).endsWith(".py"));
    if (!scriptArg) continue;
    server.command = pythonCmd[0];
    server.args = [...pythonCmd.slice(1), scriptArg];
  }
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

/**
 * Pin `hooks.json`: exec form (Claude, has `args`) gets command+args; shell
 * form (Codex, OQ4) keeps its quoted script tail with the resolved interpreter
 * swapped in.
 */
function pinHookFile(file, pythonCmd) {
  const data = JSON.parse(fs.readFileSync(file, "utf8"));
  for (const group of data.hooks?.PostToolUse || []) {
    for (const hook of group.hooks || []) {
      if (hook.type !== "command") continue;
      if (Array.isArray(hook.args)) {
        const scriptArg = hook.args.find((arg) => String(arg).endsWith(".py")) ?? hook.args.at(-1);
        hook.command = pythonCmd[0];
        hook.args = [...pythonCmd.slice(1), scriptArg];
      } else if (typeof hook.command === "string") {
        const quote = hook.command.indexOf('"');
        const tail = quote >= 0 ? hook.command.slice(quote) : `"${hook.command.split(/\s+/).pop()}"`;
        hook.command = `${pythonCmd.join(" ")} ${tail}`;
      }
    }
  }
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function pinOne(file, pythonCmd, dryRun, transform) {
  if (!fs.existsSync(file)) return;
  if (dryRun) {
    process.stdout.write(`dry-run: pin interpreter '${pythonCmd.join(" ")}' into ${file}\n`);
    return;
  }
  transform(file, pythonCmd);
}

/** Pin both the Codex and Claude config copies under an installed plugin root. */
function pinInstalledConfigs(root, pythonCmd, dryRun) {
  pinOne(path.join(root, ".mcp.json"), pythonCmd, dryRun, pinMcpFile);
  pinOne(path.join(root, "claude-plugin", ".mcp.json"), pythonCmd, dryRun, pinMcpFile);
  pinOne(path.join(root, "hooks", "hooks.json"), pythonCmd, dryRun, pinHookFile);
  pinOne(path.join(root, "claude-plugin", "hooks", "hooks.json"), pythonCmd, dryRun, pinHookFile);
}

function installCodexPlugin(marketplaceName, dryRun) {
  requireCommand("codex", "Install Codex or pass --skip-plugin-add to copy files without registering the plugin.");
  const ref = `spec-lifecycle-manager@${marketplaceName}`;
  planOrRun(dryRun, ["codex", "plugin", "add", ref], () => {
    const result = spawnSync("codex", ["plugin", "add", ref], { stdio: "inherit" });
    if (result.status !== 0) throw new InstallError(`codex plugin add failed for ${ref}`);
  });
}

/**
 * Install the spec-lifecycle-manager package.
 * @param {string[]} argv installer arguments (as passed after the program name)
 * @returns {number} process exit code
 */
export async function install(argv = []) {
  let opts;
  try {
    opts = parseArgs(argv);
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.stderr.write(USAGE);
    return error instanceof InstallError ? error.exitCode : 2;
  }

  if (opts.help) {
    process.stdout.write(USAGE);
    return 0;
  }

  try {
    const sourceRoot = fs.realpathSync(opts.source ? opts.source : process.cwd());
    const repoRoot = fs.realpathSync(opts.repoRoot ? opts.repoRoot : sourceRoot);
    const codexHome = ensureDirResolved(opts.codexHome);
    const marketplaceRoot = ensureDirResolved(opts.marketplaceRoot);
    void repoRoot; // resolved for parity; reserved for future MCP repo-root wiring

    for (const relativePath of REQUIRED_PATHS) {
      if (!fs.existsSync(path.join(sourceRoot, relativePath))) {
        throw new InstallError(`Missing package component: ${relativePath}`);
      }
    }

    const pluginInstallRoot = path.join(codexHome, "plugins", "spec-lifecycle-manager");
    const marketplacePluginRoot = path.join(marketplaceRoot, "plugins", "spec-lifecycle-manager");
    const marketplaceJson = path.join(marketplaceRoot, ".agents", "plugins", "marketplace.json");
    const pluginSource = path.join(sourceRoot, "plugins", "spec-lifecycle-manager");

    const pythonCmd = ensurePython();
    removeOldSkillInstall(codexHome, opts.dryRun);
    copyTree(pluginSource, pluginInstallRoot, opts.dryRun);
    copyTree(pluginSource, marketplacePluginRoot, opts.dryRun);
    for (const root of [pluginInstallRoot, marketplacePluginRoot]) {
      for (const script of EXECUTABLE_SCRIPTS) {
        chmodExecutable(path.join(root, script), opts.dryRun);
      }
    }
    // T002/T003: pin the host-resolved interpreter into both installed copies
    // (install root and marketplace root), so whichever copy Codex/Claude runs
    // launches with an interpreter proven to exist on this host.
    pinInstalledConfigs(pluginInstallRoot, pythonCmd, opts.dryRun);
    pinInstalledConfigs(marketplacePluginRoot, pythonCmd, opts.dryRun);

    if (opts.writeCodexConfig) removeOldCodexConfig(codexHome, opts.dryRun);
    if (opts.writeCodexHooks) removeOldCodexHooksJson(codexHome, opts.dryRun);
    if (opts.writeMarketplace) writeMarketplaceJson(marketplaceJson, opts.marketplaceName, opts.dryRun);
    if (opts.installCodexPlugin) installCodexPlugin(opts.marketplaceName, opts.dryRun);

    process.stdout.write(`Spec Lifecycle Manager installed at ${codexHome}\n`);
    return 0;
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    return error instanceof InstallError ? error.exitCode : 1;
  }
}

// Self-execution guard: run when invoked directly (node installer.mjs ...).
if (process.argv[1] && fileURLToPath(import.meta.url) === fs.realpathSync(process.argv[1])) {
  install(process.argv.slice(2)).then((code) => process.exit(code));
}
