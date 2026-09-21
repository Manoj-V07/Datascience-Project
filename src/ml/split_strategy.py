import pandas as pd
from sklearn.model_selection import GroupKFold

def get_cv_splitter(n_splits=5):
    """Return GroupKFold to prevent leakage across simulations/times of same event."""
    return GroupKFold(n_splits=n_splits)

def get_train_test_split(X, y, groups, test_size_groups=1):
    """
    Splits data such that groups (e.g. Event_IDs) are fully in train or test.
    We'll do a deterministic split based on unique groups for the final holdout.
    """
    unique_groups = groups.unique()
    # Simple deterministic split (e.g., last 'test_size_groups' events as test)
    test_groups = unique_groups[-test_size_groups:]
    train_groups = unique_groups[:-test_size_groups]
    
    train_idx = groups.isin(train_groups)
    test_idx = groups.isin(test_groups)
    
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx], groups[train_idx], groups[test_idx]
