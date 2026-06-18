# 🤖 obsolescence-atlas — will a robot take this job?

An occupation explorer that merges **three published automation/AI-exposure forecasts** with BLS employment projections — and shows how violently they **disagree**.

### ▶️ [Live demo](https://danielduongg.github.io/obsolescence-atlas/)

Pick any of 49 occupations and compare its Frey–Osborne automation probability (2013), Felten AI Occupational Exposure, and Eloundou GPT-exposure (2023), against the BLS 10-year jobs outlook and median wage.

## The finding: the forecasts barely agree

| Measure pair | Correlation |
|---|---|
| Frey–Osborne (2013) vs **GPT-exposure (2023)** | **+0.15** (≈ unrelated) |
| Frey–Osborne (2013) vs Felten AIOE | +0.20 |
| Felten AIOE vs GPT-exposure | **+0.96** |

The 2013 automation lens points at **manual/routine** work (welders, cashiers, drivers, fast-food cooks); the 2023 LLM lens points at **cognitive/writing** work (writers, market analysts, paralegals, PR). They're nearly orthogonal. The two AI-era measures agree with each other — but not with 2013.

Two more honest notes built into the demo:
- **Exposure ≠ replacement.** Plenty of high-exposure occupations are still *growing* in BLS projections (interpreters +20%, software +25%). Being "exposed" to a technology is not the same as being eliminated by it.
- **Frey–Osborne's 2013 alarm was overstated** — the jobs it flagged as 90%+ automatable largely still exist a decade later.

So: confidently predicting which trades go obsolete is far shakier than headlines suggest.

## Files
- `occupations.json` — 49 occupations × {Frey–Osborne, Felten AIOE, Eloundou GPT-exposure, BLS 10-yr %, median wage}, with sources. Curated representative values from the published studies.
- `analysis.py` — correlation matrix + risk categorization.
- `index.html` — the in-browser explorer (gauges + the disagreement scatter).

```bash
pip install -r requirements.txt
python analysis.py
python build_demo.py
```
