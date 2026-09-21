import pandas as pd
import numpy as np
import os
import joblib
import json

from preprocessing import get_features
from split_strategy import get_train_test_split
from train_models import train_and_tune
from evaluate_models import evaluate
from explain_models import calculate_feature_importance

def main():
    project_dir = r"d:\Data-Science-Project"
    v2_6_dir = os.path.join(project_dir, "data", "processed", "v2_6")
    models_dir = os.path.join(project_dir, "models", "phase3_1")
    outputs_dir = os.path.join(project_dir, "outputs", "phase3_1")
    
    df = pd.read_csv(os.path.join(v2_6_dir, "zone_assessments_v2_6.csv"))
    events = pd.read_csv(os.path.join(project_dir, "data", "raw", "disaster_events.csv"))
    df = df.merge(events[['Event_ID', 'Disaster_Type']], on='Event_ID', how='left')
    
    targets = [
        'Food_Required_packets',
        'Water_Required_Liters',
        'Medical_Kits_Required',
        'Shelter_Spaces_Required'
    ]
    
    final_predictions = df[['Assessment_ID', 'Event_ID', 'District', 'Response_Zone', 'Assessment_Window', 'Hours_Since_Disaster']].copy()
    
    report = []
    
    # Simple holdout: the last 5 events out of ~120 for test set
    groups = df['Event_ID']
    
    metadata = {}
    
    for tgt in targets:
        print(f"\n=============================")
        print(f"Processing {tgt}...")
        
        cat_feats, num_feats = get_features(tgt)
        features = cat_feats + num_feats
        
        X = df[features]
        y = df[tgt]
        
        X_train, X_test, y_train, y_test, g_train, g_test = get_train_test_split(X, y, groups, test_size_groups=5)
        print(f"Train samples: {len(X_train)} | Test samples: {len(X_test)}")
        
        # Train & Tune
        models = train_and_tune(X_train, y_train, g_train, tgt)
        
        # Evaluate
        results_df = evaluate(models, X_test, y_test)
        print("\nEvaluation Metrics:")
        print(results_df)
        
        # Select best model (lowest MAE)
        best_model_name = results_df.loc[results_df['MAE'].idxmin()]['Model']
        best_model = models[best_model_name]
        print(f"\nBest Model selected: {best_model_name}")
        
        # Calculate feature importance
        fi_df = calculate_feature_importance(best_model, X_test, y_test, num_feats, cat_feats)
        top_features = fi_df.head(5)['Feature'].tolist()
        
        report.append({
            'Target': tgt,
            'Best_Model': best_model_name,
            'MAE': results_df.loc[results_df['Model'] == best_model_name, 'MAE'].values[0],
            'RMSE': results_df.loc[results_df['Model'] == best_model_name, 'RMSE'].values[0],
            'R2': results_df.loc[results_df['Model'] == best_model_name, 'R2'].values[0],
            'Top_Features': top_features
        })
        
        # Save model
        model_path = os.path.join(models_dir, f"{tgt.lower()}_model.pkl")
        joblib.dump(best_model, model_path)
        
        metadata[tgt] = {
            'best_model': best_model_name,
            'features': features,
            'metrics': results_df.to_dict(orient='records'),
            'top_features': top_features
        }
        
        # Generate predictions for the entire dataset to store in outputs
        # Note: In real life we only predict on test, but for the requirement "outputs/phase3/demand_predictions.csv" 
        # we provide predictions for all rows so Phase 4 can use it.
        preds = best_model.predict(X)
        preds = np.maximum(preds, 0)
        
        final_predictions[f"Actual_{tgt}"] = df[tgt]
        final_predictions[f"Predicted_{tgt}"] = preds.round().astype(int)
        
    # Save predictions
    final_predictions.to_csv(os.path.join(outputs_dir, "demand_predictions.csv"), index=False)
    
    # Save metadata
    with open(os.path.join(models_dir, "model_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=4)
        
    # Save quick report
    with open(os.path.join(outputs_dir, "quick_report.json"), "w") as f:
        json.dump(report, f, indent=4)
        
    print("\nPhase 3 pipeline execution complete.")

if __name__ == "__main__":
    main()
