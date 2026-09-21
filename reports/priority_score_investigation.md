# Priority Score Investigation

## Reverse-Engineering Priority_Score
- **R-squared**: 0.9964
- **Intercept**: 8.6034
- **Coefficients**:
  - Severity_Score: 0.2117
  - Medical_Urgency_Score: 0.3114
  - Infrastructure_Damage_Score: 0.2016
  - Accessibility_Score: -0.0785
  - Affected_Population_pct: 0.2199

## Conclusion
Priority_Score is **directly calculated** (or nearly so) from the existing columns via a linear formula. DO NOT USE AS ML TARGET. It constitutes target leakage and trivializes ML.