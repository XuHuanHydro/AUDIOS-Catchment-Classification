# WRR 2026WR044991: revision reproducibility materials

**AUDIOS: An Interpretable Framework for Global Catchment Classification Based on Hydrological Signatures**

This package corresponds to revision **v8, 4 October 2026**, prepared for Water Resources Research. It is a **partial reproducibility package starting from archived intermediate results**. It redraws five adopted figures and checks the statistics behind those plots and Tables S6–S8. It does not retrain the classifiers, select donors, reconstruct daily discharge, or recompute hydrological signatures from raw observations.

## Quick start

Python 3.12 is recommended. From this directory:

```sh
python -m venv .venv
# Activate on Windows: .venv\Scripts\activate
# Activate on macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/reproduce.py
```

No external datasets, network calls, MATLAB, GPU, or local project paths are needed after installing dependencies. The full check took about 10 seconds on the preparation machine. Files are written to `generated/`; the supplied inputs are not overwritten. The scripts resolve paths relative to their location, so they can also be called from a different working directory. Do not use Python's `-O` flag, which disables assertion checks.

The scripts use Times New Roman when installed, with DejaVu Serif as a fallback. Font or platform changes can alter typography and PDF bytes; the numerical checks should still pass. The five PNGs in [examples](examples/) were regenerated with the pinned environment and were pixel-identical to the adopted figure sources on the preparation machine.

## What is reproduced

| Revision item | Packaged input | Reproduction/check |
|---|---|---|
| Figure 8 | `data/external/GSIM/` | 18 signatures, 831 catchments; separation contrasts and four RMSE comparison lines |
| Figure S11 | `data/external/GSCD/` | 17 signatures, 355 catchments (213 for T50); same comparisons |
| Figure S12 | `data/external/GSHA/` | 14 signatures, 803 catchments; same comparisons |
| Tables S6–S8 | `data/external/reconstruction_summary.csv` and displayed reference tables | 245 unrounded RMSE results (49 signatures × five methods), checked against the displayed table values |
| Figure 9 | `data/daily/Figure9/` | 2016–2020 NSE/KGE boxplots and paired AUDIOSK5–KnobenK5 differences |
| Figure S17 | `data/daily/FigureS17/` | The same evaluation cohorts over 1981–2015 |

`signature_definitions.csv` files transcribe the corresponding parts of Table S4, including units. Definitions and raw-source conventions are dataset-specific. A matching short label across datasets does not imply an identical definition or unit.

## Interpretation and sample boundaries

- Separation differences are AUDIOS minus the climate classification. Each metric has its own zero-centered color scale. RMSE improvement is `100 * (baseline RMSE - AUDIOS RMSE) / baseline RMSE`; negative improvements are retained.
- External signature estimates use class means or up to five nearest donors **within the target class**. The fourth plotted line compares an AUDIOS class mean with KnobenK5 and therefore has unequal donor rules.
- The daily five-method boxplots use **626 catchments**, common to all five methods and both periods. Each method is evaluated on its own valid dates. The paired comparison uses **627 catchments**, common to the two K5 methods and both periods, with matching valid dates within each pair and period. Paired medians need not equal differences of the boxplot medians.
- In the daily experiment, AUDIOSK5 uses signature-space nearest donors without a class restriction. The daily and external K5 donor rules must not be conflated.
- Daily scores are archived intermediate outputs. This package cannot independently verify upstream time alignment, predictions, cohort screening, or model fitting. The full manuscript describes those operations. No raw discharge series or trained model weights are included.
- All eligible plotted scores, negative values, and outliers are retained. The daily difference histograms use 36 equal-width bins **in display coordinates** on a symmetric-log axis, with a linear threshold of ±0.2 and zero as a bin edge. Median lines remain at their actual values.

## Files and validation

- [DATA_DICTIONARY.md](DATA_DICTIONARY.md): columns, method labels, and units.
- [provenance.json](provenance.json): SHA-256 input hashes and source identifiers. Historical source paths are provenance labels, not runtime dependencies. Figure 8 and 9 source PDFs matched the v8 submission PDFs byte-for-byte; SI source images matched the embedded image bytes in the final SI document.
- `scripts/reproduce.py`: checks input integrity; verifies separation arithmetic, sample counts, RMSE comparisons and displayed tables; runs all figures; compares regenerated daily scores, quartiles, medians, percentiles, win rates, and bins to archived references.
- `generated/verification.json`: validation report from your own run.
- [examples/verification.json](examples/verification.json): successful preparation-run report; [figure_comparison.json](examples/figure_comparison.json): local pixel comparison with the adopted sources.

Figures 1–7, other SI figures, the global mapping pipeline, raw-data processing, and full training are outside this package. The older root-level demos are retained for reference and are not a substitute for this revision-specific workflow.

## Data sources, reuse, and citation

The supplied files contain author-produced evaluation scores, aggregated benchmark results, figure inputs, and table definitions. Underlying observations come from the Caravan catchment collection and the GSIM, GSCD, and GSHA resources described and cited in the manuscript/SI. Original time series and third-party dataset files are not redistributed here. Obtain those resources from their original providers under their respective terms for work requiring raw data.

The repository's [CC BY-NC-SA 4.0 license](../LICENSE) applies to the authored package; it does not replace the terms of upstream datasets. Cite the AUDIOS manuscript using its publication details when available and identify the exact repository commit used. Manuscript number 2026WR044991 is an editorial identifier, not a DOI. This package does not claim a publication or archival DOI.
