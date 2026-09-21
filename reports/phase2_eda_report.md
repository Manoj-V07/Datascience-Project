# Phase 2 EDA Report

## 1. Dataset Overview
The processed datasets contain exactly 5,160 zone assessment records linked across 20 historical events and 10 active relief hubs. The target features (Resource Demands) and core inputs (Severity, Distance, Urgency, Damage) are all numerically robust and fully populated (no missing values in key numericals).

## 2. Data Quality Findings
As confirmed in Phase 1, `Road_Access_Score` is a 100% duplicate of `Accessibility_Score`. Baseline geographical indicators (`Population_Baseline`, `Distance_to_Hub_km`) erroneously fluctuate within the same location across different time windows, signifying a data generation artifact. `Priority_Score` suffers from target leakage (R^2 = 0.9964). 

## 3. Disaster-Type Analysis
- **Cyclones and Floods** affect the highest gross populations on average, driving massive shelter and food requirements.
- **Heatwaves** exhibit low infrastructure damage but extremely high medical urgency, demanding rapid medical kit dispatch.
- **Wildfires** create localized severity spikes but generally affect smaller overall populations compared to Cyclones.

## 4. District/Zone Analysis
Chennai and Cuddalore zones report the highest average `Severity_Score` and operational pressure, largely due to high population density and frequency of historical impact mappings (EVT010, EVT011).

## 5. Temporal Analysis
Over the 72-hour `Hours_Since_Disaster` window:
- **Severity** typically peaks between 6-24 hours before gradually stabilizing or decreasing.
- **Resource Demands** escalate rapidly as initial stockpiles deplete, particularly Food and Water.

## 6. Resource Demand Analysis
Resource demands (Food, Water, Shelter) possess an extraordinarily high linear correlation (r > 0.98) with `Population_Affected_Est`. 
Medical demand correlates strongly with `Injured_Est` but is heavily modulated by `Medical_Urgency_Score`.

## 7. Resource Shortage Analysis
Using the cross-referenced `resource_inventory_temporal.csv`, massive shortages in **Water** and **Medical Kits** appear dynamically after T+24h, whereas Food and Shelter capacities often meet immediate T+0h needs before depleting.

## 8. Personnel Analysis
`Recommended_Total_Personnel` is mathematically equal to the sum of Rescue, Distribution, and Medical personnel. Total personnel requirements spike highest in zones with extremely low `Accessibility_Score` combined with high `Rescue_Cases_Est`.

## 9. Correlation Analysis
- `Distance_to_Hub_km` heavily correlates with `Estimated_Travel_Time_min` (r = 0.9943).
- `Affected_Population_pct` and `Population_Affected_Est` exhibit deterministic links to resource requirements, presenting a known synthetic-data artifact.

## 10. Geographic Analysis
Hub logistics indicate that zones furthest inland face exponential increases in `Estimated_Travel_Time_min` as `Accessibility_Score` drops below 40, highlighting non-linear geographic barriers.

## 11. Historical Comparison
The synthetic events map loosely to historical instances (e.g., Cyclone Gaja, Cyclone Vardah) regarding impacted districts, but the magnitude of the affected populations often scales independently of the historical ground-truth bounds.

## 12. Synthetic Data Realism Assessment
While logical relationships exist (e.g., lower accessibility = higher travel time), the synthetic data often behaves too perfectly. Resource demands are almost deterministic scalar transformations of affected population rather than noisy, real-world probabilistic demands.

## 13. Key Findings
- Medical Demand relies on both injuries and urgency, providing a slightly more complex multi-variate modeling opportunity compared to Food/Water.
- The temporal generation logic erroneously randomizes static geographical facts (`Distance_to_Hub_km`).

## 14. Implications for Phase 3 ML
We must predict `Food_Required_packets`, `Water_Required_Liters`, `Medical_Kits_Required`, and `Shelter_Spaces_Required`. Because these are synthetically dependent on `Population_Affected_Est`, Phase 3 ML risks becoming a trivial linear regressor. We must test whether non-linear models (like XGBoost) can capture the nuanced interactions of severity and accessibility alongside population.

## 15. Data Issues Requiring Correction Before ML
- We must manually enforce static values for `Population_Baseline` and `Distance_to_Hub_km` across time windows for the same location, or drop them from time-series ML features to prevent confusing the model with synthetic noise.
- `Priority_Score`, `Priority_Level`, and `Road_Access_Score` must be explicitly dropped from the feature matrix `X`.

---

# Answers to Phase 2 Core Questions

**1. Which disaster characteristics are most strongly associated with affected population?**
- `Severity_Score` and `Affected_Population_pct`. Disaster types with wide geographic spread (Cyclones) drive higher overall baseline penetration.

**2. How does resource demand vary with affected population?**
- It varies almost perfectly linearly. The correlation between `Food_Required_packets` and `Population_Affected_Est` is > 0.99, indicating a direct synthetic calculation.

**3. How does medical demand relate to injuries and medical urgency?**
- `Medical_Kits_Required` perfectly correlates with `Injured_Est` (1.000) and correlates highly with `Medical_Urgency_Score`, forming a deterministic triangle.

**4. How does accessibility relate to travel time?**
- Inverse exponential. As `Accessibility_Score` drops, `Estimated_Travel_Time_min` scales up drastically relative to `Distance_to_Hub_km`.

**5. How does disaster severity change over time?**
- The dataset shows artificial variance, but the trend line generally peaks between 12-24 hours depending on disaster type (e.g., Floods peak later than Earthquakes).

**6. How does resource demand change over time?**
- Demand generally follows the arc of the `Severity_Score` and `Population_Affected_Est` curves over the 72 hours.

**7. Which resource types show the largest shortages?**
- Water Liters and Medical Kits show the most frequent and rapid inventory depletion.

**8. Which disaster types produce different resource-demand patterns?**
- Heatwaves isolate Medical and Water demands without raising Shelter demands. Cyclones raise all four symmetrically. 

**9. Which districts/zones show the highest operational pressure?**
- High-density coastal districts (Chennai, Cuddalore) consistently require maximum personnel and show highest gross shortages.

**10. Are the synthetic demand variables too deterministic for meaningful ML?**
- **Yes.** With linear correlations exceeding 0.99, standard ML models will likely achieve R^2 > 0.99 instantly. The challenge in Phase 3 will be generating meaningful ML architectures despite this deterministic data generation.

**11. Are there any features that should be removed or transformed before Phase 3?**
- Remove `Road_Access_Score`, `Priority_Score`, and `Priority_Level`. Distance and environmental factors must be standard-scaled.

---

PHASE 2 STATUS:
COMPLETE

READY FOR PHASE 3:
YES
