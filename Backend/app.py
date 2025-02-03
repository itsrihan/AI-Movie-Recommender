import os
import pandas as pd
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

#zero-shot-classification
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

candidate_labels = [
    'Action', 'Comedy', 'Drama', 'Thriller', 'Horror', 'Romance', 'Musical', 'Fantasy', 'IMAX',
    'Children', 'Sci-Fi', 'Adventure', 'Mystery', 'War', 'Documentary', 'Crime',
    'Film-Noir', 'Western'
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
movies_path = os.path.join(BASE_DIR, ".gitignore", "movies.csv")
ratings_path = os.path.join(BASE_DIR, ".gitignore", "ratings.csv")

movies = pd.read_csv(movies_path)
ratings = pd.read_csv(ratings_path)

movie_ratings = ratings.groupby('movieId').agg({'rating': 'mean', 'userId': 'count'}).reset_index()
movie_ratings.rename(columns={'userId': 'num_ratings'}, inplace=True)  # Rename

movies = movies.merge(movie_ratings, on='movieId', how='left')

def classify_user_input(prompt):
    result = classifier(prompt, candidate_labels)
    
    # Adjust threshold 
    threshold = 0.10
    detected = [label for label, score in zip(result['labels'], result['scores']) if score > threshold]
    return detected


app = Flask(__name__)
CORS(app)  

@app.route('/recommend', methods=['POST']) 
def recommend():
    data = request.get_json()
    prompt = data.get('prompt', '').lower()

    
    refined_keywords = classify_user_input(prompt)

    print("Detected Keywords:", refined_keywords)

    # Filter movies
    filtered_movies = movies
    if refined_keywords:
        
        filtered_movies['match_count'] = filtered_movies['genres'].apply(
            lambda genres: sum(genre in genres for genre in refined_keywords)
        )       
        filtered_movies['match_all'] = filtered_movies['match_count'] == len(refined_keywords)
        all_match_movies = filtered_movies[filtered_movies['match_all']]

        if not all_match_movies.empty:           
            top_movie = all_match_movies.sort_values(by=['rating', 'num_ratings'], ascending=[False, False]).head(1)
        else:
            top_movie = filtered_movies.sort_values(by=['match_count', 'rating', 'num_ratings'], ascending=[False, False, False]).head(1)

    if not top_movie.empty:
        recommend_movies = top_movie.iloc[0]['title']
        genres = top_movie.iloc[0]['genres']
    else:
        recommend_movies = "No movies found"
        genres = "n/a"
#log
    log_entry = (
        f"Timestamp: {datetime.datetime.now()}\n"
        f"User Input: {prompt}\n"
        f"Refined Keywords Detected: {refined_keywords}\n"
        f"Output: {recommend_movies}\n"
        f"Movies Genres: {genres}\n"
        f"{'-'*50}\n"
    )

    log_dir = "test"
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, 'log.txt'), 'a') as log_file:
        log_file.write(log_entry)

    return jsonify({'recommendation': recommend_movies})

if __name__ == '__main__':
    app.run(debug=True)
