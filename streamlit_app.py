import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(page_title="AI Movie Recommender", page_icon="movie", layout="wide")

st.title("AI Movie Recommendation System")
st.write("Enter a movie, genre, mood, or story idea and get AI-powered movie recommendations.")

with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Number of recommendations", min_value=1, max_value=10, value=5)
    st.caption("Backend API: http://127.0.0.1:8000")

query = st.text_area(
    "What kind of movie do you want to watch?",
    placeholder="Example: emotional sci-fi adventure, funny animation for family, dark crime thriller...",
    height=120,
)

if st.button("Recommend Movies", type="primary"):
    if not query.strip():
        st.warning("Please enter your movie preference first.")
    else:
        try:
            response = requests.post(
                f"{API_URL}/recommend",
                json={"query": query, "top_k": top_k},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            st.subheader("Recommended Movies")
            for index, movie in enumerate(data["recommendations"], start=1):
                with st.container(border=True):
                    st.markdown(f"### {index}. {movie['title']}")
                    st.write(f"**Genres:** {movie['genres']}")
                    st.write(movie["description"])
                    st.progress(min(movie["score"], 1.0), text=f"Similarity score: {movie['score']}")

        except requests.exceptions.ConnectionError:
            st.error("Backend API is not running. Start FastAPI first with: uvicorn backend.main:app --reload")
        except requests.exceptions.RequestException as error:
            st.error(f"Request failed: {error}")
