import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from scipy import stats

def clean_data(df):
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    imputer = IterativeImputer()
    df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
    df = df.drop_duplicates()
    z_scores = stats.zscore(df[numeric_cols])
    abs_z_scores = np.abs(z_scores)
    filtered_entries = (abs_z_scores < 3).all(axis=1)
    df = df[filtered_entries]
    return df
