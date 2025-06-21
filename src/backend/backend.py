import fastapi
from fastapi import HTTPException
from data.apiClasses.apiClasses import *
from fastapi.middleware.cors import CORSMiddleware
from server import *
from database_request import *

from data.turnierplangenerator_4 import return_plan

server = Server()
api = fastapi.FastAPI()
data_request = DatabaseRequests()


origins = [
    "*"
]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST","PUT"],
    allow_headers=["*"], 
)

def check_received_data():
    pass


# Behandlung der API Schnittstellen

# API Schnittstelle für die Übermittlung der Eingabeparameter aus dem Frontend um den Turnierplan zu erstellen
@api.post("/tournament/")
def generate_tournament(tournament: GenerateTournament):
    """
    Erstellt ein neues Turnier und speichert es in der Datenbank.

    Eingabe:
        - name (str): Name des Turniers
        - num_fields (int): Anzahl der Spielfelder (max. 4)
        - return_match (str): "true" oder "false", ob Rückspiele stattfinden
        - start (time): Startzeit des Turniers
        - period (int): Spieldauer in Minuten
        - warm_up (int): Aufwärmzeit in Minuten
        - num_breaks (int): Anzahl der Pausen
        - break_length (List[int]): Längen der Pausen in Minuten
        - break_times (List[time]): Startzeiten der Pausen
        - stage_name (List[str]): Namen der Leistungsgruppen (max. 2)
        - num_teams (List[int]): Anzahl der Teams je Leistungsgruppe

    Fehler:
        - HTTP 500: Datenbankfehler beim Hinzufügen oder Abfragen von Daten.
    """
    sum_teams = 0
    for i in range(len(tournament.stage_name)):
        sum_teams = sum_teams + tournament.num_teams[i]

    # Funktion Turnier erstellen in Datenbank
    data_request.insert_tournament(tournament.name, tournament.period, sum_teams)

    
    # Funktion hinzufügen stages
    for stage in range(len(tournament.stage_name)):
        data_request.insert_stages(tournament.stage_name[stage], tournament.num_teams[stage]) 

    # Funktion um Turnier ID zu erhalten
    tournament_id = data_request.get_tournament_id()


    # TODO Hier müssen die Werte an den Algorithmus für die Erstellung des Turnierplans übergeben werden
    
    # Feste werte funktionieren nur mit einer Leistungsgruppe
    # tournament_data = [[1, 1, "Team 1", "Team 2", "Team 3", tournament.stage_name[0], 0, 0, "12:30"],[2, 1, "Team 2", "Team 1", "Team 3", tournament.stage_name[0], 0, 0, "12:50"]]

    tournament_data = return_plan(tournament.num_fields, tournament.num_teams, tournament.start, tournament.period, tournament.return_match, tournament.warm_up, [] if tournament.break_length is None else tournament.break_length, tournament.num_breaks, [] if tournament.break_times is None else tournament.break_times, tournament.stage_name)

    # game Aufbau [Spielnummer, Feldnummer, Team Name 1 Team, Team Name 2 Team, Team Name Schiedsrichter, Leistungsgruppe, Punkte Team 1, Punkte Team 2, Spieluhrzeit]
    # tournament_data [{'Spiel': 2, 'Feld': 'Field 1', 'Uhrzeit': '12:30', 'Team 1': 'STeam 1', 'Team 2': 'STeam 2', 'Schiedsrichter': 'STeam 3', 'Gruppe': 'Fun', 'Ergebnis Team 1': None, 'Ergebnis Team 2': None, 'Match Type': 'Hinspiel'},... ]
    print(f"Backend api: {tournament_data}")


    # Funktion hinzufügen der Teams in Team Tabelle und auch die Spiele
    if tournament_id is not None:
        for game in tournament_data:
            field_nummer = int(game["Feld"].split(" ")[-1])
            
            data_request.insert_tournament_data(tournament_id, game["Team 1"],game["Team 2"],game["Schiedsrichter"],field_nummer,game["Gruppe"],game["Uhrzeit"])
        return HTTPException(status_code=200,detail="SUCCESS")
    else:
        return HTTPException(status_code=500,detail="FAILED")


# API Schnittstelle für das Laden der Existierenden Turniere
@api.get("/tournaments/")
def get_tournaments():
    """
    Gibt alle existierenden Turniere aus der Datenbank zurück.

    Rückgabewert:
        - JSON-Objekt mit dem Schlüssel "tournaments":
            - Eine Liste von Turnieren mit je:
                - "id" (int): Turnier-ID
                - "name" (str): Name des Turniers

    Fehler:
        - HTTP 500: Datenbankfehler beim Abfragen von Daten.
    """
    # Funktion erhalten der existierenden Turniere
    tournaments = data_request.get_existing_tournaments()

    return {"tournaments": tournaments}

