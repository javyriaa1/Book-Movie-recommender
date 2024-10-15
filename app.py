import pandas as pd
from collections import defaultdict
import streamlit as st

# Load the data
books = pd.read_csv('books.csv')  # Load your books data
movies = pd.read_csv('movies.csv')  # Load your movies data

# Limit to 4000 books and 4000 movies
books = books.head(4000)
movies = movies.head(4000)

# Extract keywords from genres
def extract_keywords(df, genre_column):
    keyword_mapping = defaultdict(set)
    
    for index, row in df.iterrows():
        genres = str(row[genre_column]).split(',')
        for genre in genres:
            keywords = genre.strip().lower().split()
            for keyword in keywords:
                keyword_mapping[keyword].add(genre.strip().lower())
    
    return keyword_mapping

# Extract keywords
book_keywords = extract_keywords(books, 'genres')
movie_keywords = extract_keywords(movies, 'genres')

# Recommendation function
def recommend_based_on_genre(selected_genre):
    selected_keywords = selected_genre.lower().strip().split(',')
    
    recommended_books = set()
    recommended_movies = set()
    
    for keyword in selected_keywords:
        keyword = keyword.strip()
        if keyword in book_keywords:
            genres = book_keywords[keyword]
            for genre in genres:
                # Filter the books by genre and add their titles
                titles = books[books['genres'].str.contains(genre, case=False, na=False)]['Title']
                recommended_books.update(titles.tolist())  # Convert to list and update the set
        if keyword in movie_keywords:
            genres = movie_keywords[keyword]
            for genre in genres:
                # Filter the movies by genre and add their titles
                titles = movies[movies['genres'].str.contains(genre, case=False, na=False)]['title']
                recommended_movies.update(titles.tolist())  # Convert to list and update the set
    
    return recommended_books, recommended_movies

# Streamlit app
st.title("Book and Movie Recommendation System")

# User input
selected_genre = st.text_input("Enter genres (e.g., Fantasy, Magic):")

if st.button("Get Recommendations"):
    if selected_genre:
        recommended_books, recommended_movies = recommend_based_on_genre(selected_genre)
        
        st.subheader("Recommended Books:")
        if recommended_books:
            for book in recommended_books:
                st.write(book)
        else:
            st.write("No recommendations found for books.")

        st.subheader("Recommended Movies:")
        if recommended_movies:
            for movie in recommended_movies:
                st.write(movie)
        else:
            st.write("No recommendations found for movies.")
    else:
        st.write("Please enter a genre.")
