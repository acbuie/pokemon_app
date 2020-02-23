import sys

import requests
from bs4 import BeautifulSoup

from pokemon import Pokemon

#######################################################################################################
# encoding wrapper function for printing


# def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
#     enc = file.encoding
#     if enc == 'UTF-8':
#         print(*objects, sep=sep, end=end, file=file)
#     else:
#         def f(obj): return str(obj).encode(
#             enc, errors='backslashreplace').decode(enc)
#         print(*map(f, objects), sep=sep, end=end, file=file)


########################################################################################################
pokemondb_url = 'https://pokemondb.net'


source = requests.get(f'{pokemondb_url}/pokedex/national').text
soup = BeautifulSoup(source, 'lxml')

pokemonPages = []
for generation in soup.main.find_all('div', class_='infocard-list infocard-list-pkmn-lg'):

    for pokemon in generation.find_all('div', class_='infocard'):
        href = pokemon.a.get('href')
        pokemon_url = f'{pokemondb_url}{href}'
        pokemonPages.append(pokemon_url)
        # sprite = pokemon.a.find('span')
        # print(sprite.get('data-src'))


for pokemon in pokemonPages:
    name = pokemon.split('/')[-1]
    print(name.capitalize())
