import requests
import pandas as pd
import time

API_KEY = "d85632569c1b7220a3dc26d452f8b3d2"
BASE_URL = "https://api.themoviedb.org/3"

def fetch_movies_by_year(year, max_pages=2):
    """Lấy phim theo năm bằng discover/movie"""
    all_movies = []
    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}/discover/movie"
        params = {
            "api_key": API_KEY,
            "language": "en-US",
            "sort_by": "popularity.desc",
            "page": page,
            "primary_release_date.gte": f"{year}-01-01",
            "primary_release_date.lte": f"{year}-12-31"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            all_movies.extend(data["results"])
        else:
            print(f"❌ Error fetching year {year}, page {page}: {response.status_code}")
    return all_movies

def fetch_movie_detail(movie_id):
    """Lấy chi tiết phim để có budget, revenue, runtime,..."""
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error fetching movie {movie_id}: {response.status_code}")
        return {}

def build_movies_dataframe(start_year=2009, end_year=2023, pages_per_year=2):
    all_data = []
    for year in range(start_year, end_year + 1):
        movies = fetch_movies_by_year(year, max_pages=pages_per_year)
        for movie in movies:
            detail = fetch_movie_detail(movie["id"])
            movie_data = {
                "id": movie["id"],
                "title": movie.get("title"),
                "release_date": movie.get("release_date"),
                "vote_average": movie.get("vote_average"),
                "vote_count": movie.get("vote_count"),
                "popularity": movie.get("popularity"),
                "original_language": movie.get("original_language"),
                "budget": detail.get("budget"),
                "revenue": detail.get("revenue"),
                "runtime": detail.get("runtime"),
                "status": detail.get("status")
            }
            all_data.append(movie_data)
            time.sleep(0.2)  # tránh vượt rate limit
        print(f"✅ Done year {year}, collected {len(movies)} movies")
    return pd.DataFrame(all_data)

def save_to_csv(df, filename="movies_2009_2023.csv"):
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"💾 Saved {len(df)} movies to {filename}")

if __name__ == "__main__":
    df = build_movies_dataframe(2009, 2023, pages_per_year=2)  # thử trước 2 trang/năm
    save_to_csv(df, "movies_2009_2023.csv")
    print(df.head())
