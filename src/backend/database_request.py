import fastapi
from fastapi import HTTPException
from data.apiClasses.apiClasses import *
from server import *

server = Server()

class DatabaseRequests:
    def __init__(self):
        pass

    def insert_tournament(self, name: str, period: int , anz_teams: int ):
        """
        TODO Dokumentation
        """
        try:
            server.execute("""INSERT INTO Turnier (TurnierBez, Spieldauer, TeamAnz)
                                    VALUES (?,?,?)""",[name, period, anz_teams])
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Hinzufügen von Daten! ")

    def insert_stages(self, name: str, team_size: int):
        """
        TODO Dokumentation
        """
        try: 
            server.execute("""INSERT INTO Leistungsgruppen (Leistungsgruppenname,AnzTeamsLeist) 
                                        VALUES (?,?)""",[name,team_size])
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Hinzufügen von Daten! ")

    def get_tournament_id(self):
        """
        TODO Die ID des zuletzt erstellten Turniers wird geholt.
        """
        try:
            tournament_id = server.query("SELECT MAX(TurnierID) FROM Turnier ")
            tournament_id = tournament_id[0][0]
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Abfrage von Daten! ")
        
        if type(tournament_id) == int:
            return tournament_id
        else:
            return None
    

    def insert_tournament_data(self, tournament_id: int, team1: str, team2: str, referee: str, field: int, stage_name: str, play_time: str):
        """
        TODO Dokumentation
        """
        # Überprüft ob die Teams bereits in der Datenbank eingetragen worden sind 
        try:
            team1_is_inserted = server.query("SELECT * FROM Team WHERE TurnierID = ? AND Teamname Like ? ",[tournament_id, team1])
            team2_is_inserted = server.query("SELECT * FROM Team WHERE TurnierID = ? AND Teamname Like ? ",[tournament_id, team2])
            referee_is_inserted = server.query("SELECT * FROM Team WHERE TurnierID = ? AND Teamname Like ? ",[tournament_id, referee])

            stage_id = server.query("SELECT MAX(LeistungsgruppenID) FROM Leistungsgruppen WHERE Leistungsgruppenname LIKE ? ",[stage_name])
            stage_id = stage_id[0][0]
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Abfrage von Daten! ")
    
        # Wenn die Teams noch nicht in der Datenbank existiert werden sie eingetragen 
        if team1_is_inserted == []:
            try:
                server.execute("INSERT INTO Team (TurnierID, LeistungsgruppenID, Teamname) VALUES (?,?,?)",[tournament_id, stage_id, team1])
            except Exception as e:
                raise HTTPException(status_code=500, detail="Datenbankfehler beim Hinzufügen von Daten! ")

        if team2_is_inserted == []:
            try:
                server.execute("INSERT INTO Team (TurnierID, LeistungsgruppenID, Teamname) VALUES (?,?,?)",[tournament_id, stage_id, team2]) 
            except Exception as e:
                raise HTTPException(status_code=500, detail="Datenbankfehler beim Hinzufügen von Daten! ")                

        if referee_is_inserted == []:
            try:
                server.execute("INSERT INTO Team (TurnierID, LeistungsgruppenID, Teamname) VALUES (?,?,?)",[tournament_id, stage_id, referee]) 
            except Exception as e:
                raise HTTPException(status_code=500, detail="Datenbankfehler beim Hinzufügen von Daten! ")
        
        # Die IDs Der Teams die an dem Spiel Teilnehmen werden Abgefragt
        try:
            team1_id= server.query("SELECT TeamID FROM Team WHERE TurnierID = ? AND Teamname Like ?",[tournament_id, team1])
            team2_id = server.query("SELECT TeamID FROM Team WHERE TurnierID = ? AND Teamname Like ?",[tournament_id, team2])
            referee_id = server.query("SELECT TeamID FROM Team WHERE TurnierID = ? AND Teamname Like ?",[tournament_id, referee])
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Abfrage von Daten! ")
        
        # Das Spiel wird in die Ergebnisse Tabelle Eingetragen
        if team1_id != [] and team2_id != [] and referee_id != []:
            try:
                server.execute("""INSERT INTO Ergebnisse (TeamID1, TeamID2, SchiedsrichterID, Spielergebnis1 ,Spielergebnis2, SpielfeldNr, Uhrzeit)
                                    VALUES (?,?,?,?,?,?,?)""",[team1_id[0][0], team2_id[0][0], referee_id[0][0], 0, 0, field, play_time])
            except Exception as e:
                raise HTTPException(status_code=500, detail="Datenbankfehler beim Hinzufügen von Daten! ")
            
    def get_existing_tournaments(self):
        """
        TODO Dokumentation
        """
        return_data = []
        try:
            get_tournament_data = server.query("SELECT TurnierID, TurnierBez FROM Turnier")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Abfrage von Daten! ")
        
        # TODO für Turnierauswahl nur Namen oder auch ID 
        for tournament in get_tournament_data:
            if type(tournament[0]) == int and type(tournament[1]) == str:
                return_data.append({"id":tournament[0],"name":tournament[1]})
        
        return return_data

    def get_tournament_plan(self, tournament_id: int):
        """
        TODO Dokumentation
        """
        return_date = []
        try:
            data = server.query("""SELECT DISTINCT e.SpielID, e.SpielfeldNr,
                                                   t1.TeamID, t2.TeamID, t3.TeamID,
                                                   t1.Teamname, t2.Teamname, t3.Teamname,
                                                   l.Leistungsgruppenname, e.Spielergebnis1, e.Spielergebnis2, e.Uhrzeit
                                   FROM Ergebnisse e 
                                   JOIN Team t1 ON t1.TeamID = e.TeamID1 
                                   JOIN Team t2 ON t2.TeamID = e.TeamID2 
                                   JOIN Team t3 ON t3.TeamID = e.SchiedsrichterID  
                                   JOIN Leistungsgruppen l ON l.LeistungsgruppenID = t1.LeistungsgruppenID  
                                   WHERE t1.TurnierID = ?""",[tournament_id])
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Abfrage von Daten! ")

        # Überprüfen der Werte und die übergabe der Werte in ein dictionary für die Rückgabe 
        if  type(data) == list:
            for game in data:
                # t_data = TournamentPlan(**{"game_id": game[0], "field_number": game[1], "team1_id": game[2], "team2_id": game[3], "referee_id": game[4],
                #                            "team1": game[5], "team2": game[6], "referee": game[7], "stage_name": game[8],
                #                            "score_team1": game[9], "score_team2": game[10], "time_of_game": game[11] })
                t_data = TournamentPlan(game_id=game[0], field_number=game[1], team1_id=game[2], team2_id=game[3],referee_id=game[4],
                                        team1=game[5], team2=game[6], referee=game[7], stage_name=game[8], score_team1=game[9], score_team2=game[10], time_of_game=game[11])
                # t_data=TournamentPlan(*game)
                return_date.append({"game_id":t_data.game_id, "team_ids":[t_data.team1_id, t_data.team2_id, t_data.referee_id],
                                    "team_names":[t_data.team1, t_data.team2,t_data.referee], "scores":[t_data.score_team1, t_data.score_team2 ],
                                    "stage_name":t_data.stage_name, "field":t_data.field_number, "play_time":t_data.time_of_game})
        else:
            print("Abfrage der Datenbank ist Fehlgeschlagen.")

        return return_date
    
    def get_matches(self, match_id: int):
        """
        TODO Dokumentation
        """
        return_data = []
        try:
            match_data = server.query("SELECT Spielergebnis1, Spielergebnis2 FROM Ergebnisse WHERE SpielID = ?",[match_id])
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Abfrage von Daten! ")

        # validate Data
        if len(match_data) == 1:
            return_data.append(match_data[0][0])
            return_data.append(match_data[0][1])

        return return_data   
  
    def change_results(self, match_id: int, score1: int, score2: int, time_change: str):
        """
        TODO Dokumentation
        """
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
                                        VALUES (?,?,?,?)""",[match_id, old_score_team1[0][0] , old_score_team2[0][0] ,time_change])
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=" Datenbankfehler beim ändern von Daten! ")
        
    def change_team_name(self, tournament_id: int, team_id: int,new_name: str):
        """
        TODO Dokumentation
        """
        try:
            team_name_exist = server.query("SELECT Count(*) FROM Team WHERE TurnierID = ? AND Teamname LIKE ?",[tournament_id,new_name])
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Abfrage von Daten! ")
        
        if team_name_exist[0][0] == 0:
            try:
                server.execute("UPDATE Team SET Teamname = ? WHERE TeamID = ?",[new_name,team_id])
            except Exception as e:
                raise HTTPException(status_code=500, detail="Datenbankfehler beim ändern von Daten! ")
        else:
            raise HTTPException(status_code=409, detail="Teamname existiert bereits")

        
    def delete_tournament(self, tournament_id: int):
        """
        TODO Dokumentation
        """
        try:
            server.execute("DELETE FROM Turnier WHERE TurnierID = ?", [tournament_id])

            server.execute("""DELETE FROM Leistungsgruppen
                                    WHERE LeistungsgruppenID NOT IN (
                                    SELECT DISTINCT LeistungsgruppenID FROM Team)""")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Löschen von Daten! ")

