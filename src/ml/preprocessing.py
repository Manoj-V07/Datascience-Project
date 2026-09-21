import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def get_features(target):
    """Return categorical and numerical features for ML models."""
    categorical_features = ['Disaster_Type', 'District']
    
    numerical_features = [
        'Hours_Since_Disaster',
        'Population_Baseline', 'Population_Affected_Est', 'Affected_Population_pct',
        'Fatalities_Est', 'Houses_Damaged_Est',
        'Severity_Score', 'Infrastructure_Damage_Score', 'Accessibility_Score',
        'Medical_Urgency_Score', 'Temperature_C', 'Rainfall_mm', 'Wind_Speed_kmph',
        'Distance_to_Hub_km', 'Estimated_Travel_Time_min', 'Rescue_Cases_Est'
    ]
    
    # Target-specific feature overrides
    if target == 'Medical_Kits_Required':
        numerical_features.append('Injured_Est')
        
    return categorical_features, numerical_features

def build_preprocessor(categorical_features, numerical_features):
    """Builds an sklearn ColumnTransformer."""
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    return preprocessor
