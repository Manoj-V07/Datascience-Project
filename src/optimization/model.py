import pulp
import numpy as np

def build_optimization_model(demands, inventory_t0, resources, hubs, time_windows, penalty_weight=100.0, transport_weight=0.01):
    """
    Builds the PuLP LP optimization model.
    """
    # Create the problem
    prob = pulp.LpProblem("Disaster_Relief_Resource_Allocation", pulp.LpMaximize)
    
    # Priority mapping
    def get_priority_weight(level):
        if level == 'Critical': return 1.0
        if level == 'High': return 0.8
        if level == 'Moderate': return 0.5
        return 0.2

    # Prepare dictionaries for rapid access
    demand_dict = {}
    priority_dict = {}
    travel_dict = {}
    
    for _, row in demands.iterrows():
        z = row['Assessment_ID']
        t = row['Hours_Since_Disaster']
        priority_dict[z] = get_priority_weight(row['Priority_Level'])
        travel_dict[z] = row['Estimated_Travel_Time_min']
        
        for r in resources:
            r_name = r.split("_")[0]
            demand_dict[(z, t, r_name)] = row[f'Predicted_{r}']

    r_names = [r.split("_")[0] for r in resources]
    zones = demands['Assessment_ID'].unique().tolist()
    
    # ------------------
    # DECISION VARIABLES
    # ------------------
    # Allocation[h, z, t, r] -> Continuous >= 0
    alloc = pulp.LpVariable.dicts("Alloc",
        [(h, z, t, r) for h in hubs for z in zones for t in time_windows for r in r_names],
        lowBound=0, cat='Continuous')

    # UnmetDemand[z, t, r] -> Continuous >= 0
    unmet = pulp.LpVariable.dicts("Unmet",
        [(z, t, r) for z in zones for t in time_windows for r in r_names],
        lowBound=0, cat='Continuous')
        
    # RemainingInventory[h, t, r] -> Continuous >= 0
    inv = pulp.LpVariable.dicts("Inv",
        [(h, t, r) for h in hubs for t in time_windows for r in r_names],
        lowBound=0, cat='Continuous')
        
    # ------------------
    # CONSTRAINTS
    # ------------------
    for r in r_names:
        for t in time_windows:
            # 1. Demand Constraint: Allocated + Unmet = Predicted
            for z in zones:
                d = demand_dict.get((z, t, r), 0)
                prob += pulp.lpSum([alloc[(h, z, t, r)] for h in hubs]) + unmet[(z, t, r)] == d, f"Demand_{z}_{t}_{r}"
            
            # 2. Inventory Conservation & Temporal Flow
            # Get the previous period's inventory, or T0 if t == 0
            if t == 0:
                for h in hubs:
                    # Find exact opening inventory for this hub
                    h_inv = inventory_t0[(inventory_t0['Hub_ID'] == h)]
                    col_name = f'{r}_Opening_Inventory' if r != 'Shelter' else f'{r}_Opening_Capacity'
                    if not h_inv.empty:
                        start_inv = h_inv.iloc[0][col_name]
                    else:
                        start_inv = 0
                        
                    prob += inv[(h, t, r)] == start_inv - pulp.lpSum([alloc[(h, z, t, r)] for z in zones]), f"Inv_Flow_{h}_{t}_{r}"
            else:
                prev_t = time_windows[time_windows.index(t) - 1]
                for h in hubs:
                    prob += inv[(h, t, r)] == inv[(h, prev_t, r)] - pulp.lpSum([alloc[(h, z, t, r)] for z in zones]), f"Inv_Flow_{h}_{t}_{r}"

    # ------------------
    # OBJECTIVE FUNCTION
    # ------------------
    objective_terms = []
    
    for r in r_names:
        for t in time_windows:
            for z in zones:
                d = demand_dict.get((z, t, r), 0)
                # Normalize factor to prevent water (large numbers) from dominating medical (small numbers)
                norm = d if d > 0 else 1.0
                
                # Term 1: Maximize Priority-Weighted Allocation
                for h in hubs:
                    objective_terms.append(
                        alloc[(h, z, t, r)] * priority_dict[z]
                    )
                    
                    # Term 3: Minimize Travel Time (Negative weight)
                    # Penalize based on absolute travel time to prioritize closer hubs
                    objective_terms.append(
                        -alloc[(h, z, t, r)] * (travel_dict[z] / 1000.0) * transport_weight
                    )
                
                # Term 2: Minimize Unmet Demand (Negative weight)
                objective_terms.append(
                    -unmet[(z, t, r)] * penalty_weight
                )

    prob += pulp.lpSum(objective_terms), "Maximize_Fulfillment_Minimize_Shortage_Travel"
    
    return prob, alloc, unmet, inv
