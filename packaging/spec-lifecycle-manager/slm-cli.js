#!/usr/bin/env node
"use strict";

const { spawnSync } = require("node:child_process");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const packageRoot = path.resolve(__dirname, "..", "..");
const installerUrl = pathToFileURL(path.join(__dirname, "installer.mjs"));
const resolverUrl = pathToFileURL(path.join(__dirname, "resolve-python.mjs"));
const pythonCli = path.join(
  packageRoot,
  "plugins",
  "spec-lifecycle-manager",
  "skills",
  "spec-lifecycle-manager",
  "scripts",
  "slm_cli.py",
);

async function dispatch(argv, dependencies = {}) {
  const args = [...argv];
  const root = dependencies.packageRoot || packageRoot;
  const cliPath = dependencies.pythonCli || (root === packageRoot
    ? pythonCli
    : path.join(root, "plugins/spec-lifecycle-manager/skills/spec-lifecycle-manager/scripts/slm_cli.py"));
  const writeError = dependencies.writeError || ((message) => process.stderr.write(message));

  if (args[0] === "install") {
    const installerArgs = args.slice(1);
    const forwarded = installerArgs[0] === "--" ? installerArgs.slice(1) : installerArgs;
    const install = dependencies.install || (await import(installerUrl.href)).install;
    return install(["--source", root, ...forwarded]);
  }

  const resolvePython = dependencies.resolvePython || (await import(resolverUrl.href)).resolvePython;
  const run = dependencies.spawnSync || spawnSync;
  const signalProcess = dependencies.signalProcess || ((signal) => process.kill(process.pid, signal));
  let pythonCommand;
  try {
    pythonCommand = resolvePython();
  } catch (error) {
    writeError(`slm: ${error?.message || error}\n`);
    return 1;
  }

  const [python, ...pythonArgs] = pythonCommand;
  const queryArgs = args.length === 0 ? ["specs"] : args;
  const result = run(python, [...pythonArgs, cliPath, ...queryArgs], {
    stdio: "inherit",
    shell: false,
    windowsHide: true,
  });
  if (result.error) {
    writeError(`slm: ${result.error.message || result.error}\n`);
    return 1;
  }
  if (result.signal) {
    signalProcess(result.signal);
    return 1;
  }
  return Number.isInteger(result.status) ? result.status : 1;
}

async function main() {
  return dispatch(process.argv.slice(2));
}

if (require.main === module) {
  main()
    .then((code) => process.exit(code))
    .catch((error) => {
      process.stderr.write(`slm: ${error?.stack || error}\n`);
      process.exit(1);
    });
}

module.exports = { dispatch, main, packageRoot, pythonCli };
