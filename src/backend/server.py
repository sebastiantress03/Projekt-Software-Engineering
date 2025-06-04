import sqlite3
import os

class Server:
    def __init__(self):
        self.initializing_database()

    # Erstellen der Datenbankstruktur 
    def initializing_database(self):
        """
        Erstellt die Datenbankstruktur für das Turnierverwaltungssystem.

        Falls die Datenbankdatei noch nicht existiert, wird sie neu erstellt.
        Anschließend werden die erforderlichen Tabellen angelegt, falls sie noch nicht existieren:

            - Turnier
            - Leistungsgruppen
            - Team
            - Ergebnisse
            - Aenderungen

        Fehlerbehandlung:
            - Gibt eine Fehlermeldung aus, falls die Datenbank nicht geöffnet oder erstellt werden kann.

        Hinweise:
            - Die Datenbankdatei wird unter "data/vtDatabase.db" gespeichert.
            - Bei Fehlern wird keine Exception geworfen, sondern eine Fehlermeldung ausgegeben.
        """
        try:
            # Überprüft ob die Datenbank bereits existiert
            if not os.path.exists(os.path.join("data","vtDatabase.db")):
                try:
                    with open(os.path.join("data","vtDatabase.db"),"w+") as file:
                        file.close()
                except Exception as e:
                    print(f"Database could not be opened: {e}")
                
            # Datenbankstruktur
            with sqlite3.connect(os.path.join("data","vtDatabase.db")) as connection:
                cursor = connection.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS Turnier(
                                TurnierID               INTEGER PRIMARY KEY AUTOINCREMENT,
                                TurnierBez              VARCHAR,
                                Spieldauer              INTEGER,
                                TeamAnz                 INTEGER
                                )""")
                
                cursor.execute("""CREATE TABLE IF NOT EXISTS Leistungsgruppen(
                                LeistungsgruppenID      INTEGER PRIMARY KEY AUTOINCREMENT,
                                Leistungsgruppenname    VARCHAR,
                                AnzTeamsLeist           INTEGER
                                )""")

                cursor.execute("""CREATE TABLE IF NOT EXISTS Team (
                                TeamID                  INTEGER PRIMARY KEY AUTOINCREMENT,
                                TurnierID               INTEGER,
                                LeistungsgruppenID      INTEGER,
                                Teamname                VARCHAR,
                                FOREIGN KEY (TurnierID) REFERENCES Turnier(TurnierID) ON DELETE CASCADE,
                                FOREIGN KEY (LeistungsgruppenID) REFERENCES Leistungsgruppen(LeistungsgruppenID) ON DELETE CASCADE
                                )""")

                cursor.execute("""CREATE TABLE IF NOT EXISTS Ergebnisse (
                                SpielID             INTEGER PRIMARY KEY AUTOINCREMENT,
                                TeamID1             INTEGER,
                                TeamID2             INTEGER,
                                SchiedsrichterID    INTEGER, 
                                Spielergebnis1      INTEGER,
                                Spielergebnis2      INTEGER,
                                SpielfeldNr         INTEGER,
                                Uhrzeit             VARCHAR,
                                FOREIGN KEY (TeamID1) REFERENCES Team(TeamID) ON DELETE CASCADE,
                                FOREIGN KEY (TeamID2) REFERENCES Team(TeamID) ON DELETE CASCADE,
                                FOREIGN KEY (SchiedsrichterID) REFERENCES Team(TeamID) ON DELETE CASCADE
                                )""")
                
                cursor.execute("""CREATE TABLE IF NOT EXISTS Aenderungen (
                                AenderungsID            INTEGER PRIMARY KEY AUTOINCREMENT,
                                SpielID                 INTEGER,
                                alteSpielergebnis1      INTEGER,
                                alteSpielergebnis2      INTEGER,
                                Uhrzeitaenderung        VARCHAR,
                                FOREIGN KEY (SpielID) REFERENCES Ergebnisse(SpielID) ON DELETE CASCADE
                                )""")

        except Exception as exception:
            print("Error initializing database! ")

    # Erhalt der Datenbankabfrage als Liste
    def query(self,query="",attributes=[]):
        """
        Führt eine SELECT-Abfrage auf der SQLite-Datenbank aus und gibt die Ergebnisse zurück.

        Parameter:
            - query (str): Die SQL-Abfrage, die ausgeführt werden soll.
            - attributes (list): Eine Liste von Attributen/Parametern, die in der Abfrage eingesetzt werden.

        Beispiel:
            - query("SELECT * FROM Team WHERE TurnierID = ? AND Teamname Like ? ",[tournament_id, team1])

        Rückgabewert:
            - list: Eine Liste der Datensätze, die der Abfrage entsprechen (z.B. als Liste von Tupeln).
            - bool: False, falls bei der Abfrage ein Fehler auftritt.

        Fehlerbehandlung:   
            - Fehler werden über die Konsole ausgegeben.

        Hinweise:
            - Es werden nur Leseoperationen unterstützt (z.B. SELECT).
            - Fremdschlüsselbeschränkungen werden aktiviert (PRAGMA foreign_keys = ON).    
        """
        try:
            with sqlite3.connect(os.path.join("data","vtDatabase.db")) as connection:
                connection.execute("PRAGMA foreign_keys = ON")
                cursor = connection.cursor()
                cursor.execute(query,attributes)
                data = cursor.fetchall()
                return data

        except Exception as exception:
            print("Error executing query! ")
            # return False
            raise Exception
    
    # Verändern der Datenbank (Inserts und Updates)
    def execute(self, query="", attributes=[]):
        """
        Führt eine Änderungsoperation (z.B. INSERT, UPDATE, DELETE) auf der SQLite-Datenbank aus.

        Parameter:
            - query (str): Die SQL-Anweisung, die ausgeführt werden soll.
            - attributes (list): Eine Liste von Werten, die in der SQL-Anweisung eingesetzt werden.

        Beispiel:
            - execute("INSERT INTO Team (TurnierID, LeistungsgruppenID, Teamname) VALUES (?,?,?)",[tournament_id, stage_id, team1])

        Rückgabewert:
            - bool:
                - True, wenn die Operation erfolgreich war.
                - False, wenn ein Fehler auftritt.
        
        Fehlerbehandlung:   
            - Fehler werden über die Konsole ausgegeben.

        Hinweise:
            - Die Änderungen werden direkt nach der Ausführung in die Datenbank aufgenommen (commit).
            - Fremdschlüsselbeschränkungen werden aktiviert (PRAGMA foreign_keys = ON).
        """
        try:
            with sqlite3.connect(os.path.join("data","vtDatabase.db")) as connection:
                connection.execute("PRAGMA foreign_keys = ON")
                cursor = connection.cursor()
                cursor.execute(query, attributes)
                connection.commit()
                return True
            
        except Exception as exception:
            print(f"Error executing execute! ")
            return False