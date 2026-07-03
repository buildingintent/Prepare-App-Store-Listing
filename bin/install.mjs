#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const skillName = "prepare-app-store-listing";
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const skillRoot = path.join(root, "skills", skillName);
const codexHome = process.env.CODEX_HOME || path.join(os.homedir(), ".codex");
const dest = argValue("--dest") || path.join(codexHome, "skills", skillName);
const include = ["SKILL.md", "agents", "references", "scripts"];

function argValue(name) {
  const index = process.argv.indexOf(name);
  return index === -1 ? "" : process.argv[index + 1] || "";
}

function copy(source, target) {
  const stat = fs.statSync(source);
  if (stat.isDirectory()) {
    fs.mkdirSync(target, { recursive: true });
    for (const entry of fs.readdirSync(source)) {
      copy(path.join(source, entry), path.join(target, entry));
    }
    return;
  }
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.copyFileSync(source, target);
}

fs.rmSync(dest, { recursive: true, force: true });
for (const entry of include) {
  copy(path.join(skillRoot, entry), path.join(dest, entry));
}

console.log(`Installed ${skillName} to ${dest}`);
console.log("Restart Codex, then run: /store:prepare");
