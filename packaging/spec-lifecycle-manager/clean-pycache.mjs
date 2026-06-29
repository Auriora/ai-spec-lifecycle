#!/usr/bin/env node
"use strict";

// Spec 028: npm's `files` allowlist pulls __pycache__/*.pyc into the tarball
// even though .npmignore lists them, so a stray dev-run cache would ship in a
// GitHub-release tarball. This prepack step removes Python bytecode caches from
// the packaged trees before `npm pack` gathers files. Cross-platform (Node fs).

import fs from "node:fs";
import path from "node:path";

const ROOTS = ["plugins", "skills", "packaging"];
const SKIP = new Set(["node_modules", ".git"]);

let removed = 0;

function clean(dir) {
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === "__pycache__") {
        fs.rmSync(full, { recursive: true, force: true });
        removed += 1;
      } else if (!SKIP.has(entry.name)) {
        clean(full);
      }
    } else if (/\.py[cod]$/.test(entry.name)) {
      fs.rmSync(full, { force: true });
      removed += 1;
    }
  }
}

for (const root of ROOTS) clean(root);
// Write to stderr: `npm pack --json` reserves stdout for the file manifest.
if (removed > 0) process.stderr.write(`clean-pycache: removed ${removed} bytecode cache entr${removed === 1 ? "y" : "ies"}\n`);
