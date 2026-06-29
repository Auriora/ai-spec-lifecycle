#!/usr/bin/env node
"use strict";

const path = require("node:path");
const { pathToFileURL } = require("node:url");

const packageRoot = path.resolve(__dirname, "..", "..");
const installerUrl = pathToFileURL(path.join(__dirname, "installer.mjs"));

function usage() {
  process.stdout.write(`Usage: spec-lifecycle-manager <command> [installer options]

Commands:
  install      Install or refresh the Codex plugin from this npm package.
  help         Show this help.

Examples:
  npx @auriora/ai-spec-lifecycle install
  npx @auriora/ai-spec-lifecycle install -- --codex-home ~/.codex
`);
}

async function main() {
  const args = process.argv.slice(2);
  const command = args.shift() || "install";

  if (command === "help" || command === "--help" || command === "-h") {
    usage();
    return 0;
  }

  if (command !== "install") {
    process.stderr.write(`Unknown command: ${command}\n\n`);
    usage();
    return 2;
  }

  const installerArgs = args[0] === "--" ? args.slice(1) : args;
  // installer.mjs is ESM; this entrypoint is CommonJS, so load it via dynamic
  // import and call it in-process (no shell, no spawned .sh).
  const { install } = await import(installerUrl.href);
  return install(["--source", packageRoot, ...installerArgs]);
}

main()
  .then((code) => process.exit(code))
  .catch((error) => {
    process.stderr.write(`${error?.stack || error}\n`);
    process.exit(1);
  });
