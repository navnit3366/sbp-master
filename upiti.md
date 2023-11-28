# Izvršeni upiti

### 1. U koje doba dana se desilo najviše susreta sa pokemonima? <br/>
*Rešenje:* <br/>
<pre>
  db.encounters.aggregate([	
	{$project: {"_id": 0, "TimeOfTheDay": "$Encounters.Time.TimeOfTheDay"}},
	{$unwind: "$TimeOfTheDay"},
	{$sortByCount: "$TimeOfTheDay" },
	{$limit: 1},
	{$project: {"_id": 0, "Time of the day": "$_id", "Number of encountered pokemon": "$count" } }
  ]) 
</pre>
*Rezultat:* <br/>
<pre>
{ 
    "Time of the day" : "night", 
    "Number of encountered pokemon" : NumberInt(147990)
}
</pre>

### 2. Odrediti kontinent sa najmanje i kontinent sa najviše susreta? <br/>
*Rešenje:* <br/>
<pre>
  db.encounters.aggregate([
	{$group: {
	    		"_id": "$CommonInfo.Continent", 
	    		"Count": {$sum: { $size:"$Encounters" }} 
	}},
	{$sort: {"Count": -1} },
	{$project: {"_id": 0, "Encounter.Continent": "$_id", "Encounter.Count": "$Count"}},
	{$group: {"_id": null, "EncountersPerContinent":{$push: "$Encounter"} }},
	{$project: {
	    		"_id": 0,
	    		"Continent with most encounters": { $arrayElemAt: [ "$EncountersPerContinent", 0 ] },
	    		"Continent with least encounters": { $arrayElemAt: [ "$EncountersPerContinent", -1 ] } 
	}}
  ])
</pre>
*Rezultat:* <br/>
<pre>
{ 
    "Continent with most encounters" : {
        "Continent" : "America", 
        "Count" : NumberInt(152711)
    }, 
    "Continent with least encounters" : {
        "Continent" : "Indian", 
        "Count" : NumberInt(3)
    }
}
</pre>

### 3. Za svakog pokemona odrediti ukupan broj susreta i prosečnu temperaturu prilikom susreta? <br/>
*Rešenje:* <br/>
<pre>
db.encounters.aggregate([
	{$project: {
	    		"Encounters.Pokemon.Id": 1, 
	    		"Encounters.Pokemon.Name": 1, 
	    		"Encounters.Weather.Temperature": 1
	}},
	{$unwind: "$Encounters"},
	{$group: {
	    		"_id":{"Number": "$Encounters.Pokemon.Id", "Name":"$Encounters.Pokemon.Name"}, 
	    		"Count":{$sum: 1}, 
	    		"Temperature": {$avg: "$Encounters.Weather.Temperature"}
        }},
	{$project: {
	    		"_id": 0, "Pokedex Number": "$_id.Number", 
	    		"Name":"$_id.Name", 
	    		"Number of encounters":"$Count", 
	    		"Average Temperature": "$Temperature"
	}},
	{$sort: {"Number of encounters": -1}}
])
</pre>
*Rezultat:* <br/>
<pre>
...
{ 
    "Pokedex Number" : NumberInt(115), 
    "Name" : "Kangaskhan", 
    "Number of encounters" : 34.0, 
    "Average Temperature" : 13.008823529411766
}
...
</pre>

### 4. Odrediti prosečnu udaljenost teretane i pokestopa za pokemone kojima je barem jedan od tipova vodeni? <br/>
*Rešenje:* <br/>
<pre>
db.encounters.aggregate([	
	{$project: {
	    		"Encounters.Pokemon.Type": 1, 
	    		"Encounters.NearbyObjects.ClosestGym": 1, 
	    		"Encounters.NearbyObjects.ClosestPokestop": 1
	}},
	{$unwind: "$Encounters"},
	{$match: {"Encounters.Pokemon.Type": "Water"} },
	{$group: {
	    		"_id": null, 
	    		"Average Closest Gym Distance": {$avg: "$Encounters.NearbyObjects.ClosestGym"}, 
	    		"Average Closest Pokestop Distance": {$avg: "$Encounters.NearbyObjects.ClosestPokestop"} 
	}},
	{$project: {"_id": 0} }
])
</pre>
*Rezultat:* <br/>
<pre>
{ 
    "Average Closest Gym Distance" : 1.9188675028379507, 
    "Average Closest Pokestop Distance" : 0.4771367950166632
}
</pre>

