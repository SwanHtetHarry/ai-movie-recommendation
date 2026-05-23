from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "movies.csv"


class MovieRecommender:
    """Small local AI model using TF-IDF text features over movie metadata."""

    def __init__(self, data_path: Path = DATA_PATH):
        self.movies = pd.read_csv(data_path)
        self.movies["combined_text"] = (
            self.movies["title"].fillna("")
            + " "
            + self.movies["genres"].fillna("")
            + " "
            + self.movies["description"].fillna("")
        )
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.movie_vectors = self.vectorizer.fit_transform(self.movies["combined_text"])

    def recommend(self, user_input: str, top_k: int = 5) -> list[dict]:
        query = user_input.strip()
        if not query:
            return []

        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.movie_vectors).flatten()
        ranked_indexes = scores.argsort()[::-1][:top_k]

        recommendations = []
        for index in ranked_indexes:
            movie = self.movies.iloc[index]
            recommendations.append(
                {
                    "title": movie["title"],
                    "genres": movie["genres"],
                    "description": movie["description"],
                    "score": round(float(scores[index]), 3),
                }
            )
        return recommendations

    def titles(self) -> list[str]:
        return self.movies["title"].tolist()
