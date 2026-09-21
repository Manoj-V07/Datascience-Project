# Feature Redundancy Report

## Accessibility_Score vs Road_Access_Score
- **Correlation**: 1.0000
- **Mean Absolute Difference**: 0.0000
- **Identical values fraction**: 1.0000

**Recommendation**: MERGE THEM or KEEP ONLY ONE (They are nearly identical).

## Highly Correlated Numeric Features (|corr| >= 0.90)
| Feature A | Feature B | Correlation | Recommendation |
| --------- | --------- | ----------: | -------------- |
| Distance_to_Hub_km | Estimated_Travel_Time_min | 0.9943 | Investigate |
| Population_Affected_Est | Rescue_Cases_Est | 0.9137 | Investigate |
| Population_Affected_Est | Estimated_Relief_Time_min | 0.9803 | Investigate |
| Population_Affected_Est | Food_Required_packets | 0.9970 | Investigate |
| Population_Affected_Est | Water_Required_Liters | 0.9951 | Investigate |
| Population_Affected_Est | Medical_Kits_Required | 0.9887 | Investigate |
| Population_Affected_Est | Shelter_Spaces_Required | 0.9913 | Investigate |
| Population_Affected_Est | Required_Rescue_Personnel | 0.9137 | Investigate |
| Population_Affected_Est | Required_Distribution_Personnel | 0.9968 | Investigate |
| Population_Affected_Est | Recommended_Total_Personnel | 0.9575 | Investigate |
| Injured_Est | Required_Medical_Personnel | 1.0000 | Investigate |
| Severity_Score | Medical_Urgency_Score | 0.9074 | Investigate |
| Severity_Score | Priority_Score | 0.9118 | Investigate |
| Infrastructure_Damage_Score | Priority_Score | 0.9078 | Investigate |
| Accessibility_Score | Road_Access_Score | 1.0000 | Investigate |
| Medical_Urgency_Score | Priority_Score | 0.9682 | Investigate |
| Rainfall_mm | River_Level_m | 0.9245 | Investigate |
| Wind_Speed_kmph | Storm_Surge_m | 0.9174 | Investigate |
| Rescue_Cases_Est | Estimated_Relief_Time_min | 0.9370 | Investigate |
| Rescue_Cases_Est | Food_Required_packets | 0.9424 | Investigate |
| Rescue_Cases_Est | Water_Required_Liters | 0.9155 | Investigate |
| Rescue_Cases_Est | Medical_Kits_Required | 0.9559 | Investigate |
| Rescue_Cases_Est | Shelter_Spaces_Required | 0.9536 | Investigate |
| Rescue_Cases_Est | Required_Rescue_Personnel | 1.0000 | Investigate |
| Rescue_Cases_Est | Required_Distribution_Personnel | 0.9408 | Investigate |
| Rescue_Cases_Est | Recommended_Total_Personnel | 0.9832 | Investigate |
| Estimated_Relief_Time_min | Food_Required_packets | 0.9854 | Investigate |
| Estimated_Relief_Time_min | Water_Required_Liters | 0.9743 | Investigate |
| Estimated_Relief_Time_min | Medical_Kits_Required | 0.9861 | Investigate |
| Estimated_Relief_Time_min | Shelter_Spaces_Required | 0.9870 | Investigate |
| Estimated_Relief_Time_min | Required_Rescue_Personnel | 0.9370 | Investigate |
| Estimated_Relief_Time_min | Required_Distribution_Personnel | 0.9850 | Investigate |
| Estimated_Relief_Time_min | Recommended_Total_Personnel | 0.9691 | Investigate |
| Food_Required_packets | Water_Required_Liters | 0.9933 | Investigate |
| Food_Required_packets | Medical_Kits_Required | 0.9958 | Investigate |
| Food_Required_packets | Shelter_Spaces_Required | 0.9975 | Investigate |
| Food_Required_packets | Required_Rescue_Personnel | 0.9424 | Investigate |
| Food_Required_packets | Required_Distribution_Personnel | 0.9996 | Investigate |
| Food_Required_packets | Recommended_Total_Personnel | 0.9753 | Investigate |
| Water_Required_Liters | Medical_Kits_Required | 0.9836 | Investigate |
| Water_Required_Liters | Shelter_Spaces_Required | 0.9838 | Investigate |
| Water_Required_Liters | Required_Rescue_Personnel | 0.9155 | Investigate |
| Water_Required_Liters | Required_Distribution_Personnel | 0.9952 | Investigate |
| Water_Required_Liters | Recommended_Total_Personnel | 0.9552 | Investigate |
| Medical_Kits_Required | Shelter_Spaces_Required | 0.9972 | Investigate |
| Medical_Kits_Required | Required_Rescue_Personnel | 0.9559 | Investigate |
| Medical_Kits_Required | Required_Distribution_Personnel | 0.9961 | Investigate |
| Medical_Kits_Required | Recommended_Total_Personnel | 0.9877 | Investigate |
| Shelter_Spaces_Required | Required_Rescue_Personnel | 0.9536 | Investigate |
| Shelter_Spaces_Required | Required_Distribution_Personnel | 0.9961 | Investigate |
| Shelter_Spaces_Required | Recommended_Total_Personnel | 0.9822 | Investigate |
| Required_Rescue_Personnel | Required_Distribution_Personnel | 0.9408 | Investigate |
| Required_Rescue_Personnel | Recommended_Total_Personnel | 0.9832 | Investigate |
| Required_Distribution_Personnel | Recommended_Total_Personnel | 0.9754 | Investigate |
