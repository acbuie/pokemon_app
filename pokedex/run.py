from pokedex.common.constants import POKEMONDB_URL, NATIONAL_DEX_URL
from pokedex.data_scrape.sprites import scrape_names, scrape_sprites

def run():
    """
    Does all the things to run the application. 
    """
    pkmn_names, pkmn_page_url = scrape_names(NATIONAL_DEX_URL)
    print(pkmn_names)