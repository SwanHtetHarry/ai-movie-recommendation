import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="CineMatch – AI Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0a0a0b;
    --surface:   #111114;
    --card:      #16161a;
    --border:    #2a2a32;
    --gold:      #c9a84c;
    --gold-dim:  #8a6e2f;
    --amber:     #e8b86d;
    --text:      #e8e4dc;
    --muted:     #7a7570;
    --red:       #c0392b;
}

/* ── Global reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

[data-testid="stAppViewContainer"] {
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(201,168,76,0.07) 0%, transparent 70%),
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container { padding-top: 2rem; }

.sidebar-logo {
    text-align: center;
    padding: 1.5rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.sidebar-logo .reel {
    font-size: 2.8rem;
    display: block;
    margin-bottom: 0.3rem;
}
.sidebar-logo h2 {
    font-family: 'Playfair Display', serif;
    color: var(--gold);
    font-size: 1.4rem;
    margin: 0;
    letter-spacing: 0.05em;
}
.sidebar-logo p {
    color: var(--muted);
    font-size: 0.75rem;
    margin: 0.2rem 0 0;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* ── Slider label ── */
[data-testid="stSidebar"] label {
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: var(--gold) !important;
}
[data-testid="stSidebar"] [data-testid="stTickBar"] { color: var(--muted); }

/* ── Hero header ── */
.hero {
    text-align: center;
    max-width: 760px;
    margin: 0 auto;
    padding: 3.5rem 1rem 2.5rem;
    position: relative;
}
.hero::after {
    content: '';
    display: block;
    width: 80px;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 1.5rem auto 0;
}
.hero-eyebrow {
    font-size: 0.72rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--gold-dim);
    margin-bottom: 0.6rem;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 700;
    color: var(--text);
    line-height: 1.1;
    margin: 0 0 0.7rem;
}
.hero h1 em {
    font-style: italic;
    color: var(--amber);
}
.hero-sub {
    color: var(--muted);
    font-size: 0.95rem;
    font-weight: 300;
    max-width: 620px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Search area ── */
.search-wrap {
    max-width: 720px;
    margin: 0 auto 2.5rem;
    padding: 0 1rem;
}

[data-testid="stTextArea"] label {
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}
[data-testid="stTextArea"] textarea {
    background-color: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    line-height: 1.6 !important;
    transition: border-color 0.2s;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--gold-dim) !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.08) !important;
}
[data-testid="stTextArea"] textarea::placeholder { color: var(--muted) !important; }

/* ── Primary button ── */
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #b8922a 0%, #c9a84c 50%, #d4b86a 100%) !important;
    color: #0a0a0b !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 2.2rem !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 20px rgba(201,168,76,0.25) !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Results header ── */
.results-header {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    margin: 0.5rem 0 1.6rem;
    padding-bottom: 0.9rem;
    border-bottom: 1px solid var(--border);
}
.results-header h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: var(--text);
    margin: 0;
}
.results-count {
    background: rgba(201,168,76,0.12);
    border: 1px solid var(--gold-dim);
    color: var(--gold);
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    letter-spacing: 0.06em;
}

/* ── Movie card ── */
.movie-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.1rem;
    position: relative;
    transition: border-color 0.2s, transform 0.2s;
    overflow: hidden;
}
.movie-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, var(--gold) 0%, var(--gold-dim) 100%);
    border-radius: 3px 0 0 3px;
    opacity: 0;
    transition: opacity 0.2s;
}
.movie-card:hover {
    border-color: var(--gold-dim);
    transform: translateX(3px);
}
.movie-card:hover::before { opacity: 1; }

.card-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 0.7rem;
}
.card-rank {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 2rem;
    color: var(--border);
    line-height: 1;
    flex-shrink: 0;
    margin-top: 0.1rem;
    min-width: 2.5rem;
}
.card-title-wrap { flex: 1; }
.card-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text);
    margin: 0 0 0.3rem;
    line-height: 1.25;
}
.card-genres {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 0;
}
.genre-tag {
    background: rgba(201,168,76,0.08);
    border: 1px solid rgba(201,168,76,0.2);
    color: var(--gold-dim);
    font-size: 0.7rem;
    padding: 0.15rem 0.55rem;
    border-radius: 4px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-weight: 500;
}
.card-score-badge {
    flex-shrink: 0;
    text-align: right;
}
.score-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    line-height: 1;
}
.score-label {
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    display: block;
}
.card-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 0.9rem 0;
}
.card-description {
    color: #9e9a94;
    font-size: 0.92rem;
    line-height: 1.7;
    font-weight: 300;
    margin: 0;
}

