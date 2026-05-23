from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.recommender import MovieRecommender


app = FastAPI(title="AI Movie Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = MovieRecommender()


class RecommendationRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Movie title, genre, mood, or story preference")
    top_k: int = Field(5, ge=1, le=10, description="Number of recommendations to return")


@app.get("/")
def health_check() -> dict:
    return {
        "message": "AI Movie Recommendation API is running",
        "model": "Local TF-IDF content-based recommendation model",
    }


@app.get("/movies")
def get_movies() -> dict:
    return {"movies": model.titles()}


@app.post("/recommend")
def recommend_movies(request: RecommendationRequest) -> dict:
    recommendations = model.recommend(request.query, request.top_k)
    if not recommendations:
        raise HTTPException(status_code=400, detail="Please enter a movie preference.")

    return {
        "query": request.query,
        "recommendations": recommendations,
    }
