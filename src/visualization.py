import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def group_and_plot(df, group_col, value_cols, kind="bar", bins=None, title=""):
    """
    df: DataFrame
    group_col: cột để nhóm (categorical hoặc continuous)
    value_cols: list cột giá trị ['revenue','vote_average']
    kind: loại biểu đồ ('bar','box','scatter')
    bins: nếu group_col là continuous -> chia bin
    """
    temp = df.copy()

    # Nếu là continuous và có bins
    if bins is not None:
        temp[group_col] = pd.cut(temp[group_col], bins=bins)

    # Nhóm và tính trung bình
    grouped = temp.groupby(group_col)[value_cols].mean().reset_index()

    # Vẽ biểu đồ
    if kind == "bar":
        grouped.plot(x=group_col, kind="bar", figsize=(10, 6))
        plt.title(title)
        plt.ylabel("Average values")
        plt.show()

    elif kind == "box":
        for col in value_cols:
            sns.boxplot(x=temp[group_col], y=temp[col])
            plt.title(f"{title} - {col}")
            plt.show()

    elif kind == "scatter" and len(value_cols) == 2:
        sns.scatterplot(data=df, x=value_cols[0], y=value_cols[1], hue=group_col)
        plt.title(title)
        plt.show()

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
