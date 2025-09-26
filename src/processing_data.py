# src/processing_data.py
import pandas as pd
import numpy as np
def Tinh_ROI(df):
    # Tính lợi nhuận trên đầu tư (ROI)
    df['ROI'] = (df['revenue'] - df['budget']) / df['budget'].replace(0, np.nan)
def Loc_Nam(df, cot_ngay="release_date", tu=2000, den=2023):
    """Lọc phim theo năm"""
    return df[(df[cot_ngay].dt.year >= tu) & (df[cot_ngay].dt.year <= den)]