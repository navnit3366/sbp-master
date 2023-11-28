import pymongo
import csv
import encounter_model
from parse_pokemon import Pokemon_Parser

class Encounters_Parser():
    def __init__(self, encounters_file, pokemon_file) -> None:
        self._encounters_file = encounters_file
        self._encounters = dict()
        self._pokemon_parser = Pokemon_Parser(pokemon_file) 
        self._pokemon_parser.prepare_previews()

    def add_encounters_to_db(self, url, db_name) -> None:
        """Add all encounters from given file to database."""
        #make db ready        
        client = pymongo.MongoClient(url)
        db = client[db_name]     
        with open(self._encounters_file, mode ='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                new_encounter = encounter_model.get_encounter(row)
                #replace id with more data
                new_encounter['EncounterInfo']['Pokemon'] = self._pokemon_parser.get_pokemon_preview(new_encounter['EncounterInfo']['Pokemon'])
                #add coencounters
                new_encounter['EncounterInfo']['Coencounters'] = []
                for coen in encounter_model.get_nearby_pokemon(row):
                    new_encounter['EncounterInfo']['Coencounters'].append(self._pokemon_parser.get_pokemon_preview(coen))      
                #add encounter to document it belongs to
                key = str(new_encounter['CommonInfo']['Day']) + ' ' + str(new_encounter['CommonInfo']['Month'])+ ' ' + str(new_encounter['CommonInfo']['Year']) + ' ' + new_encounter['CommonInfo']['City']  + ' ' + new_encounter['CommonInfo']['Continent'] 
                if key not in self._encounters:
                    new_file = {
                        'CommonInfo': new_encounter['CommonInfo'],
                        'Encounters': [new_encounter['EncounterInfo']]
                    }
                    self._encounters[key] = new_file
                else:
                    if len(self._encounters[key]['Encounters']) > 150:
                        db['encounters'].insert_one(self._encounters[key])
                        del self._encounters[key]
                        new_file = {
                            'CommonInfo': new_encounter['CommonInfo'],
                            'Encounters': [new_encounter['EncounterInfo']]
                        }
                        self._encounters[key] = new_file
                    else:
                        self._encounters[key]['Encounters'].append(new_encounter['EncounterInfo'])
                
        #insert all encounters to db collection encounters
        encounters = [record for record in self._encounters.values()]
        db['encounters'].insert_many(encounters)