import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get("poster_path", None)
        if poster_path:
            poster_url = f"http://image.tmdb.org/t/p/w185/{poster_path}"
            return poster_url
        else:
            return None
    else:
        return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    for i in movies_list:
        movie_id = i[0]
        poster_url = fetch_poster(movie_id, "ef5a52c5a7905217853c5888224c4819")  # Replace with your actual API key
        if poster_url:
            recommend_movies.append((movies.iloc[i[0]]['title'], poster_url))
    return recommend_movies

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    st.write("Recommended Movies:")
    row = st.columns(len(recommendations))  # Create columns dynamically based on the number of movies
    for i, (movie, poster_url) in enumerate(recommendations):
        row[i].write(f"Movie: {movie}")
        row[i].image(poster_url, width=150, use_column_width=True)