### 5. Za svako vreme odrediti 3 tipa koja su se najviše puta pojavila? <br/>
*Rešenje:* <br/>
<pre>
db.encounters.aggregate([
	{$project: {"Encounters.Pokemon.Type": 1, "Encounters.Weather.Weather": 1}},
	{$unwind: "$Encounters"},
	{$project: {"Type":"$Encounters.Pokemon.Type", "Weather":"$Encounters.Weather.Weather"}},
	{$unwind: "$Type"},	
	{$group: {"_id":{"Weather":"$Weather", "Type":"$Type"}, "Count":{$sum: 1}} },
	{$project: {"_id": "$_id.Weather", "Encounters.Type": "$_id.Type", "Encounters.Count":"$Count"} },
	{$sort: {"Encounters.Count": -1} },
	{$group: { "_id": "$_id", "EncountersByType": { $push: "$Encounters" } } },
	{$project: {
	    		"_id":0, 
	    		"Weather": "$_id", 
	    		"Most Encountered Type": { $slice: [ "$EncountersByType", 3 ] } 
	}} 
])
</pre>
*Rezultat:* <br/>
<pre>
...
{ 
    "Weather" : "BreezyandOvercast", 
    "Most Encountered Type" : [
        {
            "Type" : "Water", 
            "Count" : 66.0
        }, 
        {
            "Type" : "Normal", 
            "Count" : 64.0
        }, 
        {
            "Type" : "Poison", 
            "Count" : 63.0
        }
    ]
}
...
</pre>
### 6. Kojih 10 pokemona se najčešće pojavilo kada se pojavio Bulbasaur? <br/>
*Rešenje:* <br/>
<pre>
db.encounters.aggregate([	
	{$unwind: "$Encounters"},	
	{$project: {"Name": "$Encounters.Pokemon.Name", "Coencounters":"$Encounters.Coencounters"} },
	{$match: {"Name": "Bulbasaur"} },
	{$unwind: "$Coencounters"},
	{$project: {"_id":"$Coencounters.Name"}},
	{$group: {"_id":"$_id", "Count":{$sum: 1} }},
	{$sort: {"Count": -1}},
	{$limit: 10}
])
</pre>
*Rezultat:* <br/>
<pre>
{ 
    "_id" : "Nidoranâ™‚", 
    "Count" : 273.0
}
// ----------------------------------------------
{ 
    "_id" : "Drowzee", 
    "Count" : 189.0
}
// ----------------------------------------------
{ 
    "_id" : "Pidgey", 
    "Count" : 187.0
}
...
</pre>
### 7. Kojih 5 tipova se najčešće pojavilo kada se pojavio pokemon čiji barem jedan tip je vodeni? <br/>
*Rešenje:* <br/>
<pre>
db.encounters.aggregate([	
	{$unwind: "$Encounters"},	
	{$project: {"Type": "$Encounters.Pokemon.Type", "Coencounters":"$Encounters.Coencounters"} },
	{$match: {"Type": "Water"} },
	{$unwind: "$Coencounters"},
	{$project: {"Type": "$Coencounters.Type"} },
	{$unwind: "$Type"},
	{$group: {"_id":"$Type", "Count":{$sum: 1}}},
	{$sort: {"Count": -1}},
	{$limit: 5}
])
</pre>
*Rezulat:* <br/>
<pre>
{ 
    "_id" : "Water", 
    "Count" : 17391.0
}
// ----------------------------------------------
{ 
    "_id" : "Poison", 
    "Count" : 16492.0
}
// ----------------------------------------------
{ 
    "_id" : "Normal", 
    "Count" : 13740.0
}
...
</pre>
### 8. Koja kombinacija vremena i tipa ima najmanji broj pojava. Uzeti u obzir samo tipove koji imaju više od 10000 pojava. <br/>
*Rešenje:* <br/>
<pre>
db.encounters.aggregate([	
	{$unwind: "$Encounters"},	
	{$project: {"Type": "$Encounters.Pokemon.Type", "Weather":"$Encounters.Weather.WeatherIcon"}},	
	{$unwind: "$Type"},
	{$group: {"_id":"$Type", "TotalEncounters":{$sum: 1}, "EncountersWeather": {$push:"$Weather"} }},
	{$match: {"TotalEncounters": {$gt: 10000} }},
	{$unwind: "$EncountersWeather"},
	{$group: {"_id":{"Type":"$_id", "Weather":"$EncountersWeather"}, "Count":{$sum:1}}},
	{$sort:{"Count":1}},
	{$limit: 1},
	{$project: {"_id": 0, "Type": "$_id.Type", "Weather":"$_id.Weather", "Encounters count":"$Count"}}
])
</pre>
*Rezultat:* <br/>
<pre>
{ 
    "Type" : "Psychic", 
    "Weather" : "fog", 
    "Encounters count" : 93.0
}
</pre>

