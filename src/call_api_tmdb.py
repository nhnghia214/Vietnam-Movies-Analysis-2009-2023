import requests
import pandas as pd
import time

API_KEY = "d85632569c1b7220a3dc26d452f8b3d2"
BASE_URL = "https://api.themoviedb.org/3"

def fetch_movies_by_year(year, max_pages=2):
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

def has_vietnam_release(movie_id):
    """Kiểm tra xem phim có phát hành tại Việt Nam (VN) không"""
    url = f"{BASE_URL}/movie/{movie_id}/release_dates"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        for entry in data.get("results", []):
            if entry.get("iso_3166_1") == "VN":
                return True
    else:
        print(f"❌ Error fetching release dates for movie {movie_id}: {response.status_code}")
    return False

def fetch_movie_detail(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error fetching movie {movie_id}: {response.status_code}")
        return {}

def build_movies_dataframe(start_year=2009, end_year=2023, pages_per_year=3):
    all_data = []
    for year in range(start_year, end_year + 1):
        movies = fetch_movies_by_year(year, max_pages=pages_per_year)
        for movie in movies:
            movie_id = movie["id"]
            if not has_vietnam_release(movie_id):
                continue  # bỏ qua phim không chiếu tại VN

            detail = fetch_movie_detail(movie_id)
            movie_data = {
                "id": movie_id,
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
            time.sleep(0.25)  # tránh vượt rate limit
        print(f"✅ Done year {year}, collected {len(all_data)} movies so far")
    return pd.DataFrame(all_data)

def save_to_csv(df, filename="movies_vietnam_release.csv"):
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"💾 Saved {len(df)} movies to {filename}")

if __name__ == "__main__":
    df = build_movies_dataframe(2015, 2023, pages_per_year=20)
    save_to_csv(df, "movies_vietnam_release.csv")
    print(df.head())
