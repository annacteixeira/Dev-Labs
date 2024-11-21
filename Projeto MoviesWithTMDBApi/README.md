# TMDB Movie Recommender

![TMDB Logo](https://www.themoviedb.org/assets/2/v4/logos/v2/blue_long_1-8ba2ac31f354005783fab473602c34c3f4fd207150182061e425d366e4f34596.svg)

Este projeto é um programa em Python que utiliza a [API TMDB](https://www.themoviedb.org/) para recomendar os 10 melhores filmes semelhantes ao filme informado pelo usuário. O objetivo é oferecer sugestões de filmes baseadas na pontuação média de popularidade.

## Projeto Original
O projeto original pode ser encontrado no GitHub do professor [João Paulo Aramuni](https://github.com/joaopauloaramuni/python/tree/main/PROJETOS/Projeto%20MoviesWithTMDBApi). 

O meu projeto possui algumas diferenças

## Funcionalidades

- Pesquisa o ID de um filme a partir do seu nome.
- Obtém uma lista de filmes semelhantes utilizando a API TMDB.
- Classifica e exibe os 10 melhores filmes semelhantes, com base na pontuação média (`vote_average`).

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Requests**: Biblioteca para realizar chamadas HTTP.

## Requisitos

1. **Python 3.7 ou superior**
2. **Biblioteca `requests`**
   - Instale usando:
     ```bash
     pip install requests
     ```

3. **Chave de API do TMDB**
   - Crie uma conta em [TMDB](https://www.themoviedb.org/).
   - Acesse [Configurações de API](https://www.themoviedb.org/settings/api) e gere uma chave de API.

## Configuração

1. Clone este repositório ou copie o código.
2. Substitua a variável `API_KEY` no código pela sua chave de API do TMDB:
   ```python
   API_KEY = 'sua_chave_api_aqui'

## Como Executar

1. Execute o script em Python:
python3 tmdb_recommender.py

2. Insira o nome de um filme quando solicitado.

## Exemplo de uso:
- Entrada:
Informe o nome de um filme: Harry Potter

- Saída:
Os 10 melhores filmes semelhantes a 'Harry Potter':
1. Fantastic Beasts and Where to Find Them (Nota: 7.3, Lançamento: 2016-11-16)
2. Fantastic Beasts: The Crimes of Grindelwald (Nota: 6.9, Lançamento: 2018-11-14)
3. Percy Jackson & the Olympians: The Lightning Thief (Nota: 6.2, Lançamento: 2010-02-01)
...

## Estrutura do Código

get_movie_id(movie_name):
Busca o ID de um filme pelo nome utilizando a API TMDB.

get_similar_movies(movie_id):
Retorna uma lista de filmes semelhantes com base no ID informado.

recommend_movies(movie_name):
Exibe os 10 melhores filmes semelhantes, ordenados pela nota.

## Possíveis problemas e soluções
Erro: Import "requests" could not be resolved from source
Certifique-se de que o pacote requests está instalado no ambiente correto: pip install requests

Erro: Invalid API key
Verifique se a chave de API foi configurada corretamente no código.

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.