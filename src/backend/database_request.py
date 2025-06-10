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
        Führt ein INSERT INTO auf die SQL-Tabelle "Turnier" aus und fügt dadurch ein neues Turnier hinzu.

        Parameter:
            - name (str): Die Bezeichnung des Turniers, die in die Tabelle eingetragen werden soll.
            - period (int): Die Spielzeit (in Minuten), die pro Spiel eingeplant werden soll.
            - anz_teams (int): Die Gesamtanzahl der Teams, die am Turnier teilnehme.

        Beispiel:
            - insert_tournament("Nikolaus Turnier" ,20,16)

        Fehlermeldung:
            - Falls beim Hinzufügen der Daten in die Datenbank ein Fehler auftritt, wird eine HTTPException mit dem Statuscode 500 ausgelöst.
        
        Hinweise:
            Es wird nicht das gesamte Turnier erfasst, sondern lediglich der Name, die Spieldauer und die Anzahl der teilnehmenden Teams.
        """
        try:
            server.execute("""INSERT INTO Turnier (TurnierBez, Spieldauer, TeamAnz)
                                    VALUES (?,?,?)""",[name, period, anz_teams])
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Hinzufügen von Daten! ")

    def insert_stages(self, name: str, team_size: int):
        """
        Führt ein INSERT INTO auf die SQL-Tabelle "Leistungsgruppen" aus und fügt eine neue Leistungsgruppe hinzu.

        Parameter:
            - name (str): Der Name der Leistungsgruppe, die in die Tabelle eingetragen werden soll.
            - team_size (int): Die Anzahl der Teams die Teil der Leistungsgruppe sind.

        Beispiel:
            - insert_stages("Anfänger" , 8)

        Fehlermeldung:
           - Falls beim Hinzufügen der Daten in die Datenbank ein Fehler auftritt, wird eine HTTPException mit dem Statuscode 500 ausgelöst.

        Hinweis:
            - Doppelte Namen für Leistungsgruppen können existieren.
        """
        try: 
            server.execute("""INSERT INTO Leistungsgruppen (Leistungsgruppenname,AnzTeamsLeist) 
                                        VALUES (?,?)""",[name,team_size])
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Hinzufügen von Daten! ")

    def get_tournament_id(self):
        """
        Führt eine SELECT-Abfrage auf das "Turnier" aus, um die neuste TurnierID zu erhalten.

        Rückgabewert:
            - int: Die ID des neuesten Turniers.
            - None: Falls bei der SQL-Abfrage ein Fehler aufgetreten ist.

        Fehlermeldung:
           - Falls beim Abfragen der Daten aus der Datenbank ein Fehler auftritt, wird eine HTTPException mit dem Statuscode 500 ausgelöst.

        Hinweis:
            - Die Abfrage erfolgt mithilfe von MAX ausgeführt.
            - Es wird davon ausgegangen, dass Turniere mit fortlaufend steigenden IDs erstellt werden, sodass das Turnier mit der höchsten ID dem neuesten entspricht.
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
        Fügt ein neues Spiel in die Tabelle "Ergebnisse" ein. Falls die beteiligten Teams oder der Schiedsrichter noch nicht existieren, 
        werden sie automatisch in die Tabelle "Team" aufgenommen.
        
        Parameter:
            - tournament_id (int): Die ID des Turniers, zu dem das Spiel gehört.
            - team1 (str): Der Name ersten Teams.
            - team2 (str): Der Name zweiten Teams.
            - referee (str): Der Name des Schiedsrichterteams.
            - field (int): Die Nummer des Spielfelds, auf dem das Spiel stattfindet.
            - stage_name (str): Der Name der Leistungsgruppe, zu der die Teams gehören.
            - play_time (str): Die Uhrzeit, zu der das Spiel geplant ist (Format: "HH:MM").
        
        Beispiel:
            - insert_tournament_data(1 ,"Team1" ,"Team2" ,"Team3" ,1 ,"Anfänger" , "10:00")
        
        Fehlermeldung:
            - Falls beim Abrufen oder Einfügen von Daten in die Datenbank ein Fehler auftritt, wird eine HTTPException mit dem Statuscode 500 ausgelöst.

        Hinweis:
            - Teams und Schiedsrichter werden nur dann neu eingetragen, wenn sie noch nicht in der Datenbank vorhanden sind.
            - Die Zuordnung der Teams zur Leistungsgruppe erfolgt anhand des Namens.
            - Spielstände werden beim Einfügen initial auf 0 gesetzt.
        """
        # Überprüft ob die Teams bereits in der Datenbank eingetragen worden sind 
        try:
            team1_is_inserted = server.query("SELECT * FROM Team WHERE TurnierID = ? AND Teamname Like ? ",[tournament_id, team1])
            team2_is_inserted = server.query("SELECT * FROM Team WHERE TurnierID = ? AND Teamname Like ? ",[tournament_id, team2])
            referee_is_inserted = server.query("SELECT * FROM Team WHERE TurnierID = ? AND Teamname Like ? ",[tournament_id, referee])

            stage_id = server.query("SELECT MAX(LeistungsgruppenID) FROM Leistungsgruppen WHERE Leistungsgruppenname LIKE ? ",[stage_name])
            print(f"stageid vor [0][0] {stage_id}")
            stage_id = stage_id[0][0]
            print(f"stageid nach [0][0] {stage_id}")

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
        Ruft alle bestehenden Turniere mit deren IDs und Bezeichnungen aus der Datenbank ab.

        Rückgabewert:
            - list[dict]: Eine Liste von Dictionaries mit den Schlüsseln:
                - "id" (int): Die ID des Turniers.
                - "name" (str): Die Bezeichnung des Turniers.

        Fehlermeldung:
            - Falls beim Abrufen der Daten ein Datenbankfehler auftritt, wird eine HTTPException mit Statuscode 500 ausgelöst.
        """
        return_data = []
        try:
            get_tournament_data = server.query("SELECT TurnierID, TurnierBez FROM Turnier")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Abfrage von Daten! ")
        
        # Rückgabewerte für die Turnierauswahl mit Namen und ID 
        for tournament in get_tournament_data:
            if type(tournament[0]) == int and type(tournament[1]) == str:
                return_data.append({"id":tournament[0],"name":tournament[1]})
        
        return return_data

    def get_tournament_plan(self, tournament_id: int):
        """
        Ruft den Spielplan (Ergebnisse) für ein bestimmtes Turnier ab und gibt alle relevanten Spieldaten zurück.

        Parameter:
            - tournament_id (int): Die ID des Turniers, dessen Spielplan abgerufen werden soll.

        Rückgabewert:
            - list[dict]: Eine Liste von Dictionaries mit folgenden Schlüsseln und Datentypen:
                - "game_id" (int): Die eindeutige ID des Spiels.
                - "team_ids" (list[int]): Liste der IDs der beteiligten Teams und des Schiedsrichters [Team1, Team2, Schiedsrichter].
                - "team_names" (list[str]): Liste der Namen der beteiligten Teams und des Schiedsrichters [Team1, Team2, Schiedsrichter].
                - "scores" (list[int]): Liste der Spielergebnisse [Punkte Team1, Punkte Team2].
                - "stage_name" (str): Name der Leistungsgruppe.
                - "field" (int): Nummer des Spielfelds.
                - "play_time" (str): Uhrzeit des Spiels (z. B. "10:00").

        Fehlermeldung:
            - Falls beim Abrufen der Daten ein Datenbankfehler auftritt, wird eine HTTPException mit Statuscode 500 ausgelöst.

        Hinweis:
            - Die Daten werden aus mehreren Tabellen verknüpft, um alle notwendigen Informationen zu sammeln.
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
        Ruft die Spielergebnisse (Punkte) eines bestimmten Spiels anhand der Spiel-ID ab.

        Parameter:
            - match_id (int): Die ID des Spiels.

        Rückgabewert:
            - list[int]: Eine Liste mit zwei Elementen [Spielergebnis1, Spielergebnis2]. Ist kein Ergebnis vorhanden, wird eine leere Liste zurückgegeben.

        Fehlermeldung:
            - Falls beim Abrufen der Daten ein Datenbankfehler auftritt, wird eine HTTPException mit Statuscode 500 ausgelöst.
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
        Ändert die Spielergebnisse eines Spiels und protokolliert die Änderung mit Zeitstempel.

        Parameter:
            - match_id (int): Die ID des Spiels, dessen Ergebnisse geändert werden sollen.
            - score1 (int): Neues Ergebnis für Team 1.
            - score2 (int): Neues Ergebnis für Team 2.
            - time_change (str): Zeitpunkt der Änderung (z.B. "15:00").

        Rückgabewert:
            - bool: True, wenn die Änderung erfolgreich durchgeführt wurde.

        Fehlermeldung:
            - Falls das Spiel nicht existiert, wird eine HTTPException mit Statuscode 400 ausgelöst.
            - Falls ein Datenbankfehler beim Abrufen oder Ändern der Daten auftritt, wird eine HTTPException mit Statuscode 500 ausgelöst.
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
        Ändert den Namen eines Teams in einem bestimmten Turnier, sofern der neue Name noch nicht vergeben ist.

        Parameter:
            - tournament_id (int): Die ID des Turniers.
            - team_id (int): Die ID des Teams, dessen Name geändert werden soll.
            - new_name (str): Der neue Teamname.

        Fehlermeldung:
            - Falls der neue Teamname bereits existiert, wird eine HTTPException mit Statuscode 409 ausgelöst.
            - Falls ein Datenbankfehler beim Abfragen oder Ändern der Daten auftritt, wird eine HTTPException mit Statuscode 500 ausgelöst.
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
        Löscht ein Turnier anhand der TurnierID aus der Datenbank. 
        Zusätzlich werden Leistungsgruppen entfernt, die danach nicht mehr von Teams genutzt werden.

        Parameter:
            - tournament_id (int): Die ID des zu löschenden Turniers.

        Fehlermeldung:
            - Falls beim Löschen aus der Datenbank ein Fehler auftritt, wird eine HTTPException mit Statuscode 500 ausgelöst.

        Hinweis:
            - Leistungsgruppen werden nur dann gelöscht, wenn sie keiner Mannschaft mehr zugeordnet sind.
        """
        try:
            server.execute("DELETE FROM Turnier WHERE TurnierID = ?", [tournament_id])

            server.execute("""DELETE FROM Leistungsgruppen
                                    WHERE LeistungsgruppenID NOT IN (
                                    SELECT DISTINCT LeistungsgruppenID FROM Team)""")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Datenbankfehler beim Löschen von Daten! ")
    
    