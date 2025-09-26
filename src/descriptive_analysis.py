def top_doanh_thu(df, n=10):
    """Top n phim doanh thu cao nhất"""
    return df.sort_values("revenue", ascending=False).head(n)

def diem_tb_the_loai(df):
    """Điểm trung bình theo thể loại"""
    return df.explode("genres").groupby("genres")["vote_average"].mean()

def doanh_thu_tb_quoc_gia(df):
    """Doanh thu TB theo quốc gia"""
    return df.explode("production_countries").groupby("production_countries")["revenue"].mean()

def phan_phoi_thoi_luong(df):
    """Phân phối thời lượng phim"""
    return df["runtime"].dropna()
