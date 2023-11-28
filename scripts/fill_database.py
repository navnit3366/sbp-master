from parse_pokemon import Pokemon_Parser
from parse_encounters import Encounters_Parser
import pymongo


if __name__ == '__main__':

    print('Inserting pokemon')
    pokemon_parser = Pokemon_Parser(pokemon_file = 'data/csv/pokemon.csv' )
    pokemon_parser.add_pokemon_to_db(url = 'mongodb://localhost:27017/', db_name = 'sbp')

    print('Inserting encounters')
    encounters_parser = Encounters_Parser(encounters_file = 'data/csv/encounters.csv', pokemon_file = 'data/csv/pokemon.csv')
    encounters_parser.add_encounters_to_db(url = 'mongodb://localhost:27017/', db_name = 'sbp')