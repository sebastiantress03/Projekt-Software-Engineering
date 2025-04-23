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
    allow_methods=["GET,POST"],
    allow_headers=["*"], #TODO spezifische Header benennen die zugelassen sin sollen
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

    dataTu = server.execute("INSERT INTO Turnier (TurnierBez, Spieldauer, TeamAnz) VALUES (?,?,?)",[tournament.tournament_name, tournament.game_time, sum_teams])

    data_stages_succesful = True
    for stage in range(tournament.number_of_stages):
        success = server.execute("INSERT INTO Leistungsgruppen (Leistungsgruppenname,AnzTeamsLeist) VALUES (?,?)",[tournament.stage_name[stage],tournament.number_of_teams[stage]])
        
        if not success:
            data_stages_succesful = False
            break
    
    # TODO Hier müssen die Werte an den Algorithmus für die Erstellung des Turnierplans übergeben werden und danch in die Tabelle gespeichert werden 

    if dataTu != None and data_stages_succesful:
        return fastapi.HTTPException(status_code=200,detail="SUCCESS")
    else:
        return fastapi.HTTPException(status_code=404,detail="ERROR while inserting data") # TODO extra fehlerabfrage nach übermittlung der daten ans Frontend


# API Schnittstelle für die Übermittlung des Turnierplans
@api.get("/tournament/{tournament_name}")
def generate_tournament(tournament_name: str):
    
    tournamentID  = server.query("SELECT TurnierID FROM Turnier WHERE TurnierBez IS LIKE ? ",[tournament_name])

    data = server.query("""SELECT DISTINCT e.SpielID, e.TeamID1, e.TeamID2, e.SchiedsrichterID, e.Spielergebnis1, e.Spielergebnis2, e.SpielfeldNr,e.Uhrzeit FROM Ergebnisse e 
                            JOIN Team t1 ON t1.TeamID = e.TeamID1 
                            JOIN Team t2 ON t2.TeamID = e.TeamID2 
                            WHERE t1.TurnierID = ?""",[tournamentID])
    

    if data != None and len(data) != 0:
        return {"data": data}
    else:
        return fastapi.HTTPException(status_code=404,detail="ERROR while fetching data")

# API Schnittstelle für das Laden des Turnierplans
@api.get("/tournaments/{tournamentID}")
def get_matchplan(tournamentID: str):
    data = server.query("""SELECT DISTINCT e.SpielID, e.TeamID1, e.TeamID2, e.SchiedsrichterID, e.Spielergebnis1, e.Spielergebnis2, e.SpielfeldNr, e.Uhrzeit FROM Ergebnisse e 
                            JOIN Team te ON te.TeamID = e.TeamID1 
                            JOIN Team te ON te.TeamID = e.TeamID2 
                            WHERE te.TurnierID = ?""",[int(tournamentID)])
    
    if data != None and len(data) != 0:
        return {"data": data}
    else:
        return fastapi.HTTPException(status_code=404,detail="ERROR while fetching data")


# API Schnittstelle für das Laden der Existierenden Turniere
@api.get("/tournaments/")
def get_tournaments():
    data = server.query("SELECT TurnierID, TurnierBez FROM Turnier")
    
    if data != None and len(data) != 0:
        return {"data": data}
    else:
        return fastapi.HTTPException(status_code=404,detail="ERROR while fetching data")


# API Schnittstelle für das aktualisieren des Matches
@api.get("/tournaments/matchplan/{matchID}")
def get_match(matchID: str):
    data = server.query("SELECT Spielergebnis1, Spielergebnis2 FROM Ergebnisse WHERE SpielID = ?",[int(matchID)])

    if data != None and len(data) != 0:
        return {"data": data}
    else:
        return fastapi.HTTPException(status_code=404,detail="ERROR while fetching data")
    
# API Änderung Spieldaten
@api.post("/tournaments/matchplan/{matchID}")
def change_match_result(matchID: str, match_result: Match):
    data = server.execute("""UPDATE Ergebnisse SET Spielergebnis1 = ?, Spielergebnis2 = ? 
                        WHERE SpielID = ?""",[match_result.spielergebnis1,match_result.spielergebnis2, int(matchID)])
    
    if data != None:
        return fastapi.HTTPException(status_code=200,detail="SUCCESS")
    else:
        return fastapi.HTTPException(status_code=404,detail="ERROR while update data")

# API Löschen der Spieldaten 
@api.post("/tournaments/deleat_plan/{tournamentID}")
def delete_tournament(tournamentID: str):

    data = server.execute("DELETE FROM Turnier WHERE TurnierID = ?", [int(tournamentID)])

    dataLe = server.execute("""DELETE FROM Leistungsgruppen
                                WHERE LeistungsgruppenID NOT IN (
                                SELECT DISTINCT LeistungsgruppenID FROM Team)""")

    
    if data != None and dataLe != None:
        return fastapi.HTTPException(status_code=200,detail="SUCCESS")
    else:
        return fastapi.HTTPException(status_code=404,detail="ERROR while deleting data")