### 9. Prikazati za svaki kontinent pokemone koji su se pojavili samo na njemu. <br/>
*Rešenje:* <br/>
<pre>
db.encounters.aggregate([	
	{$unwind: "$Encounters"},
	{$project: {"Continent":"$CommonInfo.Continent", "Pokemon":"$Encounters.Pokemon.Name"}},
	{$group: {"_id":"$Pokemon", "Continents":{$addToSet: "$Continent"} }},
	{$match: {"Continents": { $size: 1 } } },
	{$unwind: "$Continents"},
	{$group: {"_id":"$Continents", "Pokemon":{$push:"$_id"} }},
	{$project: {"_id": 0, "Pokemon": 1, "Continent":"$_id"}}
])
</pre>
*Rešenje:* <br/>
<pre>
{ 
    "Pokemon" : [
        "Farfetch'd"
    ], 
    "Continent" : "Asia"
}
// ----------------------------------------------
{ 
    "Pokemon" : [
        "Raichu", 
        "Jolteon"
    ], 
    "Continent" : "America"
}
// ----------------------------------------------
{ 
    "Pokemon" : [
        "Kangaskhan"
    ], 
    "Continent" : "Australia"
}
</pre>

### 10. Pronaći pokemona primećenog najbliže Novom Sadu (koordinate:[45.267136, 19.833549]). <br/>
*Rešenje:* <br/>
<pre>
db.encounters.ensureIndex({'Encounters.Location.GeoLocation':'2dsphere'})

db.encounters.aggregate([
    { $geoNear: {
        near: {"type": "Point", "coordinates": [19.833549, 45.267136]},
        distanceField: "distance",
        includeLocs: "location",
        spherical: true
    }},
    { $redact: {
        $cond: {
            if: { $eq: [ { $ifNull: [ "$Location.GeoLocation", "$$ROOT.location" ] }, "$$ROOT.location"]},
			then: "$$DESCEND",
			else: "$$PRUNE"
        }
    }},
    {$unwind: "$Encounters"},
    {$project: {
        		"Pokemon":"$Encounters.Pokemon", 
        		"Distance":"$distance", 
        		"Continent":"$CommonInfo.Continent", 
        		"City":"$CommonInfo.City"
    }},
    {$sort: {"Distance": 1}},
    {$limit: 1}
])
</pre>
*Rezultat:* <br/>
<pre>
{ 
    "_id" : ObjectId("5d04d3037cdf7ccaab495b95"), 
    "Pokemon" : {
        "Id" : NumberInt(16), 
        "Name" : "Pidgey", 
        "Type" : [
            "Normal", 
            "Flying"
        ], 
        "Total" : NumberInt(251)
    }, 
    "Distance" : 193046.47106034038, 
    "Continent" : "Europe", 
    "City" : "Sarajevo"
}
</pre>
