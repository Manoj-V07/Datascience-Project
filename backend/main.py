from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import sys
import joblib
from pydantic import BaseModel

app = FastAPI(title="Disaster Relief API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_DIR = r"d:\Data-Science-Project"

# Memoized Dataframes (simple cache)
cache = {}

def get_df(path):
    if path not in cache:
        full_path = os.path.join(PROJECT_DIR, path)
        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail=f"Data file not found: {path}")
        cache[path] = pd.read_csv(full_path).fillna("")
    return cache[path]

@app.get("/api/events")
def get_events():
    df = get_df(r"data\raw\disaster_events.csv")
    return df.to_dict(orient="records")

@app.get("/api/hubs")
def get_hubs():
    df = get_df(r"data\raw\relief_hubs.csv")
    return df.to_dict(orient="records")

@app.get("/api/historical")
def get_historical():
    df = get_df(r"data\raw\historical_event_districts.csv")
    return df.to_dict(orient="records")

def get_sim_assessment_ids(event_id: str, time_window: int, sim_id: str):
    df = get_df(r"data\processed\v2_6\zone_assessments_v2_6.csv")
    filtered = df[(df['Event_ID'] == event_id) & (df['Hours_Since_Disaster'] == time_window)]
    if 'Simulation_ID' in filtered.columns:
        filtered = filtered[filtered['Simulation_ID'] == sim_id]
    if 'Assessment_ID' in filtered.columns:
        return filtered['Assessment_ID'].tolist()
    return []

@app.get("/api/assessments")
def get_assessments(event_id: str, time_window: int = 0, sim_id: str = "SIM001"):
    df = get_df(r"data\processed\v2_6\zone_assessments_v2_6.csv")
    sim001_ids = get_sim_assessment_ids(event_id, time_window, sim_id)
    filtered = df[(df['Event_ID'] == event_id) & (df['Hours_Since_Disaster'] == time_window)]
    if 'Assessment_ID' in filtered.columns and sim001_ids:
        filtered = filtered[filtered['Assessment_ID'].isin(sim001_ids)]
    return filtered.to_dict(orient="records")

@app.get("/api/inventory")
def get_inventory(event_id: str, time_window: int = 0):
    df = get_df(r"data\processed\v2_6\resource_inventory_temporal_v2_6.csv")
    filtered = df[(df['Event_ID'] == event_id) & (df['Hours_Since_Disaster'] == time_window)]
    return filtered.to_dict(orient="records")

@app.get("/api/predictions")
def get_predictions(event_id: str, time_window: int = 0, sim_id: str = "SIM001"):
    df = get_df(r"outputs\phase3_1\demand_predictions.csv")
    sim001_ids = get_sim_assessment_ids(event_id, time_window, sim_id)
    filtered = df[(df['Event_ID'] == event_id) & (df['Hours_Since_Disaster'] == time_window)]
    if 'Assessment_ID' in filtered.columns and sim001_ids:
        filtered = filtered[filtered['Assessment_ID'].isin(sim001_ids)]
    return filtered.to_dict(orient="records")

@app.get("/api/allocations")
def get_allocations(event_id: str, time_window: int = 0, sim_id: str = "SIM001"):
    df = get_df(r"outputs\phase4\resource_allocation.csv")
    sim001_ids = get_sim_assessment_ids(event_id, time_window, sim_id)
    filtered = df[(df['Event_ID'] == event_id) & (df['Hours_Since_Disaster'] == time_window)]
    if 'Assessment_ID' in filtered.columns and sim001_ids:
        filtered = filtered[filtered['Assessment_ID'].isin(sim001_ids)]
    return filtered.to_dict(orient="records")

@app.get("/api/baseline")
def get_baseline(event_id: str, time_window: int = 0, sim_id: str = "SIM001"):
    df = get_df(r"outputs\phase4\baseline_allocation.csv")
    sim001_ids = get_sim_assessment_ids(event_id, time_window, sim_id)
    filtered = df[(df['Event_ID'] == event_id) & (df['Hours_Since_Disaster'] == time_window)]
    if 'Assessment_ID' in filtered.columns and sim001_ids:
        filtered = filtered[filtered['Assessment_ID'].isin(sim001_ids)]
    return filtered.to_dict(orient="records")

class CustomPredictionRequest(BaseModel):
    Disaster_Type: str
    District: str
    Hours_Since_Disaster: float
    Population_Baseline: float
    Population_Affected_Est: float
    Affected_Population_pct: float
    Fatalities_Est: float
    Houses_Damaged_Est: float
    Severity_Score: float
    Infrastructure_Damage_Score: float
    Accessibility_Score: float
    Medical_Urgency_Score: float
    Temperature_C: float
    Rainfall_mm: float
    Wind_Speed_kmph: float
    Distance_to_Hub_km: float
    Estimated_Travel_Time_min: float
    Rescue_Cases_Est: float
    Injured_Est: float

models_cache = {}

@app.post("/api/predict_custom")
def predict_custom(req: CustomPredictionRequest):
    req_dict = req.dict()
    df_input = pd.DataFrame([req_dict])
    
    resources = [
        "Food_Required_packets",
        "Water_Required_Liters",
        "Medical_Kits_Required",
        "Shelter_Spaces_Required"
    ]
    
    results = {}
    
    for r in resources:
        if r not in models_cache:
            model_path = os.path.join(PROJECT_DIR, "models", "phase3_1", f"{r.lower()}_model.pkl")
            if not os.path.exists(model_path):
                raise HTTPException(status_code=404, detail=f"Model for {r} not found.")
            models_cache[r] = joblib.load(model_path)
            
        model = models_cache[r]
        # Predict
        try:
            pred = model.predict(df_input)[0]
            results[r] = max(0, int(round(pred)))
        except Exception as e:
            print(f"Error predicting {r}: {e}")
            results[r] = 0
            
    return {"predictions": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
