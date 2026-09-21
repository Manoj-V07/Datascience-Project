import pandas as pd
import os

def preprocess_data(raw_dir, processed_dir):
    print("Starting preprocessing...")
    
    # Load raw data
    inventory_path = os.path.join(raw_dir, "resource_inventory.csv")
    zone_path = os.path.join(raw_dir, "zone_assessments.csv")
    
    if os.path.exists(inventory_path) and os.path.exists(zone_path):
        inv_df = pd.read_csv(inventory_path)
        zones_df = pd.read_csv(zone_path)
        
        # Determine temporal windows
        if 'Hours_Since_Disaster' in zones_df.columns:
            windows = sorted(zones_df['Hours_Since_Disaster'].unique())
            
            # Expand inventory to track temporal depletion
            expanded_inv = []
            for _, row in inv_df.iterrows():
                for w in windows:
                    r = row.copy()
                    r['Hours_Since_Disaster'] = w
                    expanded_inv.append(r)
            
            new_inv_df = pd.DataFrame(expanded_inv)
            new_inv_path = os.path.join(processed_dir, "resource_inventory_temporal.csv")
            new_inv_df.to_csv(new_inv_path, index=False)
            print(f"Created temporal inventory: {new_inv_path}")
    else:
        print(f"Raw files not found in {raw_dir}")
            
if __name__ == "__main__":
    raw = r"d:\Data-Science-Project\data\raw"
    processed = r"d:\Data-Science-Project\data\processed"
    preprocess_data(raw, processed)