import fastapi
from fastapi import HTTPException
from data.apiClasses.apiClasses import *
from fastapi.middleware.cors import CORSMiddleware
from server import *
from database_request import *

server = Server()
api = fastapi.FastAPI()
data_request = DatabaseRequests()


#hier werden die Ansteuerungen vom Fronten zugelasse
# TODO muss noch optimiert werden um die ansteuerung der API sicherer zu machen

origins = [
    "*"
]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET,POST,PUT"],
    allow_headers=["*"], #TODO spezifische Header benennen die zugelassen sein sollen
)

def check_received_data():
    pass


# Behandlung der API Schnittstellen

# API Schnittstelle für die Übermittlung der Eingabeparameter aus dem Frontend um den Turnierplan zu erstellen
@api.post("/tournament/")
def generate_tournament(tournament: GenerateTournament):
    
    sum_teams = 0
    for i in range(tournament.number_of_stages):
        sum_teams = sum_teams + tournament.number_of_teams[i]

    # Funktion Tournier erstellen in Datenbank
    data_request.insert_tournament(tournament.tournament_name,tournament.time_to_start, sum_teams)

    
    # Funktion hinzufügen stages
    for stage in range(tournament.anz_stages):
        data_request.insert_stages(tournament.stage_name[stage], tournament.number_of_teams[stage]) 

    # Funktion um tournierid zu erhalten
    tournament_id = data_request.get_tournament_id(tournament.tournament_name)


    # TODO Hier müssen die Werte an den Algorithmus für die Erstellung des Turnierplans übergeben werden
    
    tournament_data = [[1, 1, "Team 1", "Team 2", "Team 3", "Anfänger", 0, 0, time(12,30)],[2, 1, "Team 2", "Team 1", "Team 3" "Anfänger", 0, 0, time(12,50)]]

    # game Aufbau [Spielnummer, Feldnummer, Teamname 1 Team, Teamname 2 Team, Teamname Schiri, Leistungsgruppe, Punkte Team 1, Punkte Team 2, Spieluhrzeit]

    # Funktion hinzufügen der Teams in Team Tabelle und auch die Spiele
    for game in tournament_data:
        data_request.insert_tournament_data(tournament_id, game[2],game[3],game[4],game[1],game[5],game[8])


    return HTTPException(status_code=200,detail="SUCCESS")

# API Schnittstelle für die Übermittlung des Turnierplans
@api.get("/tournament/{tournament_name}")
def generate_tournament(tournament_name: str):
    try:
        tournament_bez = str(tournament_name)
    except ValueError:
        return HTTPException(status_code=400,detail="ERROR while fetching data")

    # Funktion erhalten der tournierid
    tournament_id = data_request.get_tournament_id(tournament_bez)

    # Funktion erhalten des Turnierplans aus Datenbank in 
    tournament = data_request.get_tournament_plan(tournament_id)

    return {"tournament": tournament}

# TODO ist überflüssig macht das gleiche wie ("/tournament/{tournament_name})
# API Schnittstelle für das Laden des Turnierplans
@api.get("/tournaments/{tournamentID}")
def get_matchplan(tournamentID: str):
    try:
        tournament_id = int(tournamentID)
    except ValueError:
        return HTTPException(status_code=400,detail="ERROR while fetching data")

    # Funktion get Turnierplan
    tournament_plan = data_request.get_tournament_plan(tournament_id)

    return {"tournament":tournament_plan}

# API Schnittstelle für das Laden der Existierenden Turniere
@api.get("/tournaments/")
def get_tournaments():
    # Funktion erhalten der existierenden Turniere
    tournaments = data_request.get_existing_tournaments()

    return {"tournaments": tournaments}

# API Schnittstelle für das aktualisieren des Matches
@api.get("/tournaments/matchplan/{matchID}")
def get_match(matchID: str):
    try:
        match_id = int(matchID)
    except ValueError:
        return HTTPException(status_code=400, detail="Ungültige MatchID")

    matches = data_request.get_matches(match_id)

    return {"matches": matches}

   
# API Änderung Spieldaten
@api.put("/tournaments/matchplan/match/{matchID}")
def change_match_result(matchID: str, match_result: Match):

    try:
        match_id = int(match_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Ungültige MatchID")

    # Funktion Änderung turnierdaten und Speicherung der Änderung
    data_request.change_results(match_id,match_result.score_team1,match_result.score_team2, match_result.time_change)

    return HTTPException(status_code=200,detail="SUCCESS")


# API Ändern Teamnamen
@api.put("/tournaments/matchplan/team/{tournamentID}")
def change_team_name(tournamentID: str, new_teamname: TeamUpdate ):
    try:
        tournament_id = int(tournamentID)
    except ValueError:
        raise HTTPException(status_code=400, detail="Ungültige TeamID")
    
    data_request.change_teamname(tournament_id, new_teamname.team_id, new_teamname.new_name)

    return HTTPException(status_code=200,detail="SUCCESS")
    
    
# API Löschen der Spieldaten 
@api.post("/tournaments/deleat_plan/{tournamentID}")
def delete_tournament(tournamentID: str):
    try:
        tournament_id = int(tournamentID)
    except ValueError:
        raise HTTPException(status_code=400, detail="Ungültige TournamentID")

    # Funktion Löschen eines Tourniers
    data_request.delet_tournament(tournament_id)

    return HTTPException(status_code=200,detail="SUCCESS")