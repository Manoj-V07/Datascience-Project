import pandas as pd
import numpy as np
import os

def evaluate():
    project_dir = r"d:\Data-Science-Project"
    out_dir = os.path.join(project_dir, "outputs", "phase4")
    
    print("Loading allocations...")
    opt_df = pd.read_csv(os.path.join(out_dir, "resource_allocation.csv"))
    base_df = pd.read_csv(os.path.join(out_dir, "baseline_allocation.csv"))
    
    resources = ['Food', 'Water', 'Medical', 'Shelter']
    
    summary = []
    
    for r in resources:
        # Optimized Metrics
        opt_demand = opt_df.groupby('Assessment_ID')[f'Predicted_{r}_Demand'].first().sum()
        opt_alloc = opt_df[f'{r}_Allocated'].sum()
        opt_unmet = opt_demand - opt_alloc
        
        # Baseline Metrics
        base_demand = base_df.groupby('Assessment_ID')['Predicted_Demand'].first().sum() if f'Predicted_{r}_Demand' not in base_df.columns else base_df.groupby('Assessment_ID')[f'Predicted_{r}_Demand'].first().sum()
        
        # In baseline, the resource is in the 'Resource' column
        base_r_df = base_df[base_df['Resource'] == r]
        base_alloc = base_r_df['Allocated'].sum()
        base_unmet = base_demand - base_alloc
        
        summary.append({
            'Resource': r,
            'Total_Demand': opt_demand,
            'Opt_Allocated': opt_alloc,
            'Opt_Unmet': opt_unmet,
            'Opt_Fulfillment_%': (opt_alloc / opt_demand * 100) if opt_demand > 0 else 100,
            'Base_Allocated': base_alloc,
            'Base_Unmet': base_unmet,
            'Base_Fulfillment_%': (base_alloc / opt_demand * 100) if opt_demand > 0 else 100,
            'Improvement_%': ((opt_alloc - base_alloc) / opt_demand * 100) if opt_demand > 0 else 0
        })
        
    summary_df = pd.DataFrame(summary)
    print("\n--- Allocation Summary ---")
    print(summary_df)
    summary_df.to_csv(os.path.join(out_dir, "allocation_summary.csv"), index=False)
    
    # Let's also look at Priority Fulfillment in Optimized
    opt_df['Priority_Score'] = opt_df['Priority_Score'].fillna(0)
    opt_grouped = opt_df.groupby('Priority_Level').agg({
        **{f'Predicted_{r}_Demand': 'sum' for r in resources},
        **{f'{r}_Allocated': 'sum' for r in resources}
    }).reset_index()
    
    print("\n--- Priority Fulfillment (Optimized) ---")
    for r in resources:
        opt_grouped[f'{r}_Fulfillment_%'] = (opt_grouped[f'{r}_Allocated'] / opt_grouped[f'Predicted_{r}_Demand'].replace(0, 1)) * 100
        print(opt_grouped[['Priority_Level', f'{r}_Fulfillment_%']])
        
    opt_grouped.to_csv(os.path.join(out_dir, "priority_fulfillment.csv"), index=False)

if __name__ == "__main__":
    evaluate()
