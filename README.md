# SAFI — SpectroAgro Fusion AI Index

SAFI (SpectroAgro Fusion AI) is a Geo-AI based Digital Soil Laboratory designed to estimate key soil laboratory properties and derive a Land Suitability Index (LSI) directly from geographic coordinates.

The platform combines remote sensing, climate, terrain, ecological, and soil-context variables to estimate agricultural potential in locations where no field laboratory measurements are available.

SAFI is intended for exploratory agricultural assessment, land comparison, sustainability studies, and early-stage planning. It is not intended to replace laboratory analysis or regulatory soil surveys.

---

# Project Objective

The objective of SAFI is to create a scientifically defensible inference system capable of predicting soil properties in places where direct measurements do not exist.

Instead of relying on a single variable, the system integrates many environmental signals related to soil formation and land productivity.

The final output is a continuous Land Suitability Index ranging from 0 to 1, representing the relative agricultural suitability of the selected location.

---

# Reference Dataset

SAFI was developed using the unified dataset `safi_v1_universe.csv`, which contains approximately:

- 4,416 georeferenced soil observations
- 159 environmental variables
- Laboratory targets including:
  - CECPH7
  - TOTC
  - ORGC
  - BDFIOD
  - Derived ORGM

The environmental variables used in SAFI represent long-term conditions covering the period from 2001 to 2017.

All remote sensing, climate, hydrological, and ecological features were aggregated across this time span in order to describe the stable environmental context of each soil sample and reduce short-term variability.

---

# Environmental Data Sources

| Source | Variables | Purpose |
|--------|--------|--------|
| WoSIS | Measured soil laboratory observations | Primary source for training and validation targets |
| ERA5 | Temperature, precipitation, wind, evaporation, radiation, soil moisture | Long-term climate and energy balance |
| CHELSA | Bioclimatic variables | Climatic gradients and seasonality |
| GLDAS | Root-zone and multi-depth soil moisture | Hydrological context and water availability |
| MODIS / Landsat | NDVI, NDMI, SAVI, NPP, burn frequency | Vegetation productivity and land-surface response |
| Digital Elevation Models | Elevation, aspect, curvature, TPI | Topographic controls on soil formation |

---

# Processing Workflow

1. The user selects a location on the map.
2. SAFI extracts the nearest environmental feature vector from the reference dataset.
3. The feature vector is validated against the SAFI schema.
4. The inference engine predicts the main soil variables.
5. Uncertainty intervals are calculated for every variable.
6. The Land Suitability Index is derived from the predicted variables.
7. The system reports results, confidence, and warnings.

---

# Model Training and Validation

All SAFI models were trained using strict spatial cross-validation rather than random train-test splits.

The system uses hierarchical spatial blocking and GroupKFold validation to ensure that nearby points are not simultaneously used for training and testing.

| Target | Model | Validation Result |
|--------|--------|--------|
| CECPH7 | Gradient Boosting Quantile Regression + Conformal Calibration | RMSE ≈ 10.9, MAE ≈ 5.6, Spearman ≈ 0.81 |
| TOTC | Regime-Adaptive Quantile Regression | RMSE ≈ 65–70, Spearman ≈ 0.75–0.80 |
| ORGC | LightGBM + Mondrian CV+ Intervals | RMSE ≈ 35, Spearman ≈ 0.72 |
| BDFIOD | Bayesian Ridge + Residual Scale Model | RMSE ≈ 0.28, Spearman ≈ 0.62 |

Prediction intervals were calibrated to provide approximately 80% spatial coverage, ensuring that SAFI communicates uncertainty rather than only a single deterministic value.

---

# Predicted Soil Variables

| Variable | Meaning | Function in SAFI |
|--------|--------|--------|
| CECPH7 | Cation exchange capacity at pH 7 | Main positive soil fertility driver |
| TOTC | Total organic carbon | Represents overall soil fertility |
| ORGC | Organic carbon | Supporting carbon modifier |
| BDFIOD | Bulk density of fine earth | Limiting physical factor |
| ORGM | Derived soil organic matter | Diagnostic only |

---

# Land Suitability Index (LSI)

SAFI converts each predicted soil property into a percentile score relative to the reference population.

These percentile scores are then combined using a limiting-factor logic:

