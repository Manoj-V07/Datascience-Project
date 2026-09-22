import pandas as pd

def validate_allocations(alloc_df, demands_df, t0_inventory_df, resources):
    """
    Mathematically validates the optimization output to ensure constraint compliance.
    Returns True if valid, False otherwise.
    """
    print("\n--- Running Validation ---")
    is_valid = True
    r_names = [r.split("_")[0] for r in resources]
    
    # 1. Non-negativity
    if (alloc_df[[f'{r}_Allocated' for r in r_names] + [f'{r}_Unmet' for r in r_names] + [f'Remaining_{r}_Inventory' for r in r_names]] < -1e-5).any().any():
        print("FAIL: Negative values found in allocation, unmet, or remaining inventory.")
        is_valid = False
        
    # 2. Demand Conservation
    # Since an assessment can be supplied by multiple hubs, we must group by Assessment and Time
    grouped_alloc = alloc_df.groupby(['Assessment_ID', 'Hours_Since_Disaster']).agg({
        **{f'Predicted_{r}_Demand': 'first' for r in r_names},
        **{f'{r}_Allocated': 'sum' for r in r_names},
        **{f'{r}_Unmet': 'first' for r in r_names} # Unmet is identical across rows for the same zone/time
    }).reset_index()
    
    for r in r_names:
        demand_diff = (grouped_alloc[f'Predicted_{r}_Demand'] - (grouped_alloc[f'{r}_Allocated'] + grouped_alloc[f'{r}_Unmet'])).abs()
        if (demand_diff > 1e-4).any():
            print(f"FAIL: Demand Conservation violated for {r}.")
            is_valid = False

    # 3. Temporal Flow & Inventory Conservation
    # For each hub and resource, the flow must be monotonic down, and sum of allocations cannot exceed t0 inventory
    hubs = alloc_df['Hub_ID'].unique()
    time_windows = sorted(alloc_df['Hours_Since_Disaster'].unique())
    
    for h in hubs:
        h_t0_inv = t0_inventory_df[t0_inventory_df['Hub_ID'] == h]
        
        for r in r_names:
            col_name = f'{r}_Opening_Inventory' if r != 'Shelter' else f'{r}_Opening_Capacity'
            if h_t0_inv.empty:
                max_inv = 0
            else:
                max_inv = h_t0_inv.iloc[0][col_name]
                
            total_allocated_across_time = 0
            
            for t in time_windows:
                # Sum of allocation to all zones from this hub at time t
                subset = alloc_df[(alloc_df['Hub_ID'] == h) & (alloc_df['Hours_Since_Disaster'] == t)]
                period_allocation = subset[f'{r}_Allocated'].sum()
                
                # Check remaining inventory matches expected flow
                if not subset.empty:
                    # In our dataset structure, Remaining_Inventory is recorded identically on all zone rows for the same hub/time
                    reported_remaining = subset.iloc[0][f'Remaining_{r}_Inventory']
                    expected_remaining = max_inv - (total_allocated_across_time + period_allocation)
                    
                    if abs(reported_remaining - expected_remaining) > 1e-4:
                        print(f"FAIL: Inventory Flow violated for Hub {h}, Resource {r}, Time {t}.")
                        print(f"  Expected {expected_remaining}, got {reported_remaining}")
                        is_valid = False
                        
                total_allocated_across_time += period_allocation
                
            if total_allocated_across_time > max_inv + 1e-4:
                print(f"FAIL: Total allocated exceeds opening inventory for Hub {h}, Resource {r}.")
                is_valid = False

    if is_valid:
        print("PASS: All mathematical constraints satisfied.")
    else:
        print("Validation Failed.")
        
    return is_valid
