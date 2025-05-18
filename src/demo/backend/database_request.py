import fastapi
from fastapi import HTTPException
from data.apiClasses.apiClasses import *
from server import *

server = Server()

class DatabaseRequests:
    def __init__(self):
        pass

    def insert_tournament(name: str, period: int , anz_teams: int ):
        try:
            server.execute("""INSERT INTO Turnier (TurnierBez, Spieldauer, TeamAnz)
                                    VALUES (?,?,?)""",[name, period, anz_teams])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Datenbankfehler: {str(e)}")

    def insert_stages(name: str, team_size: int):
        try: 
            server.execute("""INSERT INTO Leistungsgruppen (Leistungsgruppenname,AnzTeamsLeist) 
                                        VALUES (?,?)""",[name,team_size])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Datenbankfehler: {str(e)}")

    def get_tournament_id(name: str):
        try:
            tournament_id = server.query("SELECT TurnierID FROM Turnier WHERE TurnierBez IS LIKE ? ",[name])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Datenbankfehler: {str(e)}")
        return tournament_id
    

    def insert_tournament_data(tournament_id: int, team1: str, team2: str, referee: str, field: int, stage_name: str, play_time: time):
        try:
            team1_is_inserted = server.query("SELECT * FROM Team WHERE TurnierID = ? AND Teamname Like ? ",[tournament_id, team1])
            team2_is_inserted = server.query("SELECT * FROM Team WHERE TurnierID = ? AND Teamname Like ? ",[tournament_id, team2])
            referee_is_inserted = server.query("SELECT * FROM Team WHERE TurnierID = ? AND Teamname Like ? ",[tournament_id, referee])

            stage_id = server.query("SELECT LeistungsgruppenID FROM Leistungsgruppe WHERE Leistungsgruppenname LIKE ? ",[stage_name])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Datenbankfehler: {str(e)}")
    

        if team1_is_inserted is None:
            try:
                server.execute("INSERT INTO Team (TurnierID, LeistungsgruppenID, Teamname) VALUES (?,?,?,?)",[tournament_id, stage_id, team1])
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Datenbankfehler: {str(e)}")
        
        if team2_is_inserted is None:
            try:
                server.execute("INSERT INTO Team (TurnierID, LeistungsgruppenID, Teamname) VALUES (?,?,?,?)",[tournament_id, stage_id, team2]) 
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Datenbankfehler: {str(e)}")                

        if referee_is_inserted is None:
            try:
                server.execute("INSERT INTO Team (TurnierID, LeistungsgruppenID, Teamname) VALUES (?,?,?,?)",[tournament_id, stage_id, referee]) 
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Datenbankfehler: {str(e)}")
        try:
            team1 = server.query("SELECT TeamID FROM Team WHERE Teamname Like ?",[team1])
            team2 = server.query("SELECT TeamID FROM Team WHERE Teamname Like ?",[team1])
            referee = server.query("SELECT TeamID FROM Team WHERE Teamname Like ?",[team1])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Datenbankfehler: {str(e)}")
        
        if team1 is not None and team2 is not None and referee is not None:
            try:

                server.execute("""INSERT INTO Ergebnisse (TeamID1, TeamID2, SchiedsrichterID, Spielergebnis1 ,Spielergebnis2, SpielfeldNr, Uhrzeit)
                                    VALUES (?,?,?,?,?,?,?)""",[team1, team2, referee, 0, 0, field, play_time])
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Datenbankfehler: {str(e)}")

    def get_tournament_plan(tournament_id: int):
        return_date = []
        try:
            data = server.query("""SELECT DISTINCT e.SpielID, e.TeamID1, e.TeamID2, e.SchiedsrichterID, e.Spielergebnis1, e.Spielergebnis2, e.SpielfeldNr,e.Uhrzeit FROM Ergebnisse e 
                                    JOIN Team t1 ON t1.TeamID = e.TeamID1 
                                    JOIN Team t2 ON t2.TeamID = e.TeamID2 
                                    WHERE t1.TurnierID = ?""",[tournament_id])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Datenbankfehler beim Turnierplan abfragen: {str(e)}")
        
        for game in data:
            return_date.append({"gameID":data[0],"teamID":[data[1], data[2],data[3]],"scores":[data[4], data[5]],"field":data[6],"play_time":data[7]})

        return return_date
    
    def get_matches(match_id: int):
        return_data = []
        try:
            match_data = server.query("SELECT Spielergebnis1, Spielergebnis2 FROM Ergebnisse WHERE SpielID = ?",[match_id])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Datenbankfehler: {str(e)}")
        return_data.append({"scores":[match_data[0], match_data[1]]})

        return return_data
    
    def get_existing_tournaments():
        return_data = []
        try:
            get_tournament_data = server.query("SELECT TurnierID, TurnierBez FROM Turnier")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Datenbankfehler: {str(e)}")
        for tournament in get_tournament_data:
            return_data.append({"tournament_name": tournament[1]})
        
        return return_data

    
    def change_results(match_id: int, score1: int, score2: int, time_change: time):
        old_score_team1 = server.query("SELECT Spielergebnis1 FROM Ergebnisse WHERE SpielID = ?",[match_id])
        old_score_team2 = server.query("SELECT Spielergebnis2 FROM Ergebnisse WHERE SpielID = ?",[match_id])

        if old_score_team1 is None or old_score_team2 is None:
            raise HTTPException(status_code=404,detail="Spiel Existiert nicht")

        try:
            update_result = server.execute("""UPDATE Ergebnisse SET Spielergebnis1 = ?, Spielergebnis2 = ? 
                                        WHERE SpielID = ?""",[score1, score2, match_id])
            
            insert_result = server.execute("""INSERT INTO Aenderungen (SpielID, alteSpielergebnis1, alteSpielergebnis2, Uhrzeitaenderung) 
                                        VALUES (?,?,?,?)""",[match_id,old_score_team1, old_score_team2 ,time_change])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Datenbankfehler: {str(e)}")
        
    def change_teamname(tournament_id: int, team_id: int,new_name: str):
        try:
            team_name_exist = server.query("SELECT Count(*) FROM Team WHERE TurnierID = ? AND Teamname LIKE ?",[tournament_id,new_name])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Datenbankfehler: {str(e)}")
        
        if team_name_exist[0] == 0:
            try:
                server.execute("UPDATE Team SET Teamname = ? WHERE TeamID = ?",[new_name,team_id])
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Datenbankfehler bei Änderung: {str(e)}")
        else:
            raise HTTPException(status_code=409, detail="Teamname existiert bereits")

        
    def delet_tournament(tournament_id: int):
        try:
            delete_tournament = server.execute("DELETE FROM Turnier WHERE TurnierID = ?", [tournament_id])

            delete_scores = server.execute("""DELETE FROM Leistungsgruppen
                                    WHERE LeistungsgruppenID NOT IN (
                                    SELECT DISTINCT LeistungsgruppenID FROM Team)""")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Datenbankfehler: {str(e)}")

