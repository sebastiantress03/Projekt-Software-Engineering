import fastapi
from fastapi import HTTPException
import sqlite3
import os
from data.apiClasses.apiClasses import *
from fastapi.middleware.cors import CORSMiddleware
from server import *


server = Server()
api = fastapi.FastAPI()


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

    try:
        insert_tournament_data = server.execute("""INSERT INTO Turnier (TurnierBez, Spieldauer, TeamAnz)
                                    VALUES (?,?,?)""",[tournament.tournament_name, tournament.game_time, sum_teams])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")
    
    data_stages_successful = True
    for stage in range(tournament.number_of_stages):
        success = server.execute("""INSERT INTO Leistungsgruppen (Leistungsgruppenname,AnzTeamsLeist) 
                                    VALUES (?,?)""",[tournament.stage_name[stage],tournament.number_of_teams[stage]])
        
        if not success:
            data_stages_successful = False
            break
    try:
        tournament_id = server.query("SELECT TurnierID FROM Turnier WHERE TurnierBez IS LIKE ? ",[tournament.tournament_name])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")
    
    # TODO Hier müssen die Werte an den Algorithmus für die Erstellung des Turnierplans übergeben werden
    
    tournament_data = [[1, 1, "Team 1", "Team 2", "Team 3", "Anfänger", 0, 0, time(12,30)],[2, 1, "Team 2", "Team 1", "Team 3" "Anfänger", 0, 0, time(12,50)]]

  
    for game in tournament_data:
        # game Aufbau [Spielnummer, Feldnummer, Teamname 1 Team, Teamname 2 Team, Teamname, Schiri, Leistungsgruppe, Punkte Team 1, Punkte Team 2, Spieluhrzeit]

        try:
            team1_is_inserted = server.query("SELECT * FROM Team WHERE TurnierID = ? AND Teamname Like ? ",[tournament_id, game[2]])
            team2_is_inserted = server.query("SELECT * FROM Team WHERE TurnierID = ? AND Teamname Like ? ",[tournament_id, game[3]])
            referee_is_inserted = server.query("SELECT * FROM Team WHERE TurnierID = ? AND Teamname Like ? ",[tournament_id, game[4]])

            stage_id = server.query("SELECT LeistungsgruppenID FROM Leistungsgruppe WHERE Leistungsgruppenname LIKE ? ",[game[5]])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")
    

        if team1_is_inserted is None:
            try:
                server.execute("INSERT INTO Team (TurnierID, LeistungsgruppenID, Teamname) VALUES (?,?,?,?)",[tournament_id, stage_id, game[2]])
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")
        
        if team2_is_inserted is None:
            try:
                server.execute("INSERT INTO Team (TurnierID, LeistungsgruppenID, Teamname) VALUES (?,?,?,?)",[tournament_id, stage_id, game[3]]) 
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")                

        if referee_is_inserted is None:
            try:
                server.execute("INSERT INTO Team (TurnierID, LeistungsgruppenID, Teamname) VALUES (?,?,?,?)",[tournament_id, stage_id, game[4]]) 
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")
        try:
            team1 = server.query("SELECT TeamID FROM Team WHERE Teamname Like ?",[game[2]])
            team2 = server.query("SELECT TeamID FROM Team WHERE Teamname Like ?",[game[3]])
            referee = server.query("SELECT TeamID FROM Team WHERE Teamname Like ?",[game[4]])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")
        
        if team1 is not None and team2 is not None and referee is not None:
            try:

                    server.execute("""INSERT INTO Ergebnisse (TeamID1, TeamID2, SchiedsrichterID, Spielergebnis1 ,Spielergebnis2, SpielfeldNr, Uhrzeit)
                                    VALUES (?,?,?,?,?,?,?)""",[team1, team2, referee, 0, 0, game[2], game[8]])
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")

    if insert_tournament_data != None and data_stages_successful:
        return HTTPException(status_code=200,detail="SUCCESS")
    else:
        return HTTPException(status_code=404,detail="ERROR while inserting data")


