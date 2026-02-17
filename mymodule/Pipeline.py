from sklearn.base import BaseEstimator, TransformerMixin
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np

class ColumnSelector(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        super().__init__()
        self.columns = columns

    def fit(self, x, y=None):
        return self
    
    def transform(self, x):
        return x[self.columns]
    

class SequenceBuilder(BaseEstimator, TransformerMixin):
    def __init__(self, lookback=60, target_col='close'):
        self.lookback = lookback
        self.target_col = target_col
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X_seq = []
        y_seq = []
        
        values = X.values
        cols = list(X.columns)
        target_idx = cols.index(self.target_col)
        
        for i in range(self.lookback, len(values)):
            X_seq.append(values[i-self.lookback:i])
            y_seq.append(values[i, target_idx])
        
        return np.array(X_seq), np.array(y_seq)

class TransformerRegressor(BaseEstimator):
    def __init__(self, build_fn, epochs=100, batch_size=32):
        self.build_fn = build_fn
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None
        
    def fit(self, X, y):
        self.model = self.build_fn(X.shape[1], X.shape[2])
        
        early_stop = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        self.model.fit(
            X, y,
            epochs=self.epochs,
            batch_size=self.batch_size,
            validation_split=0.1,
            callbacks=[early_stop],
            verbose=1
        )
        return self
    
    def predict(self, X):
        return self.model.predict(X)
    
class DataFrameConverter(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        import pandas as pd
        return pd.DataFrame(X, columns=self.columns)