```text
PositiveScore = mean(Percentile(CECPH7), Percentile(TOTC))
ConstraintFactor = sqrt(Percentile(ORGC) × (1 - Percentile(BDFIOD)))
LSI = PositiveScore × ConstraintFactor
```

High CECPH7 and TOTC increase suitability because they indicate better nutrient retention and higher fertility.

High BDFIOD reduces the final score because dense soil limits root growth and water movement.

| LSI Range | Interpretation |
|--------|--------|
| 0.00 – 0.20 | Very low suitability |
| 0.20 – 0.40 | Low suitability |
| 0.40 – 0.60 | Moderate suitability |
| 0.60 – 0.80 | High suitability |
| 0.80 – 1.00 | Excellent suitability |

SAFI reports three forms of the index:

- Conservative LSI: based on lower uncertainty bounds
- Expected LSI: based on central predictions
- Opportunity LSI: based on upper uncertainty bounds

---

# Future Development

The current SAFI version operates in an offline mode using precomputed environmental features extracted from the reference dataset.

The next development stage currently in progress is the transition toward a full dynamic inference system.

In the future, when a user selects a point on the map, SAFI will automatically retrieve the complete environmental context of that location in real time.

This future workflow will extract all relevant variables directly from their original sources, including:

- Current and historical climate variables from ERA5 and CHELSA
- Satellite remote sensing indicators such as NDVI, NDMI and SAVI
- Soil moisture and hydrological indicators from GLDAS
- Topographic and terrain characteristics from digital elevation models
- Land cover, lithology and ecological variables

These dynamically extracted variables will then be passed directly into the existing SAFI prediction models.

This approach is expected to produce more accurate, location-specific and up-to-date soil predictions and Land Suitability Index estimates than the current nearest-neighbor method.

Another major future objective is to continuously improve the accuracy and scientific robustness of SAFI by expanding the soil laboratory database. The project aims to collect and integrate substantially more real soil laboratory analyses from as many countries and regions as possible. Each additional national dataset will provide new examples of local soil conditions, allowing the models to better represent geographic variability, reduce uncertainty, and improve prediction quality in underrepresented areas.

The long-term goal is for SAFI to evolve into a progressively self-improving global soil intelligence platform. As more countries contribute laboratory observations, the system will be retrained to increase the precision of the current soil-property predictions and to support additional laboratory variables beyond the current set, including new chemical, physical, and fertility-related soil indicators.

Future versions of SAFI are also intended to include a more advanced sustainability and agricultural potential index. Instead of relying only on the currently predicted soil variables, the future index will integrate a broader set of environmental, climatic, hydrological, ecological, and land management factors. This richer information will allow SAFI to provide a more comprehensive evaluation of long-term agricultural sustainability, crop suitability, environmental risk, and land-development potential.

---

# About the Researcher

SAFI was developed by Hussein Hadi Abbas, a Surveying Engineer graduated from the Middle Technical University, Iraq, with a research background in remote sensing, GIS, and AI-driven geospatial analysis. He also holds a Master’s degree in Map (Geomatics) Engineering from Erciyes University, Türkiye.

The idea behind SAFI began in 2022 during a discussion about a privately owned agricultural farm. The central question was whether it would be possible to infer the essential characteristics of land without relying entirely on expensive and time-consuming laboratory testing.

The discussion gradually evolved into a broader scientific problem: if a person intends to purchase or cultivate a piece of land, what are the minimum indicators required to determine whether that land is suitable for agriculture? Could soil laboratory properties be estimated from satellite observations, climate, terrain, and environmental context? And could these estimates be transformed into a simple, interpretable indicator expressing the overall suitability of the land?

From these questions, SAFI emerged as an attempt to create a Digital Soil Laboratory and a Land Suitability Index capable of translating complex environmental information into practical guidance for agricultural planning and decision-making.

---

# Scientific Limitations

- The current version uses nearest-neighbor lookup from the reference dataset.
- The platform does not yet use live raster layers or real-time satellite data.
- Prediction uncertainty increases in rare or unsupported environments.
- Locations outside the environmental domain of the training dataset may produce lower-confidence results.
- SAFI is intended for screening and comparison, not as a replacement for field sampling and laboratory measurements.

## Citation

If you use this project in research, publications, software, presentations, or derivative work, you must credit:

Hussein Hadi Abbas. SpectroAgro Fusion AI Index (SAFI), 2026.