# API Schnittstelle für die Übermittlung des Turnierplans
@api.get("/tournament/{tournament_name}")
def generate_tournament(tournament_name: str):
    try:
        tournament_bez = str(tournament_name)
    except ValueError:
        return HTTPException(status_code=422,detail="ERROR while fetching data")

    try:
        tournament_id  = server.query("SELECT TurnierID FROM Turnier WHERE TurnierBez IS LIKE ? ",[tournament_bez])
    except ValueError:
        return HTTPException(status_code=422,detail="ERROR while fetching data")
    
    try:
        data = server.query("""SELECT DISTINCT e.SpielID, e.TeamID1, e.TeamID2, e.SchiedsrichterID, e.Spielergebnis1, e.Spielergebnis2, e.SpielfeldNr,e.Uhrzeit FROM Ergebnisse e 
                                JOIN Team t1 ON t1.TeamID = e.TeamID1 
                                JOIN Team t2 ON t2.TeamID = e.TeamID2 
                                WHERE t1.TurnierID = ?""",[tournament_id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")

    if data != None and len(data) != 0:
        return {"data": data}
    else:
        return HTTPException(status_code=404,detail="ERROR while fetching data")

# API Schnittstelle für das Laden des Turnierplans
@api.get("/tournaments/{tournamentID}")
def get_matchplan(tournamentID: str):
    try:
        tournament_id = int(tournamentID)
    except ValueError:
        return HTTPException(status_code=422,detail="ERROR while fetching data")

    try:
        get_tournament_data = server.query("""SELECT DISTINCT e.SpielID, e.TeamID1, e.TeamID2, e.SchiedsrichterID, e.Spielergebnis1, e.Spielergebnis2, e.SpielfeldNr, e.Uhrzeit FROM Ergebnisse e 
                                JOIN Team te ON te.TeamID = e.TeamID1 
                                JOIN Team te ON te.TeamID = e.TeamID2 
                                WHERE te.TurnierID = ?""",[tournament_id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")

    if get_tournament_data != None and len(get_tournament_data) != 0:
        return {"data": get_tournament_data}
    else:
        return HTTPException(status_code=404,detail="ERROR while fetching data")


# API Schnittstelle für das Laden der Existierenden Turniere
@api.get("/tournaments/")
def get_tournaments():

    try:
        get_tournament_data = server.query("SELECT TurnierID, TurnierBez FROM Turnier")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")

    if get_tournament_data != None and len(get_tournament_data) != 0:
        return {"data": get_tournament_data}
    else:
        return HTTPException(status_code=404,detail="ERROR while fetching data")


# API Schnittstelle für das aktualisieren des Matches
@api.get("/tournaments/matchplan/{matchID}")
def get_match(matchID: str):
    try:
        match_id = int(matchID)
    except ValueError:
        return HTTPException(status_code=422, detail="Ungültige MatchID")

    try:
        match_data = server.query("SELECT Spielergebnis1, Spielergebnis2 FROM Ergebnisse WHERE SpielID = ?",[match_id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")

    if match_data != None and len(match_data) != 0:
        return {"data": match_data}
    else:
        return HTTPException(status_code=404,detail="ERROR while fetching data")
    
# API Änderung Spieldaten
# TODO überprüfen
@api.put("/tournaments/matchplan/{matchID}")
def change_match_result(matchID: str, match_result: Match):

    try:
        match_id = int(match_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Ungültige MatchID")

    old_score_team1 = server.query("SELECT Spielergebnis1 FROM Ergebnisse WHERE SpielID = ?",[match_id])
    old_score_team2 = server.query("SELECT Spielergebnis2 FROM Ergebnisse WHERE SpielID = ?",[match_id])

    if old_score_team1 is None or old_score_team2 is None:
        raise HTTPException(status_code=404,detail="Spiel Existiert nicht")

    try:
        update_result = server.execute("""UPDATE Ergebnisse SET Spielergebnis1 = ?, Spielergebnis2 = ? 
                                    WHERE SpielID = ?""",[match_result.score_team1,match_result.score_team2, match_id])
        
        insert_result = server.execute("""INSERT INTO Aenderungen (SpielID, alteSpielergebnis1, alteSpielergebnis2, Uhrzeitaenderung) 
                                    VALUES (?,?,?,?)""",[match_id,old_score_team1, old_score_team2 ,match_result.time_change])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")

    if update_result is not None and insert_result is not None:
        return HTTPException(status_code=200,detail="SUCCESS")
    else:
        return HTTPException(status_code=404,detail="ERROR while update or insert data")

# API Löschen der Spieldaten 
@api.post("/tournaments/deleat_plan/{tournamentID}")
def delete_tournament(tournamentID: str):

    try:
        tournament_id = int(tournamentID)
    except ValueError:
        raise HTTPException(status_code=422, detail="Ungültige TournamentID")

    try:
        delete_tournament = server.execute("DELETE FROM Turnier WHERE TurnierID = ?", [tournament_id])

        delete_scores = server.execute("""DELETE FROM Leistungsgruppen
                                    WHERE LeistungsgruppenID NOT IN (
                                    SELECT DISTINCT LeistungsgruppenID FROM Team)""")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")
    
    if delete_tournament != None and delete_scores != None:
        return HTTPException(status_code=200,detail="SUCCESS")
    else:
        return HTTPException(status_code=404,detail="ERROR while deleting data")