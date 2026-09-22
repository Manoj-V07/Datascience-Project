import pandas as pd
import numpy as np

def allocate_proportional(demands, inventory, resources, time_windows, hubs):
    """
    Naively allocates inventory proportionally based on demand across zones.
    If multiple hubs exist, treats all hubs as a single pooled inventory (simplified).
    """
    allocations = []
    
    # We will track remaining pooled inventory over time
    current_inventory = {}
    for r in resources:
        r_name = r.split("_")[0]
        col_name = f'{r_name}_Opening_Inventory' if r_name != 'Shelter' else f'{r_name}_Opening_Capacity'
        current_inventory[r] = inventory.loc[inventory['Hours_Since_Disaster'] == 0, col_name].sum()
    
    # Aggregate demand by time and zone
    for t in time_windows:
        period_demands = demands[demands['Hours_Since_Disaster'] == t]
        
        for r in resources:
            r_name = r.split("_")[0]
            total_period_demand = period_demands[f'Predicted_{r}'].sum()
            
            for _, row in period_demands.iterrows():
                zone_demand = row[f'Predicted_{r}']
                if total_period_demand > 0 and current_inventory[r] > 0:
                    # Proportion of demand * total inventory, capped at demand
                    proportion = zone_demand / total_period_demand
                    allocated = min(zone_demand, proportion * current_inventory[r])
                else:
                    allocated = 0
                
                # Assume assigned to the first hub for simplicity in the baseline
                hub_id = hubs[0]
                unmet = zone_demand - allocated
                
                # Decrement inventory pool
                current_inventory[r] -= allocated
                
                allocations.append({
                    'Assessment_ID': row['Assessment_ID'],
                    'Hours_Since_Disaster': t,
                    'Hub_ID': hub_id,
                    'Resource': r_name,
                    'Predicted_Demand': zone_demand,
                    'Allocated': allocated,
                    'Unmet': unmet,
                    'Strategy': 'Baseline'
                })
                
    return pd.DataFrame(allocations)
