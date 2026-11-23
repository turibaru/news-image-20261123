// main.ts — entrypoint for news-image-20261123 (R2).
// Renders entry.png with render.py, then copies it to MAKEFUN_OUTPUT_DIR.
// Node stdlib only. Run: MAKEFUN_OUTPUT_DIR=/tmp/out node main.ts
import { spawnSync } from "node:child_process";
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || join(repoDir, "output");

const rendered = spawnSync("python3", ["render.py"], { cwd: repoDir, stdio: "inherit" });
if (rendered.status !== 0) {
  process.exit(rendered.status ?? 1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(join(repoDir, "entry.png"), join(outDir, "entry.png"));