/* ── Score bar ── */
.score-bar-wrap { margin-top: 1rem; }
.score-bar-bg {
    height: 3px;
    background: var(--border);
    border-radius: 2px;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(90deg, var(--gold-dim), var(--amber));
    transition: width 0.6s ease;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Sidebar API info ── */
.api-info {
    margin-top: 2rem;
    padding: 1rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 8px;
}
.api-info p {
    font-size: 0.72rem;
    color: var(--muted);
    margin: 0;
    line-height: 1.6;
    letter-spacing: 0.03em;
}
.api-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #2ecc71;
    margin-right: 5px;
    vertical-align: middle;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="reel">🎬</span>
        <h2>CineMatch</h2>
        <p>AI Recommendation Engine</p>
    </div>
    """, unsafe_allow_html=True)

    top_k = st.slider(
        "Recommendations",
        min_value=1, max_value=10, value=5,
        help="Number of movies to return"
    )

    st.markdown(f"""
    <div class="api-info">
        <p><span class="api-dot"></span>Backend API</p>
        <p style="margin-top:0.3rem; color:#555;">{API_URL}</p>
    </div>
    """, unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <p class="hero-eyebrow">Powered by AI</p>
    <h1>Find Your Next<br><em>Perfect Film</em></h1>
    <p class="hero-sub">Describe a mood, genre, story idea, or a movie you love — and let AI find what to watch next.</p>
</div>
""", unsafe_allow_html=True)

# ── Search ───────────────────────────────────────────────────────────────────
_, col, _ = st.columns([1, 2, 1])
with col:
    query = st.text_area(
        "What are you in the mood for?",
        placeholder="e.g. emotional sci-fi with a twist ending, feel-good animation for the family, gritty 90s crime thriller...",
        height=110,
        label_visibility="visible",
    )
    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    search = st.button("✦  Find Movies", type="primary", use_container_width=True)

# ── Results ──────────────────────────────────────────────────────────────────
if search:
    if not query.strip():
        st.warning("Please describe what you're in the mood for.")
    else:
        with st.spinner("Searching the cinematic universe..."):
            try:
                response = requests.post(
                    f"{API_URL}/recommend",
                    json={"query": query, "top_k": top_k},
                    timeout=10,
                )
                response.raise_for_status()
                data = response.json()
                movies = data["recommendations"]

                _, rcol, _ = st.columns([1, 2, 1])
                with rcol:
                    st.markdown(f"""
                    <div class="results-header">
                        <h2>Recommended Films</h2>
                        <span class="results-count">{len(movies)} results</span>
                    </div>
                    """, unsafe_allow_html=True)

                    for idx, movie in enumerate(movies, start=1):
                        score = min(movie["score"], 1.0)
                        score_pct = int(score * 100)

                        # Format colour by score
                        if score_pct >= 80:
                            score_color = "#c9a84c"
                        elif score_pct >= 60:
                            score_color = "#8a6e2f"
                        else:
                            score_color = "#555"

                        # Genre tags HTML
                        raw_genres = movie.get("genres", "")
                        genre_list = [g.strip() for g in raw_genres.split("|") if g.strip()]
                        if not genre_list:
                            genre_list = [raw_genres] if raw_genres else []
                        genre_html = "".join(f'<span class="genre-tag">{g}</span>' for g in genre_list)

                        st.markdown(f"""
                        <div class="movie-card">
                            <div class="card-top">
                                <span class="card-rank">#{idx:02d}</span>
                                <div class="card-title-wrap">
                                    <p class="card-title">{movie['title']}</p>
                                    <div class="card-genres">{genre_html}</div>
                                </div>
                                <div class="card-score-badge">
                                    <span class="score-value" style="color:{score_color}">{score_pct}%</span>
                                    <span class="score-label">match</span>
                                </div>
                            </div>
                            <hr class="card-divider">
                            <p class="card-description">{movie['description']}</p>
                            <div class="score-bar-wrap">
                                <div class="score-bar-bg">
                                    <div class="score-bar-fill" style="width:{score_pct}%"></div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            except requests.exceptions.ConnectionError:
                st.error("⚠️  Cannot reach the backend API. Make sure FastAPI is running: `uvicorn backend.main:app --reload`")
            except requests.exceptions.RequestException as error:
                st.error(f"Request failed: {error}")
