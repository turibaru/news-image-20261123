import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = join(dirname(fileURLToPath(import.meta.url)), "entry.png");
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);
console.log(`Copied entry.png to ${dest}`);
