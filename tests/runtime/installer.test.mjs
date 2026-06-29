"use strict";

import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { install } from "../../packaging/spec-lifecycle-manager/installer.mjs";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");

function tempHomes() {
  const base = fs.mkdtempSync(path.join(os.tmpdir(), "slm-install-"));
  return { base, home: path.join(base, "home"), mkt: path.join(base, "mkt") };
}

test("--help returns 0", async () => {
  assert.equal(await install(["--help"]), 0);
});

test("unknown option returns 2", async () => {
  assert.equal(await install(["--bogus"]), 2);
});

test("real install copies the plugin tree and registers the marketplace", async () => {
  const { base, home, mkt } = tempHomes();
  try {
    const code = await install([
      "--source", repoRoot,
      "--codex-home", home,
      "--marketplace-root", mkt,
      "--skip-plugin-add",
    ]);
    assert.equal(code, 0);

    // Plugin tree copied into the Codex home and the marketplace root.
    for (const root of [
      path.join(home, "plugins", "spec-lifecycle-manager"),
      path.join(mkt, "plugins", "spec-lifecycle-manager"),
    ]) {
      assert.ok(fs.existsSync(path.join(root, ".mcp.json")), `${root}/.mcp.json`);
      assert.ok(
        fs.existsSync(path.join(root, "skills/spec-lifecycle-manager/scripts/spec_mcp_server.py")),
        `${root} server script`,
      );
    }

    // Marketplace registration written with our entry.
    const marketplace = JSON.parse(
      fs.readFileSync(path.join(mkt, ".agents", "plugins", "marketplace.json"), "utf8"),
    );
    const entry = marketplace.plugins.find((p) => p.name === "spec-lifecycle-manager");
    assert.ok(entry, "marketplace entry present");
    assert.equal(entry.source.path, "./plugins/spec-lifecycle-manager");
  } finally {
    fs.rmSync(base, { recursive: true, force: true });
  }
});

test("--skip-marketplace leaves the marketplace untouched", async () => {
  const { base, home, mkt } = tempHomes();
  try {
    const code = await install([
      "--source", repoRoot,
      "--codex-home", home,
      "--marketplace-root", mkt,
      "--skip-plugin-add",
      "--skip-marketplace",
    ]);
    assert.equal(code, 0);
    assert.ok(!fs.existsSync(path.join(mkt, ".agents", "plugins", "marketplace.json")));
  } finally {
    fs.rmSync(base, { recursive: true, force: true });
  }
});

test("missing package component fails loudly", async () => {
  const { base, home, mkt } = tempHomes();
  const emptySource = path.join(base, "empty-source");
  fs.mkdirSync(emptySource, { recursive: true });
  try {
    const code = await install([
      "--source", emptySource,
      "--codex-home", home,
      "--marketplace-root", mkt,
      "--skip-plugin-add",
    ]);
    assert.equal(code, 1);
  } finally {
    fs.rmSync(base, { recursive: true, force: true });
  }
});
