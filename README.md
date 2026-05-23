# AI Movie Recommendation System

## Project Objective

This project is an AI-driven web application that recommends movies based on a user's preferred genre, mood, movie title, or story idea. It helps users quickly discover movies that match what they want to watch.

## Tools Used

- Python
- Streamlit for the web frontend
- FastAPI for the backend API
- Pandas for loading movie data
- Scikit-learn for the AI recommendation model
- Requests for frontend-to-backend communication

## AI Model Used

The application uses a locally trained content-based recommendation model.

The model combines each movie's title, genre, and description, then uses `TfidfVectorizer` from scikit-learn to convert movie text into numerical AI features. It compares the user's input with the movie dataset using cosine similarity and returns the most relevant movies.

## Project Structure

```text
.
├── backend/
│   ├── main.py
│   └── recommender.py
├── data/
│   └── movies.csv
├── streamlit_app.py
├── requirements.txt
└── README.md
```

## Running Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

On Windows, if `python` and `pip` are not recognized, use:

```bash
py -m pip install -r requirements.txt
```

### 2. Start the FastAPI backend

```bash
uvicorn backend.main:app --reload
```

Or on Windows:

```bash
py -m uvicorn backend.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

You can test the API documentation at:

```text
http://127.0.0.1:8000/docs
```

### 3. Start the Streamlit frontend

Open a second terminal and run:

```bash
streamlit run streamlit_app.py
```

Or on Windows:

```bash
py -m streamlit run streamlit_app.py
```

The Streamlit app will run at:

```text
http://localhost:8501
```

## How It Works

1. The user enters a movie preference in Streamlit.
2. Streamlit sends the input to the FastAPI backend.
3. FastAPI passes the input to the AI recommendation model.
4. The model calculates similarity scores between the user input and movie descriptions.
5. The backend returns the best matches.
6. Streamlit displays the recommended movies clearly.
