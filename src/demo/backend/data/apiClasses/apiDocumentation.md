# API-Documentation

1. [Erstellen des Turniers](#erstellen-des-turniers)
2. [Erhalt des Turnierplans über Namen](#erhalt-des-turnierplans-über-namen)
3. [Erhalt des Turnierplans über ID](#erhalt-des-turnierplans-über-id)
4. [Laden existierender Turniere](#laden-existierender-turniere)
5. [Laden des aktuellen Spielstandes](#laden-des-aktuellen-spielstandes)
6. [Aktualisieren von Spielständen](#aktualisieren-von-spielständen)
7. [Ändern von Teamname](#ändern-von-teamname)
8. [Löschen eines Turniers](#löschen-eines-turniers)
---

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


## Erhalt des Turnierplans über Namen

    GET /tournament/{tournament_name}

### Erklärung

<<<<<<< HEAD
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
=======
Übermittelt existierenden Turnierplan aus der Datenbank, indem der Namen des Turniers das geladen werden soll mit übergeben wird.
>>>>>>> 87f2fc8b0afa4b98ea5511458ed9c02e47539079

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


## Erhalt des Turnierplans über ID

    GET /tournament/{tournamentID}

### Erklärung

<<<<<<< HEAD
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
=======
Übermittelt existierenden Turnierplan aus der Datenbank, indem die TurnierID, als String, des Turniers das geladen werden soll mit übergeben wird.
>>>>>>> 87f2fc8b0afa4b98ea5511458ed9c02e47539079

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

<<<<<<< HEAD
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
=======
Holt aktuelle Spielstand aus der Datenbank mittles der übergabe der SpielID als String.
>>>>>>> 87f2fc8b0afa4b98ea5511458ed9c02e47539079

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

<<<<<<< HEAD
Ändern von einzelnen Spielständen in der Datenbank.
=======
Ändern von einzelnen Spielständen in der Datenbank. Die Adressierung des Spiels erfolgt über die SpielID als String welche mitgegeben wir.
>>>>>>> 87f2fc8b0afa4b98ea5511458ed9c02e47539079

### Übergabe Parameter

| Felder | Typ | Beschreibung |
| :---: | :---: | :--- |
<<<<<<< HEAD
| matchID | str |  ID des Spiel als String |
=======
| score_team1 | int | Die Punkte von Team 1 |
| score_team2 | int | Die Punkte von Team 2 |
| time_change | time | Die Uhrzeit an der Die Änderung vorgenommen wurde |
>>>>>>> 87f2fc8b0afa4b98ea5511458ed9c02e47539079

### Übergabe Beispiel

```JSON
{
<<<<<<< HEAD
    "matchID": "4",
}
    wie noch andere Informationen
=======
    "score_team1": 15,
    "score_team2": 25,
    "time_change": "11:15:00"
}
>>>>>>> 87f2fc8b0afa4b98ea5511458ed9c02e47539079
```

### Mögliche Fehlermeldungen

| HTTP Code | Beschreibung |
| :---: | :--- |
| 500 | Datenbankfehler beim ändern von Daten!  |
| 500 | Datenbankfehler beim Abfragen von Daten! |


## Ändern von Teamname

    PUT /tournaments/match_plan/team/{tournamentID}

### Erklärung

<<<<<<< HEAD
Ändern der Namen von einzelnen Teams in der Datenbank.
=======
Ändern der Namen von einzelnen Teams in der Datenbank. Die Adressierung des Team erfolgt über die TurnierID als String, welche mitgegeben wir damit zunächst überprüft werden kann ob in dem Turnier bereits ein Team mit dem Namen bereits existiert.
>>>>>>> 87f2fc8b0afa4b98ea5511458ed9c02e47539079

### Übergabe Parameter

| Felder | Typ | Beschreibung |
| :---: | :---: | :--- |
<<<<<<< HEAD
| tournamentID | str |  ID des Turniers als String |
=======
| team_id | str |  ID des Teams welches den neuen Namen erhalten soll als String |
| new_name | str | Der neue Name für das Team |
>>>>>>> 87f2fc8b0afa4b98ea5511458ed9c02e47539079

### Übergabe Beispiel

```JSON
{
<<<<<<< HEAD
    "tournamentID": "4",
}
    wie noch andere Informationen
=======
    "team_id": "25",
    "new_name": "Die Informatiker"
}
>>>>>>> 87f2fc8b0afa4b98ea5511458ed9c02e47539079
```

### Mögliche Fehlermeldungen

| HTTP Code | Beschreibung |
| :---: | :--- |
| 400 | Ungültige TournamentID |
| 500 | Datenbankfehler beim Abfragen von Daten! |


## Löschen eines Turniers

    POST /tournaments/delete_plan/{tournamentID}

### Erklärung

<<<<<<< HEAD
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
=======
Das Turnier wird aus der Datenbank gelöscht mir den Dazugehörigen Spielständen und Leistungsgruppen. Dafür wird die TurnierID mit übergeben.
>>>>>>> 87f2fc8b0afa4b98ea5511458ed9c02e47539079

### Mögliche Fehlermeldungen

| HTTP Code | Beschreibung |
| :---: | :--- |
| 400 | Ungültige TournamentID |
| 500 | Datenbankfehler beim Löschen von Daten! |