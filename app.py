from flask import Flask, render_template, request, redirect, url_for, abort
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast
import os
import pickle
import sys

app = Flask(__name__)

# Configuration
DATA_PATH = 'data/anime-dataset-2023.csv'
MODEL_PATH = 'models/content_based_model.pkl'

def parse_genres(x):
    if pd.isnull(x):
        return []
    try:
        return ast.literal_eval(x)
    except (ValueError, SyntaxError):
        return [genre.strip() for genre in x.split(',')]

def load_data():
    if not os.path.exists(DATA_PATH):
        print(f'Error: Dataset not found at {DATA_PATH}')
        print('Please download the dataset and place it in the data/ directory.')
        sys.exit(1)
        
    try:
        anime = pd.read_csv(DATA_PATH)
        anime = anime[~anime['Genres'].isna()]  
        anime['Genres'] = anime['Genres'].apply(parse_genres)
        anime['Score'] = pd.to_numeric(anime['Score'], errors='coerce').fillna(0)
        anime['Synopsis'] = anime['Synopsis'].fillna('')
        anime['Type'] = anime['Type'].fillna('Unknown')
        anime['Image URL'] = anime['Image URL'].fillna('UNKNOWN')
        return anime
    except Exception as e:
        print(f'Error loading data: {e}')
        sys.exit(1)

def preprocess_data(anime):
    anime['genre_str'] = anime['Genres'].apply(lambda x: ' '.join(x))
    # Give heavy weight to Name (for sequels/seasons), moderate weight to genres/type, light weight to synopsis
    # Repeat Name 5x, Genres 3x, Type 3x to ensure high similarity for same-series shows
    anime['content'] = (anime['Name'] + ' ' + anime['Name'] + ' ' + anime['Name'] + ' ' + anime['Name'] + ' ' + anime['Name'] + ' ' +
                       anime['genre_str'] + ' ' + anime['genre_str'] + ' ' + anime['genre_str'] + ' ' +
                       anime['Type'] + ' ' + anime['Type'] + ' ' + anime['Type'] + ' ' +
                       anime['Synopsis'])
    return anime

def create_model(anime):
    # Use more permissive parameters to capture show-specific terms
    # min_df=2: word must appear in at least 2 anime (catches show-specific terms)
    # max_df=0.85: exclude words in more than 85% of anime (too common)
    # max_features=5000: keep top 5000 most important features
    tfidf = TfidfVectorizer(stop_words='english', max_df=0.85, min_df=2, max_features=5000)
    tfidf_matrix = tfidf.fit_transform(anime['content'])
    return cosine_similarity(tfidf_matrix, tfidf_matrix)

# Initialize Data and Model
try:
    if not os.path.exists(MODEL_PATH):
        os.makedirs('models', exist_ok=True)
        print('Creating model... This may take a moment.')
        anime = load_data()
        anime = preprocess_data(anime)
        cosine_sim = create_model(anime)
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump((anime, cosine_sim), f)
        print('Model created and saved.')
    else:
        print('Loading existing model...')
        with open(MODEL_PATH, 'rb') as f:
            anime, cosine_sim = pickle.load(f)
        print('Model loaded.')
except Exception as e:
    print(f'Critical Error initializing app: {e}')
    # Fallback for development if model fails
    anime = pd.DataFrame()
    cosine_sim = None

def get_recommendations(title, anime, cosine_sim, n=10):
    if cosine_sim is None:
        return pd.DataFrame()
        
    matches = anime[anime['Name'].str.lower() == title.lower()]
    if matches.empty:
        return pd.DataFrame()
    
    idx = matches.index[0]
    
    # Ensure idx is within bounds of cosine_sim
    if idx >= len(cosine_sim):
        return pd.DataFrame()

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]
    
    anime_indices = [i[0] for i in sim_scores]
    recommendations = anime.iloc[anime_indices].copy()
    recommendations['similarity'] = [i[1] for i in sim_scores]
    return recommendations

@app.route('/')
def index():
    if anime.empty:
        return 'Error: Dataset or model not loaded correctly. Check server logs.', 500
    popular_anime = anime.sort_values('Score', ascending=False).head(20)
    return render_template('index.html', top_anime=popular_anime)

@app.route('/recommend/<string:anime_title>')
def recommend(anime_title):
    if anime.empty:
        return redirect(url_for('index'))
        
    matching_anime = anime[anime['Name'].str.lower() == anime_title.lower()]
    if matching_anime.empty:
        return render_template('index.html', error='Anime not found', top_anime=anime.sort_values('Score', ascending=False).head(20))
    
    anime_details = matching_anime.iloc[0].to_dict()
    recommendations = get_recommendations(anime_title, anime, cosine_sim)
    return render_template('recommendations.html',
                         anime=anime_details,
                         recommendations=recommendations)

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    if not query:
        return redirect(url_for('index'))
    
    if anime.empty:
        return redirect(url_for('index'))

    results = anime[
        anime['Name'].str.lower().str.contains(query, na=False) |
        anime['Genres'].apply(lambda x: any(query in g.lower() for g in x) if isinstance(x, list) else False) |
        anime['Synopsis'].str.lower().str.contains(query, na=False)
    ]
    return render_template('index.html', search_results=results.head(20), query=query)

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_server_error(e):
    return 'Internal Server Error', 500

if __name__ == '__main__':
    print("Starting SenpaiList...")
    print("Go to http://127.0.0.1:5000 in your browser to view the app.")
    app.run(debug=True)
