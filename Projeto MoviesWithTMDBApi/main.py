# API: TMDB

import requests

API_KEY = 'acbf816ad3d302dc7aa9b14276628d06'
BASE_URL = 'https://api.themoviedb.org/3'

def get_movie_id(movie_name):
    url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': API_KEY,
        'query': movie_name
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            return results[0]['id']
    return None

def get_similar_movies(movie_id):
    """
    obtem uma lista de filmes semelhantes a partir do id do filme
    """
    url = f"{BASE_URL}/movie/{movie_id}/similar"
    params = {
        'api_key': API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

def recommend_movies(movie_name):
    """
    recomenda os 10 melhores filmes semelhantes ao filme informado
    """
    movie_id = get_movie_id(movie_name)
    if not movie_id:
        print("Filme não encontrado. Verifique o nome informado.")
        return

    similar_movies = get_similar_movies(movie_id)
    if not similar_movies:
        print("Nenhum filme semelhante encontrado.")
        return

    top_movies = sorted(similar_movies, key=lambda x: x['vote_average'], reverse=True)[:10]
    
    print(f"Os 10 melhores filmes semelhantes a '{movie_name}':")
    for i, movie in enumerate(top_movies, start=1):
        title = movie['title']
        rating = movie['vote_average']
        release_date = movie.get('release_date', 'Data desconhecida')
        print(f"{i}. {title} (Nota: {rating}, Lançamento: {release_date})")


if __name__ == "__main__":
    filme = input("Informe o nome de um filme: ")
    recommend_movies(filme)