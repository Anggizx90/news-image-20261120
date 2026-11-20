# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Anggizx90/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Anggizx90/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-page newspaper front page — **THE WORLD TODAY, Friday 20 November 2026** — summing up the day's world news in a single 1024×1024 image. The lead story is the first-ever three-way Trump–Xi–Putin summit in Shenzhen and its four-point peace declaration; twelve further stories cover the ICJ's Rohingya genocide ruling against Myanmar, the third Ukrainian strike on the Crimean Bridge, the drone raid that damaged two embassies in Kyiv, Israel's tank raid across the Gaza ceasefire line, the Houthi missile that hit Riyadh's PIF Tower, Cyclone Akvan's landfall in India, Anthropic's record $81.3bn IPO, Fiji's drought disaster, South Korea's top court overturning ex-PM Han Duck-soo's sentence, Iran's remaining missile arsenal, North Korea's Yongbyon enrichment expansion, and Henry Nicholls' unbeaten century in Wellington — plus a round-up strip (S&P 500's fifth straight fall, the California probe into Nvidia, Trump's pardon of Pete Rose, COP31 closing in Antalya).

`main.py` (Python 3.13, standard library only) copies the finished `entry.png` to the output directory. `draw_poster.py` is the Pillow program that draws the page from scratch — every illustration is drawn with shapes, no photographs, no network — and writes `entry.png`. Both runs of `main.py` write byte-identical output.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To redraw the poster from scratch (needs Pillow):

```sh
python3 draw_poster.py
```

## News sources

All stories were reported 19–20 November 2026 (Reuters, AP, AFP, The Wall Street Journal, IAEA, India Meteorological Department, SEC filings):

- Trump, Xi and Putin hold first three-way summit in Shenzhen; four-point peace declaration issued, details thin; Putin says no agreements after the bridge strikes; European allies meet in Berlin and say they are ready for talks with Russia.
- ICJ rules Myanmar committed genocide against the Rohingya, 9–6, the first such finding against a state.
- Ukraine strikes the Crimean Bridge for a third time in four days — Neptune missiles hit the rail span, halting trains; the road arch fell on 17 November.
- Russian drone raid on Kyiv kills one and injures five, damaging the Dutch and Austrian embassies and St Volodymyr's Cathedral (19 November).
- Israeli tanks cross the Gaza "yellow line" in the first ground raid since the October 2025 truce; the raid ends after a day; 1,600+ Palestinians killed since the truce began.
- Suspected Houthi missile hits Riyadh's PIF Tower, blowing out windows across seven floors; no injuries.
- Severe Cyclone Akvan crosses the Andhra Pradesh–Odisha coast near Gopalpur; 300,000+ evacuated, gusts to 110 km/h.
- Anthropic prices its IPO at $83 a share ($81.3bn, the largest ever); ANT closes its first day at $97.17, up 17%; the offering closes 20 November.
- Fiji declares a nationwide state of disaster as El Niño drought drains water supplies; F$20m set aside for relief.
- South Korea's Supreme Court overturns ex-PM Han Duck-soo's 15-year sentence and orders a retrial; other guilty findings stand.
- US intelligence puts Iran's missile arsenal at 1,500–2,500 (low confidence) after nine months of war.
- IAEA: North Korea is expanding its uranium enrichment plant at Yongbyon.
- Cricket: Henry Nicholls 146 not out, Glenn Phillips 118, as New Zealand reach 317 for 6 at lunch on day two of the Wellington Test against India.
- Also: S&P 500 falls 2.0% for a fifth straight day; California opens a probe into Nvidia's China AI-chip sales; Trump posthumously pardons Pete Rose; COP31 closes in Antalya.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ymjg9sbn&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
