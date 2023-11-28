import csv
import pymongo
import pokemon_model

class Pokemon_Parser():
    def __init__(self, pokemon_file) -> None:
        self._pokemon_file = pokemon_file

    def add_pokemon_to_db(self, url, db_name) -> None:
        """Add all pokemon from given file to database."""
        #make db ready        
        client = pymongo.MongoClient(url)
        db = client[db_name]
        #read all pokemon from csv and convert them to json
        pokemon = []       
        with open(self._pokemon_file, mode ='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                new_pokemon = pokemon_model.get_pokemon(row)
                pokemon.append(new_pokemon)
        #insert all pokemon to db collection pokemon
        db['pokemon'].insert_many(pokemon)

    def prepare_previews(self) -> None:
        """Prepares preview of pokemon"""
        self._pokemon_previews = {}
        with open(self._pokemon_file, mode ='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:                                
                #only pokemon from generation 1 appear in encounters
                generation = int(row['Generation'])
                if generation != 1:
                    break
                pokemon_id = int(row['Number'])
                new_pokemon = pokemon_model.get_pokemon_preview(row)
                self._pokemon_previews[pokemon_id] = new_pokemon

    def get_pokemon_preview(self, pokemon_id: int) -> dict:
        """Get preview with basic stats for pokemon with given id."""
        return self._pokemon_previews[pokemon_id]