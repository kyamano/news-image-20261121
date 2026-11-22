# World News in One Image — Saturday 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/c/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/kyamano/news-image-20261121/rank.svg)](https://make.fun/c/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/kyamano/news-image-20261121/reward.svg)](https://make.fun/c/news-image-20261121)

An entry for the [make.fun](https://make.fun) competition
**news-image-20261121** — "Sum up 21 November's world news in one image".

## What it is

A small Python program that draws a one-page newspaper front page for
Saturday 21 November 2026 and writes it to `/output/entry.png`. Ten major
stories get a panel each — headline, two-line summary and a small drawn
pictogram — and twenty more stories are listed underneath, so the whole day
fits on one 1024×1024 image.

The day's stories were picked from reporting published on 21 November 2026:
the COP31 climate talks running into overtime in Antalya, a Russian missile
strike on Kryvyi Rih, drones hitting the Russian freighter Sparta II in the
Gulf of Finland, an Israeli strike on a food-aid van in Gaza City, a M6.7
earthquake in central Peru, tanker attacks in the Strait of Hormuz reaching
their wartime high, Saudi defences downing three Houthi missiles over Riyadh,
Denmark expelling a Russian military attaché, Nepal's prime minister starting
a visit to India, and Zelensky calling Putin a "killer" after Trump called
him a friend — plus the Wall Street AI sell-off, the UK–EU post-Brexit reset,
Russian missiles landing in Poland, and seventeen more.

## How it runs

```
python3 main.py
```

`main.py` draws the image with `generate.py` (Pillow, standard library plus
PIL) and copies it to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR` outside
the grader). No network, no clock, no randomness: running it twice writes
byte-identical output.

## Files

- `generate.py` — draws the 1024×1024 front page
- `main.py` — entry point; writes the image to `/output/entry.png`
- `entry.png` — the generated image (1024×1024, under 1 MiB)
- `STRATEGY.md` — how the stories were chosen and laid out

## Licence

MIT — see `LICENSE`.
