
from sklearn.base import BaseEstimator, OutlierMixin
from sklearn.ensemble import IsolationForest
import numpy as np

class UnsupervisedEnsemble(BaseEstimator, OutlierMixin):
    def __init__(self, grid_configs, contamination=0.1):
        self.grid_configs = grid_configs
        self.contamination = contamination
        self.models = []
        # self.scaler = MinMaxScaler() # Scaler handled externally now

    def fit(self, X):
        self.models = []
        # print(f"  Training Ensemble with {len(self.grid_configs)} component models...")
        
        for i, config in enumerate(self.grid_configs):
            model = IsolationForest(
                n_estimators=config['n_estimators'],
                max_samples=config['max_samples'],
                max_features=config['max_features'],
                contamination=self.contamination,
                random_state=42 + i, # Diversity in seed
                n_jobs=-1,
                bootstrap=False
            )
            model.fit(X)
            self.models.append(model)
        return self

    def decision_function(self, X):
        # Average the decision_function scores from all models
        # IF returns negative for anomalies. We want consistent averaging.
        avg_score = np.zeros(X.shape[0])
        for model in self.models:
            avg_score += model.decision_function(X)
        return avg_score / len(self.models)
