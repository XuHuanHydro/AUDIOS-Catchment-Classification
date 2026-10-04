# AUDIOS-Catchment-Classification
Global hydrological catchment classification system (AUDIOS) based on hydrological signatures, Fuzzy C-Means clustering, CART rule extraction, and Random Forest extrapolation.
 

## Current revision materials

The partial reproducibility package for **WRR 2026WR044991, revision v8 (4 October 2026)** is available in [revision_2026WR044991](revision_2026WR044991/). It includes intermediate data and runnable Python scripts for Figures 8, 9, S11, S12, and S17, with numerical checks for those plots and Tables S6–S8. See the package README for scope, instructions, provenance, and limitations.

The manuscript is titled **AUDIOS: An Interpretable Framework for Global Catchment Classification Based on Hydrological Signatures** and is under revision at Water Resources Research. No publication DOI is asserted here.

## Earlier demonstration materials

The root-level CSV and MATLAB/Python demos below predate this revision package and are retained unchanged. They illustrate signature calculation, FCM classification, CART rule extraction, and RF extrapolation. They have not been validated here as an end-to-end reproduction of the current revised manuscript. For revision-specific figures and evaluation results, use the package linked above.

## Repository Contents

This repository is organized into root files and two main demo folders (MATLAB and Python implementations).

- **HS_MC_tick.csv**  
  Pre-computed data for 1,017 minimally disturbed catchments:  
  - 8 hydrological signatures  
  - Fuzzy membership coefficients (for each class)  
  - Final class labels (based on highest membership)  
  → Quick way to explore AUDIOS results without running any code.

- **demoMAT/** — MATLAB implementation for signature computation and class assignment  
  - `main.m` — Entry script with examples: single catchment classification and batch processing  
  - `demoData/` — Sample input data (e.g., Basin_ID1.csv, multipleBasin.mat)  
  - `function/` — Core functions for computing hydrological signatures  
    - `compute_all_signatures.m`  
    - `compute_cr1.m`, `compute_dh5.m`, `compute_dl18.m`, etc.

- **demoPY/** — Python implementation for CART rule extraction and RF extrapolation  
  - `CART_RF.ipynb` — Jupyter notebook for training CART (rules) and Random Forest (global prediction + feature importance)  
  - `demoData/` — Intermediate CSV files (e.g., FSWithMCAbove0.5.csv, TicksWithMCAbove0.5.csv)

See [How to Use AUDIOS Catchment Classification](#how-to-use-audios-catchment-classification) below for quick start instructions.



## How to Use AUDIOS Catchment Classification

### 1. Quick Use: Assign Classes from Your Own Observed Data

To classify any catchment using your observed hydrological data with the AUDIOS system:

- Download only the `demoMAT` folder from this repository.
- Open MATLAB and navigate to the `demoMAT` directory.
- Run `main.m`.

The script includes ready-to-use examples:
- Example 1: Load data for a single catchment, compute signatures, and assign its AUDIOS class.
- Example 2: Batch process multiple catchments and assign classes for all at once.

→ No model training required — just run the script and get the class labels in seconds!

### 2. Explore the Earlier Demonstration Results

- **Fastest way** — Use the pre-computed results:  
  Open `HS_MC_tick.csv` (in the root directory) with Excel, Python (pandas), or any CSV reader.  
  It contains:
  - 1,017 minimally disturbed catchments
  - 8 hydrological signatures
  - Fuzzy membership coefficients
  - Final class labels (based on highest membership)

- **Earlier raw-data workflow outline (not a verified full reproduction of the revised manuscript)**:
  1. Download the Caravan dataset (Kratzert et al., 2023).  
  2. Use the MATLAB functions in `demoMAT/function/` (e.g., `compute_all_signatures.m`) to calculate hydrological signatures.  
  3. Perform Fuzzy C-Means (FCM) clustering with the parameters from the paper.  
  → This is a workflow outline; additional settings and the relevant data are required.

- **Reproduce explicit rules and RF model**:  
  Open `demoPY/CART_RF.ipynb` in Jupyter Notebook.  
  Run the cells to extract transparent decision rules and generate global extrapolation model and feature importance 


## Citation

Please cite **AUDIOS: An Interpretable Framework for Global Catchment Classification Based on Hydrological Signatures** using its publication details when available. During review, identify manuscript **2026WR044991** and the exact repository commit used. The manuscript number is not a DOI; no placeholder bibliographic entry is provided.

## Directory Structure

```
./
├── HS_MC_tick.csv
├── demoMAT/
│   ├── main.m
│   ├── demoData/
│   │   ├── Basin_ID1.csv
│   │   ├── multipleBasin.mat
│   ├── function/
│   │   ├── classify_by_tree.m
│   │   ├── compute_all_signatures.m
│   │   ├── compute_cr1.m
│   │   ├── compute_dh5.m
│   │   ├── compute_dl18.m
│   │   ├── compute_fh3.m
│   │   ├── compute_ma2.m
│   │   ├── compute_ra1_ra3.m
│   │   ├── compute_ta2.m
├── demoPY/
│   ├── CART_RF.ipynb
│   ├── demoData/
│   │   ├── FSWithMCAbove0.5.csv
│   │   ├── MCAbovePoint5_BS2Tick.csv
│   │   ├── TicksWithMCAbove0.5.csv
```

 
## License
It is licensed under CC BY-NC-SA 4.0. See [LICENSE](LICENSE) for details.
