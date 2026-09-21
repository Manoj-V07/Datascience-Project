# Synthetic Generation Methodology

This document outlines the multivariate logic used to regenerate the synthetic resource demands in Phase 2.6 to prepare the dataset for Machine Learning.

## Food Demand Generation
**Formula**: 
`Population_Affected_Est * 2.5 * (1 + (Severity_Score / 100) * 0.3) * Disaster_Modifier * Time_Modifier * Noise`
- **Base Rate**: 2.5 packets per affected person.
- **Severity Modifier**: Up to +30% demand for extreme severity.
- **Disaster Modifier**: Cyclones (+20%), Floods (+15%).
- **Time Modifier**: +10% demand after T+24h as personal stockpiles deplete.
- **Noise**: Log-normal stochastic noise ($\sigma = 0.20$).
- **Rationale**: Breaks deterministic population links by factoring in the disaster's physical severity and geographical impact type.

## Water Demand Generation
**Formula**: 
`Population_Affected_Est * 4.0 * (1 + (Infrastructure_Damage_Score / 100) * 0.4) * Disaster_Modifier * Time_Modifier * Noise`
- **Base Rate**: 4.0 liters per affected person.
- **Infrastructure Modifier**: Up to +40% demand when infrastructure is destroyed (burst pipes, lost access).
- **Disaster Modifier**: Heatwaves (+50%), Droughts (+30%).
- **Time Modifier**: +20% demand after T+24h.
- **Noise**: Log-normal stochastic noise ($\sigma = 0.25$).
- **Rationale**: Real-world water demand is highly susceptible to heat and infrastructure failure, making it distinct from food demand.

## Shelter Demand Generation
**Formula**: 
`Population_Affected_Est * 0.2 * (Infrastructure_Damage_Score / 100) * Disaster_Modifier * Noise`
- **Base Rate**: 0.2 spaces per affected person, scaled linearly by damage.
- **Infrastructure Modifier**: Direct scaling based on structural damage (0% damage = 0 shelter demand).
- **Disaster Modifier**: Earthquakes (+40%), Cyclones (+30%), Heatwaves (-90% as homes remain intact).
- **Noise**: Log-normal stochastic noise ($\sigma = 0.30$).
- **Rationale**: Shelter demand cannot simply scale with population; it strictly requires structural displacement.

## Temporal Inventory Model
Unlike the Phase 2 static expansion, `resource_inventory_temporal_v2_6.csv` tracks genuine physical consumption across 72 hours.
- For each time window (0h, 3h, 6h, 12h, 24h, 36h, 48h, 72h):
  - Demand is aggregated across all zones supplied by a single Hub.
  - `Allocated = min(Demand, Opening_Inventory)`
  - `Remaining_Inventory = Opening_Inventory - Allocated`
  - The `Remaining_Inventory` is passed forward to the next time window as its `Opening_Inventory`.
- **Result**: True shortages organically emerge when cumulative demand exceeds the physical Hub capacity. Negative inventory is strictly prohibited.
