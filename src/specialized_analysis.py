def ngan_sach_vs_doanh_thu(df):
    """Kiểm tra tương quan ngân sách & doanh thu"""
    return df[["budget", "revenue"]].corr().iloc[0,1]

def phim_roi_cao(df, top=10):
    """Top phim ROI cao nhất"""
    return df.sort_values("roi", ascending=False).head(top)

def xu_huong_the_loai(df):
    """Số phim theo thể loại & năm"""
    df["nam"] = df["release_date"].dt.year
    return df.explode("genres").groupby(["nam", "genres"])["id"].count()

def so_sanh_truoc_sau_covid(df):
    """So sánh số phim, revenue, rating trước/sau COVID"""
    df["nam"] = df["release_date"].dt.year
    truoc = df[df["nam"] == 2019]
    sau = df[(df["nam"] >= 2020) & (df["nam"] <= 2022)]
    return {
        "so_phim_truoc": len(truoc),
        "so_phim_sau": len(sau),
        "doanh_thu_tb_truoc": truoc["revenue"].mean(),
        "doanh_thu_tb_sau": sau["revenue"].mean(),
        "diem_tb_truoc": truoc["vote_average"].mean(),
        "diem_tb_sau": sau["vote_average"].mean()
    }
