# Data dictionary

All CSVs are UTF-8 with headers. Read floating-point inputs with full precision (the scripts use pandas `float_precision="round_trip"`). The input hashes in `provenance.json` refer to exact file bytes.

## External benchmark files

| File / fields | Meaning |
|---|---|
| `panels_ab_separation.csv`: `dataset`, `feature`, `comparator`, `metric` | Dataset, native feature code, climate comparator (`Koppen` or `Knoben`), and separation metric (`silhouette`, `calinski_harabasz`, `gap`) |
| `n` | Evaluated catchment count for this feature |
| `continuous_fcm_value`, `comparator_value` | Archived separation scores for AUDIOS and the comparator |
| `delta_continuous_minus_comparator`, `direction`, `winner` | Difference, sign, and scheme favored by the difference; no significance test is implied |
| `panel_c_four_line_values.csv`: `audios_variant`, `baseline`, `baseline_variant`, `label` | Exact variants and legend label for each plotted comparison |
| `audios_pooled_rmse`, `baseline_pooled_rmse` | Pooled RMSE in the feature's native units (Table S4 definitions and S6–S8 reference tables) |
| `relative_rmse_improvement_percent` | `100 * (baseline - AUDIOS) / baseline`, percent |
| `panel_c_summary.csv` | Feature count, positive-improvement count, and median percent improvement for each curve |
| `feature_labels.csv` | Dataset-specific ordering and conversion from native `source_feature` codes to figure `label` |
| `signature_definitions.csv` | Visible Table S4 definition and unit text; some rows describe several feature codes together |
| `TableS6_reference.csv`, `TableS7_reference.csv`, `TableS8_reference.csv` | Visible SI table cells at their published display precision; values are not substituted for unrounded inputs |

`reconstruction_summary.csv` has one row per dataset / feature / method / variant (245 rows). `target_n` is the denominator. `pooled_rmse`, `mae`, and `median_absolute_error` use feature-native units. `legacy_mean_pointwise_rmse` is a legacy column equal to MAE, **not pooled RMSE**. `mean_used_donor_n` describes the used donors; `minimum_available_same_class_donor_n` is availability, not the K5 count.

External `method` codes are `Continuous_FCM` (AUDIOS), `Koppen`, and `Knoben`. `ClassMean` is the class-mean estimate; `MatchedK5` uses up to five nearest donors within the class. There is no Köppen K5 result in the five-method table.

## Daily score files

| Field | Meaning |
|---|---|
| `window` | `subsequent_2016_2020` (main evaluation) or `unified_1981_2015` (common-period sensitivity) |
| `basin_id` | Archived catchment identifier; used for pairing and deterministic ordering |
| `fold_id` | Held-out cross-validation fold, where present |
| `primary` | Archived binary membership-subset flag (1: member of the 932-catchment primary subset; 0: member of the additional 85-catchment subset). This is not an AUDIOS class label; the plots use both subsets |
| `method` | Method code; mapping below |
| `donor_count` | Archived donor count for the target/method, where present |
| `valid_days` | Number of valid daily pairs used for that score; equality is required within a paired comparison |
| `NSE`, `KGE`, `NRMSE` | Dimensionless archived efficiency/error scores; plots use NSE and KGE. NRMSE is RMSE divided by the observed flow range on the valid dates; it is retained as auxiliary data and is not recalculated from discharge here |
| `plotted_metric` | Which subplot uses this row (`NSE` or `KGE`); thus the same target/method score record occurs twice |
| `comparison` | Paired-method comparison identifier, in paired source files |

| Archived method code | Display label |
|---|---|
| `Koppen_Class_All` | Köppen |
| `Knoben_Class_All` | Knoben |
| `Continuous_FCM_Class_All` | AUDIOS |
| `Knoben_K5` | KnobenK5 |
| `RF_Signature_K5` | AUDIOSK5 |

`boxplot_source_values.csv` uses method-specific valid dates and the 626-catchment cohort. `paired_source_values.csv` uses common valid dates within each K5 pair and the 627-catchment cohort. Do not combine these files as independent observations or drop the pair-specific date restriction.

`boxplot_statistics.csv` records `n`, median, 5th percentile (`p05`), quartiles (`q1`, `q3`), and whiskers (`whislo`, `whishi`, 1.5 interquartile ranges). Outliers are drawn separately without changing their scores.

`plotted_statistics.csv` records the median of paired AUDIOSK5 minus KnobenK5 differences, percent of catchments with a strictly positive difference (ties are not wins), and each method's 5th percentile. Percentiles use NumPy's default linear interpolation.

`histogram_bins.csv` gives raw-score `left_edge`, `right_edge`, and count. Bins are left-inclusive/right-exclusive, except the last bin includes the right edge (NumPy convention). Widths are equal only after the symmetric-log transform. For each metric, identical edges are used in the two periods and counts sum to 627.