# API Schnittstelle für das Laden des Turnierplans
@api.get("/tournaments/{tournamentID}")
def get_match_plan(tournamentID: str):
    """
    Gibt den vollständigen Turnierplan für ein bestimmtes Turnier zurück.

    Pfadparameter:
        - tournamentID (str): ID des Turniers

    Rückgabe:
        - Liste von Spielen mit:
            - gameID (int)
            - team_ids (List[int])
            - team_names (List[str])
            - scores (List[int])
            - stage_name (str)
            - field (int)
            - play_time (str)

    Fehler:
        - HTTP 400: Ungültige TurnierID
        - HTTP 500: Fehler beim Datenbankzugriff
    """
    try:
        tournament_id = int(tournamentID)
    except ValueError:
        return HTTPException(status_code=400,detail="Ungültige TurnierID")

    # Funktion get Turnierplan
    tournament_plan = data_request.get_tournament_plan(tournament_id)

    return {"tournament":tournament_plan}

# API Schnittstelle für das aktualisieren der Spielstandes im Frontend
@api.get("/tournaments/match_plan/{matchID}")
def get_match(matchID: str):
    """
    Gibt den aktuellen Spielstand für ein bestimmtes Spiel zurück.

    Pfadparameter:
        - matchID (str): Spiel-ID

    Rückgabe:
        - scores (List[int]): [Punkte Team 1, Punkte Team 2]

    Fehler:
        - HTTP 400: Ungültige MatchID
        - HTTP 500: Fehler beim Datenbankzugriff
    """
    try:
        match_id = int(matchID)
    except ValueError:
        return HTTPException(status_code=400, detail="Ungültige MatchID")

    matches = data_request.get_matches(match_id)
    
    if len(matches) == 0:
        return HTTPException(status_code=500, detail="Datenbankfehler beim Abfrage von Daten! ")

    return {"scores": matches}

   
# API Änderung Spieldaten
@api.put("/tournaments/match_plan/match/{matchID}")
def change_match_result(matchID: str, match_result: Match): 
    """
    Aktualisiert den Spielstand eines bestimmten Spiels.

    Pfadparameter:
        - matchID (str): Spiel-ID

    Eingabe:
        - score_team1 (int): Punkte von Team 1
        - score_team2 (int): Punkte von Team 2
        - time_change (time): Zeitpunkt der Änderung

    Fehler:
        - HTTP 500: Fehler beim Ändern oder Abrufen der Daten
    """
    try:
        match_id = int(matchID)
    except ValueError:
        raise HTTPException(status_code=400, detail="Ungültige MatchID")

    # Funktion Änderung turnierdaten und Speicherung der Änderung
    if data_request.change_results(match_id,match_result.score_team1,match_result.score_team2, match_result.time_change):
        return HTTPException(status_code=200,detail="SUCCESS")
    return HTTPException(status_code=500, detail="Ein Fehler ist beim Ändern der Daten Aufgetreten! ")

# API holen aller Änderungen für ein Spiel
@api.get("/tournaments/match_plan/match_changes/{matchID}")
def get_match_result_changes(matchID: str):
    """
    Gibt alle Änderungen am Spielergebnis eines Spiels zurück.

    Pfadparameter:
        - matchID (str): Spiel-ID

    Rückgabe:
        - changes (List[dict]): Liste von Änderungen mit:
            - old_score_1 (int): Alter Spielstand Team 1
            - old_score_2 (int): Alter Spielstand Team 2
            - time (str): Zeitpunkt der Änderung

    Fehler:
        - HTTP 400: Ungültige MatchID
        - HTTP 500: Fehler beim Datenbankzugriff
    """
    try: 
        match_id = int(matchID)
    except:
        raise HTTPException(status_code=400, detail="Ungültige MatchID")
    
    changes = data_request.get_match_changes(match_id)

    return {"changes": changes}
    

# API Ändern Team Namen
@api.put("/tournaments/match_plan/team/{tournamentID}")
def change_team_name(tournamentID: str, new_team_name: TeamUpdate ):
    """
    Ändert den Namen eines Teams im Turnier.

    Pfadparameter:
        - tournamentID (str): ID des Turniers

    Eingabe:
        - team_id (str): ID des Teams
        - new_name (str): Neuer Name für das Team

    Fehler:
        - HTTP 400: Ungültige TurnierID
        - HTTP 500: Fehler beim Datenbankzugriff
    """
    try:
        tournament_id = int(tournamentID)
    except ValueError:
        raise HTTPException(status_code=400, detail="Ungültige TeamID")
    
    data_request.change_team_name(tournament_id, new_team_name.team_id, new_team_name.new_name)

    return HTTPException(status_code=200,detail="SUCCESS")
    
    
# API Löschen der Spieldaten 
@api.post("/tournaments/delete_plan/{tournamentID}")
def delete_tournament(tournamentID: str):
    """
    Löscht ein Turnier inklusive Spielstände und Leistungsgruppen.

    Pfadparameter:
        - tournamentID (int): ID des zu löschenden Turniers

    Fehler:
        - HTTP 400: Ungültige TurnierID
        - HTTP 500: Fehler beim Löschen aus der Datenbank
    """
    try:
        tournament_id = int(tournamentID)
    except ValueError:
        raise HTTPException(status_code=400, detail="Ungültige TournamentID")

    # Funktion Löschen eines Tourniere
    data_request.delete_tournament(tournament_id)

    return HTTPException(status_code=200,detail="SUCCESS")