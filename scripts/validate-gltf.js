#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const validator = require('gltf-validator');

async function main() {
  const [input, output] = process.argv.slice(2);
  if (!input || !output) {
    throw new Error('Usage: node scripts/validate-gltf.js MODEL REPORT.json');
  }
  const root = path.dirname(path.resolve(input));
  const report = await validator.validateBytes(new Uint8Array(fs.readFileSync(input)), {
    uri: path.basename(input),
    maxIssues: 1000,
    externalResourceFunction: async (uri) => {
      const relative = decodeURIComponent(uri);
      const resolved = path.resolve(root, relative);
      if (!resolved.startsWith(root + path.sep) || /^[a-z]+:/i.test(relative)) {
        throw new Error(`Unsafe external glTF resource: ${relative}`);
      }
      return new Uint8Array(fs.readFileSync(resolved));
    },
  });
  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.writeFileSync(output, JSON.stringify(report, null, 2) + '\n');
  const issues = report.issues;
  console.log(`${issues.numErrors} errors, ${issues.numWarnings} warnings, ${issues.numInfos} infos`);
  // Keep warnings visible for visual review instead of treating every warning as a defect.
  process.exitCode = issues.numErrors ? 1 : 0;
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
