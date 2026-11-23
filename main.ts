// main.ts — entrypoint for news-image-20261123 (R2).
// Copies the committed entry.png to MAKEFUN_OUTPUT_DIR. No rendering,
// no Python, no writes to the repository. Node stdlib only.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath as urlToPath } from "node:url";

const here = path.dirname(urlToPath(import.meta.url));
const targetDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const sourcePng = path.join(here, "entry.png");
const destPng = path.join(targetDir, "entry.png");

if (!fs.existsSync(sourcePng)) {
  console.error(`missing source image: ${sourcePng}`);
  process.exit(1);
}

fs.mkdirSync(targetDir, { recursive: true });
fs.copyFileSync(sourcePng, destPng);
const bytes = fs.statSync(destPng).size;
console.log(`wrote ${destPng} (${bytes} bytes)`);
