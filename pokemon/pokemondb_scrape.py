import requests
import re
from bs4 import BeautifulSoup

from utility import StopWatch
from utility import find_substring
from utility import make_soup

class Scrape_Master:
    """
    Class from which all other methods will inherit. Experimenting with class 
    inheritance. 
    """
    pass

# All other data must come from serebii.net, pokemondb.net doesn't like scrapers
class Scrape_Sprites:
    """
    The sprites may be scraped from pokemondb.net. 
    """
    pass

class Scrape_Pokemon:
    """
    Scrapes the pokemon data
    """
    pass

class Scrape_Moves:
    """
    Scrapes the moves
    """
    pass

class Scrape_Items:
    """
    Scrapes the items
    """
    pass

class ScrapingMethods:
    """
    Class for handling scraping (i.e. updating) the data pulled from PokemonDB. 
    Instantiate to populate necessary urls. Each method scrapes some sort of 
    information from the site, and should be run sequentially. 
    """

    def __init__(self, POKEMONDB_URL):
        self.POKEMONDB_URL = POKEMONDB_URL
        self.NATIONAL_DEX_URL = f'{POKEMONDB_URL}/pokedex/national'
        self.SPRITE_URL = f'{POKEMONDB_URL}/sprites'

    def scrape_name(self):
        """
        Takes 'https://pokemondb.net/pokedex/national' and updates the 
        self.page_url and self.name_url lists for each pokemon in the national 
        dex as it is used by pokemondb for navigation. 
        """
        soup = make_soup(self.NATIONAL_DEX_URL, 'html.parser')
        
        pkmn_page_url = []
        gen_tiles = soup.main.find_all(
            'div', 
            class_ = 'infocard-list infocard-list-pkmn-lg'
            )
        
        # For each generation, find each pokemon tile
        for gen in gen_tiles:
            
            pkmn_tiles = gen.find_all(
                'div', 
                class_ = 'infocard'
                )
            
            # For each pokemon, get the url to it's page
            for pokemon in pkmn_tiles:
                pkmn_page_url.append(pokemon.a.get('href'))

        # Get the pokemon name from it's url
        pkmn_names = [pkmn.split('/')[-1] for pkmn in pkmn_page_url]
        
        # Give these values to the instance
        self.name_url_list = pkmn_names
        self.pkmn_page_url_list = pkmn_page_url

    def scrape_sprites(self, display_output= False, record_time= True):
        """
        Returns a list of dictionaries of all sprites for all pokemon as 
        self.sprite_url_list
        """

        pkmn_sprite_dicts = {}

        for pkmn in self.name_url_list:

            GEN_LIST = [
                'gen 8',
                'gen 7',
                'gen 6',
                'gen 5',
                'gen 4',
                'gen 3',
                'gen 2',
                'gen 1'
            ]

            # Empty lists are updated with sprite urls if the pokemon has a 
            # sprite for that game
            game_dict_list = [
                {
                'home': [],
                'sword-shield': []
                }, 
                {
                'lets-go-pikachu-eevee': [],
                'ultra-sun-ultra-moon': [],
                'sun-moon': []
                }, 
                {
                'bank': [],
                'go': [],
                'omega-ruby-alpha-sapphire': [],
                'x-y': []
                }, 
                {
                'black-white-2': [],
                'black-white': []
                }, 
                {
                'heartgold-soulsilver': [],
                'platinum': [],
                'diamond-pearl': []
                }, 
                {
                'emerald': [],
                'firered-leafgreen': [],
                'ruby-sapphire': []
                }, 
                {
                'crystal': [],
                'gold': [],
                'silver': []
                },
                { 
                'yellow': [],
                'red-blue': []
                }
            ]

            # Sprite page url, updated to new pokemon each loop
            PKMN_SPRITE_URL = f'{self.SPRITE_URL}/{pkmn}'
            
            # Make soup object. Find tables that aren't history table (via 
            # class_=''...). Find all <a> from these tables. 
            soup = make_soup(PKMN_SPRITE_URL, 'html.parser')
            tables = soup.body.main.find_all(
                'table', 
                class_= 'data-table sprites-table block-wide')
            
            for table in tables:
                a = table.find_all('a')
                # Pull url, place into correct spot in dictionary. 
                for tag in a:
                    url = tag.get('href')
                    
                    game = find_substring(
                        'sprites/', 
                        '/',
                        url,
                        ''
                        )

                    for gen in game_dict_list:
                        if game in gen.keys():
                            gen[f'{game}'].append(url)

            # Completed individual pokemon sprite url dictionary
            pkmn_sprite_dict = dict(zip(GEN_LIST, game_dict_list))

            pkmn_sprite_dicts[f'{pkmn}'] = pkmn_sprite_dict

            if record_time:
                t.lap(store= True)
            elif display_output:
                print(f'Working... {pkmn}')

        self.sprite_url_list = pkmn_sprite_dicts

if __name__ == "__main__":
    POKEMONDB_URL = 'https://pokemondb.net'

    t = StopWatch()
    
    scraper = ScrapingMethods(POKEMONDB_URL)

    scraper.scrape_name()

    t.start()
    scraper.scrape_sprites(display_output= False)
    end_time = t.stop()
    
    print(
        f'Total time: {end_time / 60:.1f} Minutes ({end_time:0.1f} Seconds), ' \
        f'Average loop: {t.average_lap:0.4f} Seconds')

    print(scraper.sprite_url_list['bulbasaur'])
