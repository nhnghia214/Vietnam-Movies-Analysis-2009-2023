import matplotlib.pyplot as plt
import seaborn as sns

def ve_xu_huong(df, cot):
    """Vẽ xu hướng một chỉ số theo năm"""
    data = df.groupby(df["release_date"].dt.year)[cot].mean()
    data.plot(kind="line", marker="o", figsize=(8,4), title=f"Xu huong {cot} theo nam")
    plt.show()

def so_sanh_covid(df, chi_so="revenue"):
    """So sánh 2019 vs 2020-2022"""
    df["nam"] = df["release_date"].dt.year
    truoc = df[df["nam"] == 2019][chi_so].mean()
    sau = df[(df["nam"] >= 2020) & (df["nam"] <= 2022)][chi_so].mean()
    return {"truoc_covid": truoc, "sau_covid": sau}

def ve_tuong_quan(df, cot_list):
    """Vẽ heatmap tương quan"""
    corr = df[cot_list].corr()
    plt.figure(figsize=(6,5))
    sns.heatmap(corr, annot=True, cmap="Blues")
    plt.show()
