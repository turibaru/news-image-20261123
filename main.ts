// main.ts — entrypoint for news-image-20261123 (R2).
// Renders entry.png with render.py directly into MAKEFUN_OUTPUT_DIR.
// The repository is read-only on the grader, so nothing is ever written
// into the repo directory: render.py runs with cwd = output dir.
// Node stdlib only. Run: MAKEFUN_OUTPUT_DIR=/tmp/out node main.ts
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || join(repoDir, "output");

mkdirSync(outDir, { recursive: true });

const rendered = spawnSync("python3", [join(repoDir, "render.py")], { cwd: outDir, stdio: "inherit" });
if (rendered.status !== 0) {
  process.exit(rendered.status ?? 1);
}

if (!existsSync(join(outDir, "entry.png"))) {
  console.error("entry.png missing after render");
  process.exit(1);
}
