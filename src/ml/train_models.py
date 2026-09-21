import pandas as pd
import numpy as np
import os
import joblib
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from preprocessing import get_features, build_preprocessor
from split_strategy import get_cv_splitter

def get_models():
    """Return dictionary of models to evaluate."""
    return {
        'Linear_Regression': LinearRegression(),
        'Ridge': Ridge(alpha=1.0),
        'Random_Forest': RandomForestRegressor(random_state=42, n_jobs=-1)
    }

def train_and_tune(X_train, y_train, groups_train, target):
    """Trains baseline and tunes advanced models using GroupKFold."""
    cat_feats, num_feats = get_features(target)
    preprocessor = build_preprocessor(cat_feats, num_feats)
    
    models = get_models()
    best_pipelines = {}
    
    cv = get_cv_splitter(n_splits=5)
    
    for name, model in models.items():
        pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', model)])
        
        if name == 'Random_Forest':
            param_distributions = {
                'regressor__n_estimators': [50, 100],
                'regressor__max_depth': [None, 10, 20],
                'regressor__min_samples_split': [2, 5]
            }
            search = RandomizedSearchCV(
                pipeline, param_distributions, n_iter=5, cv=cv, 
                scoring='neg_mean_absolute_error', random_state=42, n_jobs=-1
            )
            search.fit(X_train, y_train, groups=groups_train)
            best_pipelines[name] = search.best_estimator_
            print(f"Tuned {name} for {target}. Best MAE: {-search.best_score_:.2f}")
        else:
            pipeline.fit(X_train, y_train)
            best_pipelines[name] = pipeline
            print(f"Trained {name} for {target}.")
            
    return best_pipelines
