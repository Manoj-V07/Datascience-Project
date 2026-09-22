import os

def check_project_health(project_dir="."):
    """Verifies that all required outputs from Phases 1-4 exist and are valid."""
    print("--- Phase 5 Pre-Flight Health Check ---")
    
    required_files = [
        ("Phase 1 - Zone Assessments", "data/processed/v2_6/zone_assessments_v2_6.csv"),
        ("Phase 1 - Inventory", "data/processed/v2_6/resource_inventory_temporal_v2_6.csv"),
        ("Phase 3 - ML Predictions", "outputs/phase3_1/demand_predictions.csv"),
        ("Phase 4 - Allocations", "outputs/phase4/resource_allocation.csv"),
        ("Phase 4 - Baseline", "outputs/phase4/baseline_allocation.csv"),
        ("Raw - Disaster Events", "data/raw/disaster_events.csv"),
        ("Raw - Hubs", "data/raw/relief_hubs.csv"),
        ("Raw - Historical Overlap", "data/raw/historical_event_districts.csv")
    ]
    
    all_passed = True
    
    for name, path in required_files:
        full_path = os.path.join(project_dir, path)
        if os.path.exists(full_path):
            print(f"[PASS] {name} exists.")
        else:
            print(f"[FAIL] Missing required file: {full_path}")
            all_passed = False
            
    # Optional: Quick schema check
    if all_passed:
        import pandas as pd
        try:
            alloc_df = pd.read_csv(os.path.join(project_dir, "outputs/phase4/resource_allocation.csv"))
            req_cols = ['Assessment_ID', 'Event_ID', 'Food_Allocated', 'Food_Unmet', 'Remaining_Food_Inventory']
            if all(c in alloc_df.columns for c in req_cols):
                print("[PASS] Allocation schema looks correct.")
            else:
                print("[FAIL] Allocation schema is missing columns.")
                all_passed = False
        except Exception as e:
            print(f"[FAIL] Error reading allocation output: {str(e)}")
            all_passed = False
            
    if all_passed:
        print("\nHEALTH CHECK STATUS: PASS")
    else:
        print("\nHEALTH CHECK STATUS: FAIL")
        
    return all_passed

if __name__ == "__main__":
    check_project_health(r"d:\Data-Science-Project")
