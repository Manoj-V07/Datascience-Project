# ML Leakage & Derived Features Report

## Derived Features Check
- **Recommended_Total_Personnel**: Exact match with sum of components in 100.00% of rows.
- **Priority_Level**: Likely a binned output of Priority_Score.

## Leakage Risks for Demand Targets
| Feature | Target | Leakage Risk | Recommendation |
| ------- | ------ | ------------ | -------------- |
| Population_Affected_Est | Food_Required_packets | High | Possible derived shortage |
| Rescue_Cases_Est | Food_Required_packets | High | Possible derived shortage |
| Estimated_Relief_Time_min | Food_Required_packets | High | Possible derived shortage |
| Water_Required_Liters | Food_Required_packets | High (Co-target) | Predict together or drop |
| Medical_Kits_Required | Food_Required_packets | High (Co-target) | Predict together or drop |
| Shelter_Spaces_Required | Food_Required_packets | High (Co-target) | Predict together or drop |
| Required_Rescue_Personnel | Food_Required_packets | High | Possible derived shortage |
| Required_Distribution_Personnel | Food_Required_packets | High | Possible derived shortage |
| Recommended_Total_Personnel | Food_Required_packets | High | Possible derived shortage |
| Population_Affected_Est | Water_Required_Liters | High | Possible derived shortage |
| Rescue_Cases_Est | Water_Required_Liters | High | Possible derived shortage |
| Estimated_Relief_Time_min | Water_Required_Liters | High | Possible derived shortage |
| Food_Required_packets | Water_Required_Liters | High (Co-target) | Predict together or drop |
| Medical_Kits_Required | Water_Required_Liters | High (Co-target) | Predict together or drop |
| Shelter_Spaces_Required | Water_Required_Liters | High (Co-target) | Predict together or drop |
| Required_Rescue_Personnel | Water_Required_Liters | High | Possible derived shortage |
| Required_Distribution_Personnel | Water_Required_Liters | High | Possible derived shortage |
| Recommended_Total_Personnel | Water_Required_Liters | High | Possible derived shortage |
| Population_Affected_Est | Medical_Kits_Required | High | Possible derived shortage |
| Rescue_Cases_Est | Medical_Kits_Required | High | Possible derived shortage |
| Estimated_Relief_Time_min | Medical_Kits_Required | High | Possible derived shortage |
| Food_Required_packets | Medical_Kits_Required | High (Co-target) | Predict together or drop |
| Water_Required_Liters | Medical_Kits_Required | High (Co-target) | Predict together or drop |
| Shelter_Spaces_Required | Medical_Kits_Required | High (Co-target) | Predict together or drop |
| Required_Rescue_Personnel | Medical_Kits_Required | High | Possible derived shortage |
| Required_Distribution_Personnel | Medical_Kits_Required | High | Possible derived shortage |
| Recommended_Total_Personnel | Medical_Kits_Required | High | Possible derived shortage |
| Population_Affected_Est | Shelter_Spaces_Required | High | Possible derived shortage |
| Rescue_Cases_Est | Shelter_Spaces_Required | High | Possible derived shortage |
| Estimated_Relief_Time_min | Shelter_Spaces_Required | High | Possible derived shortage |
| Food_Required_packets | Shelter_Spaces_Required | High (Co-target) | Predict together or drop |
| Water_Required_Liters | Shelter_Spaces_Required | High (Co-target) | Predict together or drop |
| Medical_Kits_Required | Shelter_Spaces_Required | High (Co-target) | Predict together or drop |
| Required_Rescue_Personnel | Shelter_Spaces_Required | High | Possible derived shortage |
| Required_Distribution_Personnel | Shelter_Spaces_Required | High | Possible derived shortage |
| Recommended_Total_Personnel | Shelter_Spaces_Required | High | Possible derived shortage |
