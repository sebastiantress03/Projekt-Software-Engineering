# API-Documentation

## Erstellen des Turniers

    POST /tournament/

### Erklärung

Erstellung und Speicherung eines Turnierplans in eine Datenbank

### Übergabe Parameter

| Felder | Typ | Beschreibung |
| :---: | :---: | :--- |
| name | str | Name für das Turnier |
| anz_field | int | Anzahl der Spielfelder die dem Turnier zur Verfügung stehen (max 4) |
| return_match | str | Ob es Rückspiele geben soll (Beinhaltet "true" oder "false") |
| start | time | Uhrzeit wann das Turnier startet |
| period | int | Dauer eines Spiels in Minuten |
| warm_up | int | Dauer der Aufwärmzeit in Minuten |
| anz_breaks | int | Anzahl der Pausen |
| break_length | array[] | Array welches die Länge der Einzelnen Pausen beinhaltet | 
| break_length[] | int | Länge der Einzelnen Pause in Minuten | 
| break_times | array[] | Array welches die start Uhrzeiten der Pausen beinhaltet |
| break_times[] | time | start Uhrzeiten der Pause |
| anz_stages | array[] | Beinhaltet die Namen der  Leistungsgruppen (max 2) |
| anz_stages[] | str | Name der Leistungsgruppe |
| anz_teams | array[] | Beinhaltet die Anzahl an Teams in den Einzelnen |
| anz_teams[] | int | Anzahl an Teams der Leistungsgruppe |

### Übergabe Beispiel

```JSON
{
    "name": "Nikolaus Turnier 2025",
    "start": "10:00:00",
    "period": 20,
    "warm_up": 30,
    "anz_breaks": 2,
    "break_length":[30,60],
    "break_times":["12:00:00","15:00:00"],
    "anz_stages": ["Profi","Anfänger"],
    "anz_teams": [6,10]
}
```

### Mögliche Fehlermeldungen

| HTTP Code | Beschreibung |
| :---: | :--- |
| 500 | Datenbankfehler beim Hinzufügen von Daten! |
| 500 | Datenbankfehler beim Abfragen von Daten! |


## Erhalt des Turnierplans

    GET /tournament/{tournament_name}

### Erklärung

Übermittelt existierenden Turnierplan aus der Datenbank über Namen des Turniers

### Übergabe 

| Felder | Typ | Beschreibung |
| :---: | :---: | :--- |
| tournament_name | str | Name des Turniers |

### Übergabe Beispiel

```JSON
{
    "tournament_name": "Nikolaus Turnier 2025",
}
```

### Rückmeldungsfelder

| Felder | Typ | Beschreibung |
| :---: | :---: | :--- |
| tournament | array[]  | Beinhaltet ein Array welches die Einzelnen Spiele beinhaltet |
| gameID | int | Beinhaltet die ID des Spiels |
| team_name | array[3] | Beinhaltet die Namen der Teilnehmenden Teams |
| team_name[0] | str | Name von Team 1 |
| team_name[1] | str | Name von Team 2 |
| team_name[2] | str | Name vom Team das den Schiedsrichter spielt |
| score | array[2] | Beinhaltet den Aktuellen Spielstand |
| score[0] | int | Spielstand von Team 1 |
| score[1] | int | Spielstand von Team 2 |
| stage_name | str | Name der Leistungsgruppe dem die Teams angehören |
| field | int | Nummer des Spielfeldes auf dem das Spiel stattfindet |
| play_time |  time | Uhrzeit andem das Spiel stattfindet |

### Rückmeldung Beispiel

```JSON
{
    "tournament":[
        {
            "gameID": 1,
            "team_name": ["Team 1", "Team 2","Team 4"],   
            "scores": [15,20],
            "stage_name":"Profi",
            "field": 3,
            "play_time": "10:15:00"
        },
        {
            "gameID": 2,
            "team_name": ["Team 2", "Team 1","Team 4"],   
            "scores": [0,0],
            "stage_name":"Profi",
            "field": 3,
            "play_time": "10:30:00"
        },
    ]
}
```

### Mögliche Fehlermeldungen

| HTTP Code | Beschreibung |
| :---: | :--- |
| 400 | Ungültiger Turniername |
| 500 | Datenbankfehler beim Abfragen von Daten! |


## Erhalt des Turnierplans

    GET /tournament/{tournamentID}

### Erklärung

Übermittelt existierenden Turnierplan aus der Datenbank über die TurnierID

### Übergabe 

| Felder | Typ | Beschreibung |
| :---: | :---: | :--- |
| tournamentID | str | ID des Turniers als String |

### Übergabe Beispiel

```JSON
{
    "tournamentID": "4",
}
```

### Rückmeldungsfelder

