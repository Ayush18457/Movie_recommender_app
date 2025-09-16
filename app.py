import streamlit as st
import pickle
import pandas as pd

def recommend(movie):
    """Recommends 5 movies based on the selected movie."""
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        for i in distances:
            recommended_movies.append(movies.iloc[i[0]].title)
        return recommended_movies
    except (IndexError, KeyError):
        return []

# --- Main App ---
st.title('Movie Recommender System')

# Load the data files
try:
    movies = pd.DataFrame(pickle.load(open('model.pkl', 'rb')))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Error: Make sure 'movies.pkl' and 'similarity.pkl' are in the same folder.")
    st.stop()


# Create a dropdown for movie selection
selected_movie = st.selectbox(
    "Type or select a movie to get a recommendation",
    movies['title'].values
)

# Button to show recommendations
if st.button('Show Recommendation'):
    recommendations = recommend(selected_movie)
    if recommendations:
        st.subheader('Recommended for you:')
        for movie_title in recommendations:
            st.write(movie_title)
    else:
        st.warning("Could not find recommendations for the selected movie.")
