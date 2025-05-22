import fastapi
from fastapi import HTTPException
from data.apiClasses.apiClasses import *
from fastapi.middleware.cors import CORSMiddleware
from server import *
from database_request import *

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
    
    sum_teams = 0
    for i in len(tournament.stage_name):
        sum_teams = sum_teams + tournament.num_teams[i]

    # Funktion Turnier erstellen in Datenbank
    data_request.insert_tournament(tournament.name,tournament.start, sum_teams)

    
    # Funktion hinzufügen stages
    for stage in len(tournament.stage_name):
        data_request.insert_stages(tournament.stage_name[stage], tournament.num_teams[stage]) 

    # Funktion um Turnier ID zu erhalten
    tournament_id = data_request.get_tournament_id(tournament.name)


    # TODO Hier müssen die Werte an den Algorithmus für die Erstellung des Turnierplans übergeben werden
    
    tournament_data = [[1, 1, "Team 1", "Team 2", "Team 3", "Anfänger", 0, 0, time(12,30)],[2, 1, "Team 2", "Team 1", "Team 3" "Anfänger", 0, 0, time(12,50)]]

    # game Aufbau [Spielnummer, Feldnummer, Team Name 1 Team, Team Name 2 Team, Team Name Schiedsrichter, Leistungsgruppe, Punkte Team 1, Punkte Team 2, Spieluhrzeit]

    # Funktion hinzufügen der Teams in Team Tabelle und auch die Spiele
    for game in tournament_data:
        data_request.insert_tournament_data(tournament_id, game[2],game[3],game[4],game[1],game[5],game[8])

    return HTTPException(status_code=200,detail="SUCCESS")

# API Schnittstelle für die Übermittlung des Turnierplans
@api.get("/tournament/{tournament_name}")
def generate_tournament(tournament_name: str):
    try:
        tournament_name = str(tournament_name)
    except ValueError:
        return HTTPException(status_code=400,detail="Ungültigen Turniernamen")

    # Funktion erhalten der Turnier ID
    tournament_id = data_request.get_tournament_id(tournament_name)

    if tournament_id is None or not isinstance(tournament_id,int):
        return HTTPException(status_code=500,detail="Datenbankfehler beim Abfrage von Daten! ")
    # Funktion erhalten des Turnierplans aus Datenbank in 
    tournament = data_request.get_tournament_plan(tournament_id)

    return {"tournament": tournament}

# TODO ist überflüssig macht das gleiche wie ("/tournament/{tournament_name})
# API Schnittstelle für das Laden des Turnierplans
@api.get("/tournaments/{tournamentID}")
def get_match_plan(tournamentID: str):
    try:
        tournament_id = int(tournamentID)
    except ValueError:
        return HTTPException(status_code=400,detail="Ungültige TurnierID")

    # Funktion get Turnierplan
    tournament_plan = data_request.get_tournament_plan(tournament_id)

    return {"tournament":tournament_plan}

# API Schnittstelle für das Laden der Existierenden Turniere
@api.get("/tournaments/")
def get_tournaments():
    # Funktion erhalten der existierenden Turniere
    tournaments = data_request.get_existing_tournaments()

    return {"tournament_name": tournaments}

# API Schnittstelle für das aktualisieren des Matches
@api.get("/tournaments/match_plan/{matchID}")
def get_match(matchID: str):
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
def change_match_result(match_ID: str, match_result: Match): 
    try:
        match_id = int(match_ID)
    except ValueError:
        raise HTTPException(status_code=400, detail="Ungültige MatchID")

    # Funktion Änderung turnierdaten und Speicherung der Änderung
    data_request.change_results(match_id,match_result.score_team1,match_result.score_team2, match_result.time_change)

    return HTTPException(status_code=200,detail="SUCCESS")


# API Ändern Team Namen
@api.put("/tournaments/match_plan/team/{tournamentID}")
def change_team_name(tournamentID: str, new_team_name: TeamUpdate ):
    try:
        tournament_id = int(tournamentID)
    except ValueError:
        raise HTTPException(status_code=400, detail="Ungültige TeamID")
    
    data_request.change_team_name(tournament_id, new_team_name.team_id, new_team_name.new_name)

    return HTTPException(status_code=200,detail="SUCCESS")
    
    
# API Löschen der Spieldaten 
@api.post("/tournaments/delete_plan/{tournamentID}")
def delete_tournament(tournamentID: str):
    try:
        tournament_id = int(tournamentID)
    except ValueError:
        raise HTTPException(status_code=400, detail="Ungültige TournamentID")

    # Funktion Löschen eines Tourniere
    data_request.delete_tournament(tournament_id)

    return HTTPException(status_code=200,detail="SUCCESS")