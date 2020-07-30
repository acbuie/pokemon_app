class Pokemon:
    
    def __init__(self, name):
        self.name = name
        self.url = f'https://pokemondb.net/pokedex/{name}'

    def set_stats(self):
        """
        Pulls the stats from self.url. Eventually will pull from database instead
        """
    
    def set_move_tables(self):
        """
        Pulls moves from self.url. Eventually will pull from database instead.
        """