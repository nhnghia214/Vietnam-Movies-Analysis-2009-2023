# src/clean_code.py
import pandas as pd
import numpy as np

def load_data(file_path):
    """Đọc dataset từ CSV"""
    return pd.read_csv(file_path)