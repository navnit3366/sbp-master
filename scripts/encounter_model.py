from dateutil import parser

def get_common_info(row) -> dict:
    #some continets have state added to them and their format is continent/state (etc. America/Argentina)
    #removing state
    continent = row['continent']
    dash_index = continent.find('/')
    if dash_index != -1:
        continent = continent[:dash_index]
    return {
        'Continent': continent,
        'City': row['city'].replace('_', ' '),
        'Day': int(row['appearedDay']),
        'Month': int(row['appearedMonth']),
        'Year': int(row['appearedYear']),
        'DayOfWeek': row['appearedDayOfWeek']
    }

def get_encounter(row) -> dict:
    return {
        'CommonInfo': get_common_info(row),
        'EncounterInfo': {
            'Pokemon': int(row['pokemonId']),
            'Location': get_location(row),
            'Time': get_time(row),
            'Weather': get_weather(row),
            'NearbyObjects': get_nearby_objects(row)
        }
    }

def get_location(row) -> dict:
    area_type = ""
    if row['urban'] == 'true' :
        area_type = 'Urban'
    elif row['suburban'] == 'true' :
        area_type = 'Suburban'
    elif row['midurban'] == 'true' :
        area_type = 'Midurban'
    else:
        area_type = 'Rural'

    return {
        'GeoLocation': {
            'type': 'Point',
            'coordinates': [float(row['longitude']), float(row['latitude'])]
        },
        'TerrainType': int(row['terrainType']),
        'CloseToWater': bool(row['closeToWater']),
        'PopulationDensity': float(row['population_density']),
        'AreaType': area_type
    }

def get_time(row) -> dict:
    return {
        'LocalTime': parser.parse(row['appearedLocalTime']),
        'TimeOfTheDay': row['appearedTimeOfDay'],
        'Minute': int(row['appearedMinute']),
        'Hour': int(row['appearedHour']),
        'MinutesSinceSinerise': int(row['sunriseMinutesSince']),
        'MinutesBeforeSunset': int(row['sunsetMinutesBefore'])
    }

def get_weather(row) -> dict:
    return {
        'Weather': row['weather'],
        'WeatherIcon': row['weatherIcon'],
        'Temperature': float(row['temperature']),
        'WindSpeed': float(row['windSpeed']),
        'WindBearing': float(row['windBearing']),
        'Pressure': float(row['pressure']),
    }

def get_nearby_objects(row) -> dict:
    distances = [100, 250, 500, 1000, 2500, 5000]
    closestGym = 0.0
    closestPokestop = 0.0
    try:
        closestGym = float(row['gymDistanceKm'])
    except ValueError:
        closestGym = -1.0
    try:
        closestPokestop = float(row['pokestopDistanceKm'])
    except ValueError:
        closestPokestop = -1.0
    
    return {
        'ClosestGym': closestGym,
        'ClosestPokestop': closestPokestop,
        'NearbyGyms': get_true_terms_list(row, 'gymIn', 'm', distances),
        'NearbyPokestops': get_true_terms_list(row, 'pokestopIn', 'm', distances)
    }

def get_nearby_pokemon(row) -> list:
    ids = list(range(1, 151))
    return get_true_terms_list(row, 'cooc_', '', ids)

def get_true_terms_list(row, pre_distance_name, post_distance_name, terms) -> list:
    ret = []
    for term in terms:        
        searchString = pre_distance_name + str(term) + post_distance_name
        if row[searchString] == 'true':
           ret.append(term)
    return ret