| Felder | Typ | Beschreibung |
| :---: | :---: | :--- |
| tournament | array[]  | Beinhaltet ein Array welches die Einzelnen Spiele beinhaltet |
| gameID | int | Beinhaltet die ID des Spiels |
| team_name | array[3] | Beinhaltet die Namen der Teilnehmenden Teams |
| team_name[0] | str | Name von Team 1 |
| team_name[1] | str | Name von Team 2 |
| team_name[2] | str | Name vom Team das den Schiedsrichter spielt |
| score | array[2] | Beinhaltet den Aktuellen Spielstand |
| score[0] | int | Spielstand von Team 1 |
| score[1] | int | Spielstand von Team 2 |
| stage_name | str | Name der Leistungsgruppe dem die Teams angehören |
| field | int | Nummer des Spielfeldes auf dem das Spiel stattfindet |
| play_time |  time | Uhrzeit andem das Spiel stattfindet |

### Rückmeldung Beispiel

```JSON
{
    "tournament":[
        {
            "gameID": 1,
            "team_name": ["Team 1", "Team 2","Team 4"],   
            "scores": [15,20],
            "stage_name":"Profi",
            "field": 3,
            "play_time": "10:15:00"
        },
        {
            "gameID": 2,
            "team_name": ["Team 2", "Team 1","Team 4"],   
            "scores": [0,0],
            "stage_name":"Profi",
            "field": 3,
            "play_time": "10:30:00"
        },
    ]
}
```

### Mögliche Fehlermeldungen

| HTTP Code | Beschreibung |
| :---: | :--- |
| 400 | Ungültiger TurnierID|
| 500 | Datenbankfehler beim Abfragen von Daten! |


## Laden existierender Turniere

    GET /tournaments/

### Explanation

Lade existierende Turniernamen aus der Datenbank.

### Rückmeldungsfelder 

| Feld | Type | Beschreibung |
| :---: | :---: | :--- |
| tournament_name | array[] | Ein Array welches alle Existierende Turniernamen aus der Datenbank beinhaltet |
| tournament_name[0] | str | Name eines Turniers aus der Datenbank Turnier Zeile 1 |
| tournament_name[1] | str | Name eines Turniers aus der Datenbank Turnier Zeile 2 |

### Rückmeldung Beispiel

```JSON
{
    "tournament_name":["Nikolaus Turnier 2024","Nikolaus Turnier 2025"]
}
```

### Mögliche Fehlermeldungen

| HTTP Code | Beschreibung |
| :---: | :--- |
| 500 | Datenbankfehler beim Abfragen von Daten! |



## Laden des aktuellen Spielstandes

    GET /tournaments/match_plan/{matchID}

### Erklärung

Holt aktuelle Spielstand aus der Datenbank 

### Übergabe 

| Felder | Typ | Beschreibung |
| :---: | :---: | :--- |
| matchID | str | ID des Spiel als String |

### Übergabe Beispiel

```JSON
{
    "matchID": "4",
}
```

### Rückmeldungsfelder 

| Felder | Typ | Beschreibung |
| :---: | :---: | :--- |
| scores | array[2] | Ein Array welches aus 2 Integer besteht |
| scores[0] | int | Spielstand von Team 1 |
| scores[1] | int | Spielstand von Team 2 |

### Rückmeldung Beispiel

```JSON
{
    "scores":[22,15]
}
```

### Mögliche Fehlermeldungen

| HTTP Code | Beschreibung |
| :---: | :--- |
| 400 | Ungültige MatchID |
| 500 | Datenbankfehler beim Abfragen von Daten! |



## Aktualisieren von Spielständen

    PUT /tournaments/match_plan/team/{matchID}

### Erklärung

Ändern von einzelnen Spielständen in der Datenbank.

### Übergabe Parameter

| Felder | Typ | Beschreibung |
| :---: | :---: | :--- |
| matchID | str |  ID des Spiel als String |

### Übergabe Beispiel

```JSON
{
    "matchID": "4",
}
    wie noch andere Informationen
```

### Mögliche Fehlermeldungen

| HTTP Code | Beschreibung |
| :---: | :--- |
| 500 | Datenbankfehler beim ändern von Daten!  |
| 500 | Datenbankfehler beim Abfragen von Daten! |


## Ändern von Teamname

    PUT /tournaments/match_plan/team/{tournamentID}

### Erklärung

Ändern der Namen von einzelnen Teams in der Datenbank.

### Übergabe Parameter

| Felder | Typ | Beschreibung |
| :---: | :---: | :--- |
| tournamentID | str |  ID des Turniers als String |

### Übergabe Beispiel

```JSON
{
    "tournamentID": "4",
}
    wie noch andere Informationen
```

### Mögliche Fehlermeldungen

| HTTP Code | Beschreibung |
| :---: | :--- |
| 400 | Ungültige TournamentID |
| 500 | Datenbankfehler beim Abfragen von Daten! |


## Löschen eines Turniers

    POST /tournaments/delete_plan/{tournamentID}

### Erklärung

Das Turnier wird aus der Datenbank gelöscht mir den Dazugehörigen Spielständen und Leistungsgruppen.

### Übergabe Parameter

| Felder | Typ | Beschreibung |
| :---: | :---: | :--- |
| tournamentID | str |  ID des Turniers als String |

### Übergabe Beispiel

```JSON
{
    "tournamentID": "4",
}
```

### Mögliche Fehlermeldungen

| HTTP Code | Beschreibung |
| :---: | :--- |
| 400 | Ungültige TournamentID |
| 500 | Datenbankfehler beim Löschen von Daten! |