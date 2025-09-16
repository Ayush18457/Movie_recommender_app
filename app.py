import streamlit as st
import pickle
import pandas as pd

# Function to get recommendations
def recommend(movie):
    """
    Takes a movie title and returns a list of 5 recommended movie titles.
    """
    try:
        # Find the index of the movie in the dataframe
        movie_index = movies[movies['title'] == movie].index[0]
        
        # Get the similarity scores for the movie
        distances = similarity[movie_index]
        
        # Sort the movies based on similarity, get top 5
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        for i in movies_list:
            recommended_movies.append(movies.iloc[i[0]].title)
        return recommended_movies
    except IndexError:
        return []

# --- Load Data ---
# Load the movies dataframe
try:
    movies_dict = pickle.load(open('movies.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
except FileNotFoundError:
    st.error("The 'movies.pkl' file was not found. Please make sure it's in the same directory.")
    st.stop()

# Load the similarity matrix
try:
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("The 'similarity.pkl' file was not found. Please generate it from your notebook.")
    st.stop()


# --- Streamlit Web App Interface ---

st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .stApp {
        background-color: #1a1a1a;
        color: #e6e6e6;
    }
    .stSelectbox > div > div > div {
        background-color: #333333;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
    }
    h1 {
        color: #007bff;
    }
    .movie-title {
        font-size: 1.1em;
        font-weight: bold;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title('Movie Recommender System')

# Movie selection dropdown
selected_movie_name = st.selectbox(
    "Type or select a movie you like:",
    movies['title'].values
)

# Recommend button
if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    if recommendations:
        st.success(f"Because you watched '{selected_movie_name}', you might also like:")
        
        # Display recommendations in columns
        cols = st.columns(5)
        for i, movie_title in enumerate(recommendations):
            with cols[i]:
                st.markdown(f"<div class='movie-title'>{movie_title}</div>", unsafe_allow_html=True)
                # You can add movie posters here in the future if you have the image URLs
                # st.image("poster_url.jpg")
    else:
        st.warning("Could not find recommendations for the selected movie.")
