import pandas as pd
import pulp
import os
import time

from model import build_optimization_model
from baseline import allocate_proportional
from validate_allocation import validate_allocations

def run_pipeline():
    project_dir = r"d:\Data-Science-Project"
    
    print("Loading data...")
    # Load ML Predictions
    preds = pd.read_csv(os.path.join(project_dir, "outputs", "phase3_1", "demand_predictions.csv"))
    
    # Load Priority and Travel info from Zone Assessments
    zones = pd.read_csv(os.path.join(project_dir, "data", "processed", "v2_6", "zone_assessments_v2_6.csv"))
    
    # Load Hub Information (Not used for direct mapping, optimizer chooses hub)
    # hubs_df = pd.read_csv(os.path.join(project_dir, "data", "raw", "relief_hubs.csv"))
    
    # Merge needed info into preds (Priority Level, Travel Time)
    preds = preds.merge(zones[['Assessment_ID', 'Priority_Score', 'Priority_Level', 'Estimated_Travel_Time_min', 'Distance_to_Hub_km']], on='Assessment_ID', how='left')
    
    # Loop over all events
    all_opt_results = []
    all_base_results = []
    
    events_to_process = preds['Event_ID'].unique()
    print(f"Processing {len(events_to_process)} events...")
    
    inventory = pd.read_csv(os.path.join(project_dir, "data", "processed", "v2_6", "resource_inventory_temporal_v2_6.csv"))
    
    for test_event in events_to_process:
        demands = preds[preds['Event_ID'] == test_event].copy()
    
        t0_inventory = inventory[(inventory['Event_ID'] == test_event) & (inventory['Hours_Since_Disaster'] == 0)].copy()
    
        resources = ['Food_Required_packets', 'Water_Required_Liters', 'Medical_Kits_Required', 'Shelter_Spaces_Required']
        r_names = [r.split("_")[0] for r in resources]
        
        time_windows = sorted(demands['Hours_Since_Disaster'].unique().tolist())
        hub_ids = t0_inventory['Hub_ID'].unique().tolist()
        
        print(f"Building optimization model for {test_event} with {len(hub_ids)} hubs and {len(demands)} assessments across {len(time_windows)} time windows...")
        
        start_time = time.time()
        prob, alloc, unmet, inv = build_optimization_model(demands, t0_inventory, resources, hub_ids, time_windows)
        
        print("Solving LP...")
        prob.solve(pulp.PULP_CBC_CMD(msg=0))
        solve_time = time.time() - start_time
        
        print(f"Solver Status: {pulp.LpStatus[prob.status]}")
        
        if prob.status != 1:
            print(f"Optimization failed to find an optimal solution for {test_event}.")
            continue
            
        print("Formatting output...")
        # Extract optimized results
        opt_results = []
        
        for _, row in demands.iterrows():
            z = row['Assessment_ID']
            t = row['Hours_Since_Disaster']
            
            for h in hub_ids:
                res_row = {
                    'Assessment_ID': z,
                    'Event_ID': row['Event_ID'],
                    'District': row['District'],
                    'Response_Zone': row['Response_Zone'],
                    'Hours_Since_Disaster': t,
                    'Hub_ID': h,
                    'Priority_Score': row['Priority_Score'],
                    'Priority_Level': row['Priority_Level'],
                    'Estimated_Travel_Time_min': row['Estimated_Travel_Time_min'],
                    'Distance_to_Hub_km': row['Distance_to_Hub_km']
                }
                
                total_allocated = 0
                
                for r in resources:
                    r_name = r.split("_")[0]
                    pred = row[f'Predicted_{r}']
                    
                    allocated = alloc[(h, z, t, r_name)].varValue
                    allocated = allocated if allocated is not None else 0
                    
                    # Unmet is property of the zone, not hub-zone, but we duplicate it across rows for simplicity or divide it
                    unmet_val = unmet[(z, t, r_name)].varValue
                    unmet_val = unmet_val if unmet_val is not None else 0
                    
                    remaining = inv[(h, t, r_name)].varValue
                    remaining = remaining if remaining is not None else 0
                    
                    res_row[f'Predicted_{r_name}_Demand'] = pred
                    res_row[f'{r_name}_Allocated'] = allocated
                    res_row[f'{r_name}_Unmet'] = unmet_val
                    res_row[f'Remaining_{r_name}_Inventory'] = remaining
                    
                    total_allocated += allocated
                    
                # Only append if this hub actually sent something to this zone OR if it's the first hub (to ensure every assessment has at least one row for unmet demand)
                if total_allocated > 0 or h == hub_ids[0]:
                    opt_results.append(res_row)
            
        opt_df = pd.DataFrame(opt_results)
        
        # Run Validation
        is_valid = validate_allocations(opt_df, demands, t0_inventory, resources)
        
        if not is_valid:
            print(f"WARNING: Output failed constraints for {test_event}.")
            continue
            
        all_opt_results.append(opt_df)
            
        # Baseline Comparison
        print(f"Running Baseline comparison for {test_event}...")
        base_df = allocate_proportional(demands, t0_inventory, resources, time_windows, hub_ids)
        all_base_results.append(base_df)
        
    print("Combining all results...")
    final_opt_df = pd.concat(all_opt_results, ignore_index=True)
    final_base_df = pd.concat(all_base_results, ignore_index=True)
    
    # Save outputs
    outputs_dir = os.path.join(project_dir, "outputs", "phase4")
    
    final_opt_df.to_csv(os.path.join(outputs_dir, "resource_allocation.csv"), index=False)
    final_base_df.to_csv(os.path.join(outputs_dir, "baseline_allocation.csv"), index=False)
    
    print("Done. Saved to outputs/phase4/")

if __name__ == "__main__":
    run_pipeline()
