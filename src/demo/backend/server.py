import sqlite3
import os

class Server:
    def __init__(self):
        self.initializing_database()

    # Erstellen der Datenbankstruktur 
    def initializing_database(self):
        try:
            with sqlite3.connect(os.path.join("data","vtDatenbase.db")) as connection:
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
                                Uhrzeit             TIME,
                                FOREIGN KEY (TeamID1) REFERENCES Team(TeamID) ON DELETE CASCADE,
                                FOREIGN KEY (TeamID2) REFERENCES Team(TeamID) ON DELETE CASCADE,
                                FOREIGN KEY (SchiedsrichterID) REFERENCES Team(TeamID) ON DELETE CASCADE
                               )""")
                
                cursor.execute("""CREATE TABLE IF NOT EXISTS Aenderungen(
                                AenderungsID            INTEGER PRIMARY KEY AUTOINCREMENT,
                                SpielID                 INTEGER,
                                alteSpielergebnis1      INTEGER,
                                alteSpielergebnis2      INTEGER,
                                Uhrzeitaenderung        TiME,
                                ForeignKey (SpielID) REFERENCES Ergebnisse(SpielID) ON DELETE CASCADE,
                               )""")

        except Exception as exception:
            print(f"Error initializing database: {exception}")

    def query(self,query="",attributes=[]):
        try:
            with sqlite3.connect(os.path.join("data","vtDatenbase.db")) as connection:
                connection.execute("PRAGMA foreign_keys = ON")
                cursor = connection.cursor()
                cursor.execute(query,attributes)
                data = cursor.fetchall()
                return data

        except Exception as exception:
            print(f"Error executing query: {exception}")
            return False
    
    # TODO Eventuell nicht nötig, überprüfen
    def execute(self, query="", attributes=[]):
        try:
            with sqlite3.connect(os.path.join("data","vtDatenbase.db")) as connection:
                connection.execute("PRAGMA foreign_keys = ON")
                cursor = connection.cursor()
                cursor.execute(query, attributes)
                connection.commit()
                return True
            
        except Exception as exception:
            print(f"Error executing query: {exception}")
            return False