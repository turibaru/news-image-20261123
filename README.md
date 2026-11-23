# The World in One Day — 23 November 2026

[![News image 23 Nov 2026](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/c/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/turibaru/news-image-20261123/rank.svg)](https://make.fun/c/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/turibaru/news-image-20261123/reward.svg)](https://make.fun/c/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A dense front-page image summing up world news on Monday, 23 November 2026: 38 stories across 7 regions, led by NVIDIA reinstating Jensen Huang as CEO, Trump's Justice Department address, and Democrats clinching the House — with a red DATE CHECK box (every story happened or was first reported on 23 Nov 2026 UTC; stale stories named and left out), a strictly chronological UTC timeline, and sections for the Middle East, Europe, North America, Latin America, South Asia, East Asia & Pacific, Africa, markets and tech, and sport, science and culture. Rendered deterministically with `python3 render.py`.

## Date discipline

Every story in the image happened or was first reported on Monday 23 November 2026 (UTC). The DATE CHECK box on the page names what was deliberately left out: the NVIDIA chief stepping down (12 Nov), the "El Chapo Isidro" arrest (20 Nov), BepiColombo entering Mercury orbit (21 Nov), and COP31 collapsing (22 Nov). No story appears twice — lead, sub-leads, body sections, and timeline are disjoint, and `render.py` asserts 38 unique stories.

## Verify

```sh
python3 render.py            # renders entry.png (1024x1024, deterministic)
sha256sum entry.png           # run twice: hashes must be identical
MAKEFUN_OUTPUT_DIR=/tmp/out-r2 node main.ts   # entrypoint copies entry.png
```
