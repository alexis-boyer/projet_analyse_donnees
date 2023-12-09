# Projet Analyse de données
BRUSTOLIN Lucas, TREMBLEAU Thibault & BOYER Alexis

## Préambule
Rendu du projet de l'UE d'analyse de données de l'université Lyon 1. L'objectif est de fournir une visualisation de données avec les pricipaux indicateur en utilisant la librairie Python Dash.

## Donneées
Médailles de jeux olympique d'été et d'hiver entre 1896 et 2016 ([lien](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results/data))
L'ensemble des données se trouvent aussi dans le fichier data.zip et dans les fichier data\athlete_events.csv et data\noc_regions.csv

### Type de données
Les données sont les colonnes suivantes : "ID","Name","Sex","Age","Height","Weight","Team","NOC","Games","Year","Season","City","Sport","Event","Medal"
```
    ID - Unique number for each athlete
    Name - Athlete's name
    Sex - M or F
    Age - Integer
    Height - In centimeters
    Weight - In kilograms
    Team - Team name
    NOC - National Olympic Committee 3-letter code
    Games - Year and season
    Year - Integer
    Season - Summer or Winter
    City - Host city
    Sport - Sport
    Event - Event
    Medal - Gold, Silver, Bronze, or NA
```

Les données Name,Sex,Team,NOC,Games,Season,City,Sport,Event et Medal sont nominal.
Les données ID,Age,Height,Weight et Year sont ordinales

### Source
Les données ont été éxtraite du site [https://www.sports-reference.com/](https://www.sports-reference.com/).
Ce site est référencé par 135 liens éxterne, est composé de profésinel et financé par des grands groupe de sport.
![lien référent à https://www.sports-reference.com/](pictures_readme/number_of_link_sport_reference.png)

