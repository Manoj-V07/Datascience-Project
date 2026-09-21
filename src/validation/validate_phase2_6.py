import pandas as pd
import numpy as np
import sys
import os

project_dir = r"d:\Data-Science-Project"
v2_6_dir = os.path.join(project_dir, "data", "processed", "v2_6")

def validate():
    zones = pd.read_csv(os.path.join(v2_6_dir, "zone_assessments_v2_6.csv"))
    inv = pd.read_csv(os.path.join(v2_6_dir, "resource_inventory_temporal_v2_6.csv"))
    
    errors = []
    
    # 1. Target Ranges (Non-negative)
    for col in ['Food_Required_packets', 'Water_Required_Liters', 'Shelter_Spaces_Required']:
        if (zones[col] < 0).any():
            errors.append(f"Negative values found in {col}")
            
    # 2. Inventory Conservation and Non-negative
    for res in ['Food', 'Water', 'Medical', 'Shelter']:
        if res == 'Shelter':
            res_open = f"{res}_Opening_Capacity"
        else:
            res_open = f"{res}_Opening_Inventory"
            
        if (inv[f"{res}_Remaining"] < 0).any():
            errors.append(f"Negative remaining inventory for {res}")
            
        diff = inv[res_open] - inv[f"{res}_Allocated"] - inv[f"{res}_Remaining"]
        if (diff.abs() > 0.01).any():
            errors.append(f"Inventory conservation failed for {res}")
            
        if (inv[f"{res}_Allocated"] > inv[res_open]).any():
            errors.append(f"Allocated exceeds Opening for {res}")
            
    # 3. Static Field Stability
    groups = zones.groupby(['Event_ID', 'District', 'Response_Zone'])
    if (groups['Population_Baseline'].std().fillna(0) > 0).any():
        errors.append("Population_Baseline is not static")
    if (groups['Distance_to_Hub_km'].std().fillna(0) > 0).any():
        errors.append("Distance_to_Hub_km is not static")
        
    # 4. Simulation Presence
    sims = zones['Simulation_ID'].nunique()
    if sims != 5:
        errors.append(f"Expected 5 simulations, found {sims}")
        
    # 5. Domain Constraints
    if (zones['Population_Affected_Est'] > zones['Population_Baseline']).any():
        errors.append("Affected Population > Baseline")
    if (zones['Fatalities_Est'] > zones['Population_Affected_Est']).any():
        errors.append("Fatalities > Affected")
        
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)
    else:
        print("VALIDATION SUCCESSFUL: All constraints passed.")
        sys.exit(0)

if __name__ == "__main__":
    validate()
