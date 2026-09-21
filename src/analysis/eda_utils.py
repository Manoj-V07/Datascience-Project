
import pandas as pd
import os

def load_processed_data():
    raw_dir = r"d:\Data-Science-Project\data\raw"
    processed_dir = r"d:\Data-Science-Project\data\processed"
    
    zones = pd.read_csv(os.path.join(raw_dir, "zone_assessments.csv"))
    events = pd.read_csv(os.path.join(raw_dir, "disaster_events.csv"))
    hubs = pd.read_csv(os.path.join(raw_dir, "relief_hubs.csv"))
    
    # Merge events for disaster types
    df = zones.merge(events[['Event_ID', 'Disaster_Type']], on='Event_ID', how='left')
    return df, events, hubs
