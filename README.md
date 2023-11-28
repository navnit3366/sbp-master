# Analiza podataka iz igrice Pokemon Go

Projekat za predmet sistemi baza podataka

### Opis
[Pokémon GO](https://www.pokemongo.com/en-us/ "Pokémon GO homepage") je AR mobilna igra. Igra koristi GPS kako bi omogućila igraču da pronađe i uhvati pokemona. Igraču se prikazuju pokemoni na njegovoj stvarnoj lokaciji, a uticaj na to kog pokemona će igrač sresti ima više faktora. Neki od faktora su:
* osobine pokemona, poput tipa i snage
* karakteristike lokacije na kojoj se nalazi igrač
* vremenske prilike.
<br/>

U okviru projekta iskorišteni su podaci o pokemonima i susretima kako bi se ispitale veze između susreta i ostalih faktora, te dali odgovori na pitanja kao što su:
* Po kom vremenu se najviše pojavljuje koji tip pokemona?
* Koji pokemoni se najčešće pojavljuju sa Bulbasaurom?
* Koji pokemoni su se pojavili samo na jednom kontinentu?

### Korišteni podaci
U projektu su korišteni set podataka sa osobinama pokemona i set pokemona sa zabeleženim susretima. Setove podataka i informacije o njima moguće je pronaći na sledećim linkovima:
 * [Set podataka o pokemonima](https://www.kaggle.com/alopez247/pokemon "Pokémon for Data Mining and Machine Learning")
 * [Set podataka o susretima](https://www.kaggle.com/semioniy/predictemall "Predict'em All")
 
 ### Potrebno pre pokretanja
 1. *MongoDB, verzija 4.0.10*. Za više informacije [pogledati ovde](https://www.mongodb.com/download-center "MongoDB Download Center")
 2. *Python 3.6.5*
 3. *PyMongo 3.8.0*
 4. *Studio 3T 2019.3.0* ili drugi odgovarajući MongoDB GUI.
 
 ### Pokretanje
 1. Skinuti csv fajlove. Kreirati data folder i u njega staviti csv fajlove preimenovane u pokemon.csv i encounters.csv (ili promeniti
 nazive fajlova koji se koriste u *scripts/fill_database.py* na odgovarajuće.
 2. Pokrenuti mongo u lokalu na portu 27017 i kreirati bazu sa nazivom sbp.
 3. Pokrenuti skriptu koja kreira kolekcije pokemon i encounters. Pozicionirati se u folder *scripts* i pokrenuti: <br/> 
	 <code>
		python fill_database.py
	 </code>
 4. Željeni upit kopirati iz fajla *upiti.md* i pokrenuti u okviru *Studio 3T*
