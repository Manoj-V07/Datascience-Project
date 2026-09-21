import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def evaluate(models, X_test, y_test):
    """Evaluates multiple models and returns metrics DataFrame."""
    results = []
    
    for name, model in models.items():
        preds = model.predict(X_test)
        # Enforce non-negativity
        preds = np.maximum(preds, 0)
        
        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)
        
        results.append({
            'Model': name,
            'MAE': mae,
            'RMSE': rmse,
            'R2': r2
        })
        
    return pd.DataFrame(results)
