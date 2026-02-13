# AUDIOS-Catchment-Classification
Global hydrological catchment classification system (AUDIOS) based on hydrological signatures, Fuzzy C-Means clustering, CART rule extraction, and Random Forest extrapolation.
 

## Overview

This repository contains the code and processed data for the **AUDIOS** (Abundant, Unseasonal, Dry, Invariant, Ordinary, and Seasonal) global catchment classification system presented in the paper:

> **Beyond climate: A Fuzzy Clustering and Explainable AI Method for global natural catchment classification defined by hydrological signatures**  
> Authors: Xu Huan, et al.  
> Journal: (to be updated)  
> DOI: (to be updated once published)

AUDIOS is the first global catchment classification system derived **directly from observed hydrological signatures** rather than climate proxies. It uses:

- Fuzzy C-Means (FCM) clustering on 1,017 minimally disturbed catchments
- Classification and Regression Trees (CART) for transparent rule extraction
- Random Forest for global extrapolation to ungauged basins

It significantly outperforms the Köppen climate classification in hydrological signature separation and PUB (Predictions in Ungauged Basins) applications.

## Repository Contents

- `HS_MC_tick.csv`  
  → Processed data of the 1,017 minimally disturbed catchments, including:
  - 8 hydrological signatures
  - Fuzzy membership coefficients
  - Final hard class labels (highest membership)

- `CART_RF.ipynb`  
  → Scripts for training the CART model for extracting interpretable decision rules, and training the Random Forest classifier for feature importance

- `main.m`  
  → Standalone tool to assign catchment classes using observed data

 
 
