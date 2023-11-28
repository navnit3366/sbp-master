def get_pokemon(row) -> dict:
    return {
        'Id': int(row['Number']),
        'Name': row['Name'],
        'Type': get_type(row),
        'Stats': get_stats(row),
        'Generation': int(row['Generation']),
        'Legendary': bool(row['isLegendary']),
        'Gender': get_gender(row),
        'EggGroup': get_egg_group(row),
        'HasMegaEvolution': bool(row['hasMegaEvolution']),
        'Body': get_body(row),
        'CatchRate': int(row['Catch_Rate'])
    }

def get_pokemon_preview(row) -> dict:
    return {
        'Id': int(row['Number']),
        'Name': row['Name'],
        'Type': get_type(row),
        'Total': int(row['Total'])
    }

def get_type(row) -> list:
    ret = []
    if row['Type_1'] != "":
        ret.append(row['Type_1'])
    if row['Type_2'] != "":
        ret.append(row['Type_2'])
    return ret

def get_egg_group(row) -> list:
    ret = []
    if row['Egg_Group_1'] != "":
        ret.append(row['Egg_Group_1'])
    if row['Egg_Group_2'] != "":
        ret.append(row['Egg_Group_2'])
    return ret

def get_stats(row) -> dict:
    return {
        'Total': int(row['Total']),
        'HP': int(row['HP']),
        'Attack': int(row['Attack']),
        'Defense': int(row['Defense']),
        'SpAtk': int(row['Sp_Atk']),
        'SpDef': int(row['Sp_Def']),
        'Speed': int(row['Speed'])
    }

def get_body(row) -> dict:
    return {
        'Height': float(row['Height_m']),
        'Weight': float(row['Weight_kg']),
        'Color': row['Color'],
        'BodyStyle': row['Body_Style']
    }

def get_gender(row) -> dict:
    if row['hasGender'] == 'True' and row['Pr_Male'] != "":
        return {
            'hasGender': bool(row['hasGender']),
            'PrMale': float(row['Pr_Male'])
        }   
    else:
        return {
            'hasGender': bool(row['hasGender'])
        }