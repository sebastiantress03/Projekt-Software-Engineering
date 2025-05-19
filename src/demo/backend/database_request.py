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
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Hinzufügen von Daten! ")

    def insert_stages(name: str, team_size: int):
        try: 
            server.execute("""INSERT INTO Leistungsgruppen (Leistungsgruppenname,AnzTeamsLeist) 
                                        VALUES (?,?)""",[name,team_size])
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Hinzufügen von Daten! ")

    def get_tournament_id(name: str):
        try:
            tournament_id = server.query("SELECT TurnierID FROM Turnier WHERE TurnierBez IS LIKE ? ",[name])
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Abfrage von Daten! ")
        
        if isinstance(tournament_id,int):
            return tournament_id
        else:
            return None
    

    def insert_tournament_data(tournament_id: int, team1: str, team2: str, referee: str, field: int, stage_name: str, play_time: time):
        try:
            team1_is_inserted = server.query("SELECT * FROM Team WHERE TurnierID = ? AND Teamname Like ? ",[tournament_id, team1])
            team2_is_inserted = server.query("SELECT * FROM Team WHERE TurnierID = ? AND Teamname Like ? ",[tournament_id, team2])
            referee_is_inserted = server.query("SELECT * FROM Team WHERE TurnierID = ? AND Teamname Like ? ",[tournament_id, referee])

            stage_id = server.query("SELECT LeistungsgruppenID FROM Leistungsgruppe WHERE Leistungsgruppenname LIKE ? ",[stage_name])
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Abfrage von Daten! ")
    

        if team1_is_inserted is None:
            try:
                server.execute("INSERT INTO Team (TurnierID, LeistungsgruppenID, Teamname) VALUES (?,?,?)",[tournament_id, stage_id, team1])
            except Exception as e:
                raise HTTPException(status_code=500, detail="Datenbankfehler beim Hinzufügen von Daten! ")
        
        if team2_is_inserted is None:
            try:
                server.execute("INSERT INTO Team (TurnierID, LeistungsgruppenID, Teamname) VALUES (?,?,?)",[tournament_id, stage_id, team2]) 
            except Exception as e:
                raise HTTPException(status_code=500, detail="Datenbankfehler beim Hinzufügen von Daten! ")                

        if referee_is_inserted is None:
            try:
                server.execute("INSERT INTO Team (TurnierID, LeistungsgruppenID, Teamname) VALUES (?,?,?)",[tournament_id, stage_id, referee]) 
            except Exception as e:
                raise HTTPException(status_code=500, detail="Datenbankfehler beim Hinzufügen von Daten! ")
        try:
            team1_id= server.query("SELECT TeamID FROM Team WHERE TurnierID = ? AND Teamname Like ?",[tournament_id, team1])
            team2_id = server.query("SELECT TeamID FROM Team WHERE TurnierID = ? AND Teamname Like ?",[tournament_id, team2])
            referee_id = server.query("SELECT TeamID FROM Team WHERE TurnierID = ? AND Teamname Like ?",[tournament_id, referee])
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Abfrage von Daten! ")
        
        if team1_id is not None and team2_id is not None and referee_id is not None:
            try:

                server.execute("""INSERT INTO Ergebnisse (TeamID1, TeamID2, SchiedsrichterID, Spielergebnis1 ,Spielergebnis2, SpielfeldNr, Uhrzeit)
                                    VALUES (?,?,?,?,?,?,?)""",[team1_id, team2_id, referee_id, 0, 0, field, play_time])
            except Exception as e:
                raise HTTPException(status_code=500, detail="Datenbankfehler beim Hinzufügen von Daten! ")

    def get_tournament_plan(tournament_id: int):
        return_date = []
        try:
            data = server.query("""SELECT DISTINCT e.SpielID, t1.Teamname, t2.Teamname, t3.Teamname, e.Spielergebnis1, e.Spielergebnis2, l.Leistungsgruppenname, e.SpielfeldNr, e.Uhrzeit FROM Ergebnisse e 
                                    JOIN Team t1 ON t1.TeamID = e.TeamID1 
                                    JOIN Team t2 ON t2.TeamID = e.TeamID2 
                                    JOIN Team t3 ON t3.TeamID = e.SchiedsrichterID  
                                    JOIN Leistungsgruppen l ON l.LeistungsgruppenID = t1.LeistungsgruppenID  
                                    WHERE t1.TurnierID = ?""",[tournament_id])
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Abfrage von Daten! ")
        
        for game in data:
            t_data = TournamentPlan(game[0],game[7],game[1],game[2],game[3],game[4],game[5],game[6],game[8])
            return_date.append({"gameID":t_data.game_number,"team_name":[t_data.team1, t_data.team2,t_data.referee],"scores":[t_data.score_team1, t_data.score_team2 ] ,"stage_name":t_data.stage_name,"field":t_data.field_number,"play_time":t_data.time_of_game})

        return return_date
    
    def get_matches(match_id: int):
        return_data = []
        try:
            match_data = server.query("SELECT Spielergebnis1, Spielergebnis2 FROM Ergebnisse WHERE SpielID = ?",[match_id])
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Abfrage von Daten! ")

        # validate Data
        if len(match_data) == 2:
            return_data.append(match_data[0])
            return_data.append(match_data[1])

        return return_data
    
    def get_existing_tournaments():
        return_data = []
        try:
            get_tournament_data = server.query("SELECT TurnierID, TurnierBez FROM Turnier")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Abfrage von Daten! ")
        
        for tournament in get_tournament_data:
            if isinstance(tournament,str):
                return_data.append(tournament[1])
        
        return return_data
    
  
    def change_results(match_id: int, score1: int, score2: int, time_change: time):
        try:
            old_score_team1 = server.query("SELECT Spielergebnis1 FROM Ergebnisse WHERE SpielID = ?",[match_id])
            old_score_team2 = server.query("SELECT Spielergebnis2 FROM Ergebnisse WHERE SpielID = ?",[match_id])
        except Exception as e:
            raise HTTPException(status_code=500,detail="Datenbankfehler beim Abfrage von Daten! ")
        
        if old_score_team1 is None or old_score_team2 is None:
            raise HTTPException(status_code=400,detail="Spiel Existiert nicht")

        try:
            server.execute("""UPDATE Ergebnisse SET Spielergebnis1 = ?, Spielergebnis2 = ? 
                                        WHERE SpielID = ?""",[score1, score2, match_id])
            
            server.execute("""INSERT INTO Aenderungen (SpielID, alteSpielergebnis1, alteSpielergebnis2, Uhrzeitaenderung) 
                                        VALUES (?,?,?,?)""",[match_id,old_score_team1, old_score_team2 ,time_change])
        except Exception as e:
            raise HTTPException(status_code=500, detail=" Datenbankfehler beim ändern von Daten! ")
        
    def change_team_name(tournament_id: int, team_id: int,new_name: str):
        try:
            team_name_exist = server.query("SELECT Count(*) FROM Team WHERE TurnierID = ? AND Teamname LIKE ?",[tournament_id,new_name])
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Abfrage von Daten! ")
        
        if team_name_exist[0] == 0:
            try:
                server.execute("UPDATE Team SET Teamname = ? WHERE TeamID = ?",[new_name,team_id])
            except Exception as e:
                raise HTTPException(status_code=500, detail="Datenbankfehler beim ändern von Daten! ")
        else:
            raise HTTPException(status_code=409, detail="Teamname existiert bereits")

        
    def delete_tournament(tournament_id: int):
        try:
            server.execute("DELETE FROM Turnier WHERE TurnierID = ?", [tournament_id])

            server.execute("""DELETE FROM Leistungsgruppen
                                    WHERE LeistungsgruppenID NOT IN (
                                    SELECT DISTINCT LeistungsgruppenID FROM Team)""")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Löschen von Daten! ")

