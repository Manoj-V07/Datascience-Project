# Phase 1 Final Decision

## KEEP
- `Accessibility_Score`, `Population_Affected_Est`, `Severity_Score`, `Medical_Urgency_Score`, `Infrastructure_Damage_Score`
- Geographic/Logistics: `Estimated_Travel_Time_min`, `Distance_to_Hub_km`, `Latitude`, `Longitude`
- All Base Environmental Factors (`Rainfall_mm`, `Wind_Speed_kmph`, etc.)
- All Identification Keys (`Event_ID`, `Location_ID`, `Hub_ID`, `Assessment_Window`)

## REMOVE FROM MODELING
- `Road_Access_Score` (Exact 100% duplicate of `Accessibility_Score`)

## DERIVED FEATURES
- `Priority_Score`: (Derived Feature / Decision Output; R² = 0.9964)
- `Priority_Level`: (Categorical derived from Priority_Score)
- `Recommended_Total_Personnel`: (Derived exactly from the sum of Required Personnel fields)

## FEATURES REQUIRING TRANSFORMATION
- ML inputs (Distances, Weather metrics) will require standard scaling during Phase 3, but raw forms are kept for Phase 2 EDA.

## FEATURES REQUIRING FURTHER INVESTIGATION
- `Population_Affected_Est`: Mark as high synthetic dependency. Must investigate target-generation logic to ensure it doesn't trivially leak into demand.
- Highly correlated pairs (e.g., `Distance_to_Hub_km` and `Estimated_Travel_Time_min`) to verify their distinct distributions during EDA.

## ML TARGET CANDIDATES
- `Food_Required_packets`
- `Water_Required_Liters`
- `Medical_Kits_Required`
- `Shelter_Spaces_Required`
*(Phase 2 EDA will determine whether their synthetic relationships are sufficiently meaningful for Phase 3.)*

## FEATURES NOT TO USE FOR ML
- `Priority_Score` (Target leakage)
- `Priority_Level` (Target leakage)
- `Recommended_Total_Personnel` (Post-allocation derivation)
- `Road_Access_Score` (Redundant)

## OPTIMIZATION INPUTS
- Target Demand variables (`Food`, `Water`, `Medical`, `Shelter`)
- Hub Inventory
- `Priority_Score` (as a weighting metric)
- `Recommended_Total_Personnel`
- `Estimated_Travel_Time_min` & `Distance_to_Hub_km`

## DATASETS VERIFIED
- `disaster_events.csv`, `historical_event_districts.csv`, `relief_hubs.csv`, `resource_inventory.csv`, `zone_assessments.csv`, `data_dictionary.csv`

## RAW DATA INTEGRITY
- Verified. Raw data under `data/raw/` remains completely unmodified.

## PHASE 2 READINESS
The project data foundation is clean and correctly documented. We are ready for Phase 2 EDA.
