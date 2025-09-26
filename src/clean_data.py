# src/clean_data.py
import pandas as pd
import numpy as np
def DocFile(file_path):
    # Đọc dataset từ CSV
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print("File khong ton tai")
        return None
def Chuan_Hoa_Cot(df):
    # Đổi tên cột về dạng chữ thường, thay khoảng trắng bằng '_'
    return df.rename(columns = lambda x: x.strip().lower().replace(' ', '_'))
def Chuyen_Doi_Ngay(df, cot_ngay):
    # Chuyển cột ngày sang datetime
    df[cot_ngay] = pd.to_datetime(df[cot_ngay], errors = 'coerce')
def Tach_The_Loai(df, cot_the_loai="genres"):
    """Tách thể loại thành list"""
    df[cot_the_loai] = df[cot_the_loai].fillna("").apply(lambda x: x.split(","))
    return df
def Lam_Sach_Thieu(df):
    """Điền missing value cơ bản"""
    df["budget"] = df["budget"].fillna(0)
    df["revenue"] = df["revenue"].fillna(0)
    df["runtime"] = df["runtime"].fillna(df["runtime"].mean())
    return df
