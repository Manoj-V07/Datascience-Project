import pandas as pd
import numpy as np
from sklearn.inspection import permutation_importance

def calculate_feature_importance(model, X_test, y_test, num_features, cat_features):
    """Calculates permutation importance for the given pipeline model."""
    result = permutation_importance(model, X_test, y_test, n_repeats=5, random_state=42, n_jobs=-1)
    
    # We must match the original feature names, not the OneHotEncoded ones, which is what Permutation Importance allows when passing the full pipeline
    all_features = num_features + cat_features
    
    importance_df = pd.DataFrame({
        'Feature': all_features,
        'Importance': result.importances_mean,
        'Std': result.importances_std
    }).sort_values(by='Importance', ascending=False)
    
    return importance_df
