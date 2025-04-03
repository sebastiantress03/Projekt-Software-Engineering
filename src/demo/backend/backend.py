import fastapi
import sqlite3
import os
from data.apiClasses.apiClasses import *
from fastapi.middleware.cors import CORSMiddleware



class Server:
    def __init__(self):
        self.initializing_database()
        #self.query("INSERT INTO Ergebnisse (TeamID1,TeamID2,Spielergebnis1,Spielergebnis2,HinRückspiel) VALUES (?,?,?,?,?)",[1,2,15,21,"Hinspiel"])
        #self.query("INSERT INTO Ergebnisse (TeamID1,TeamID2,Spielergebnis1,Spielergebnis2,HinRückspiel) VALUES (?,?,?,?,?)",[1,2,15,18,"Rückspiel"])

    def initializing_database(self):
        try:
            with sqlite3.connect(os.path.join("data","vtDatenbase.db")) as connection:
                cursor = connection.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS Ergebnisse (
                                SpielID          INTEGER PRIMARY KEY AUTOINCREMENT,
                                TeamID1          INTEGER,
                                TeamID2          INTEGER,
                                Spielergebnis1   INTEGER,
                                Spielergebnis2   INTEGER,
                                HinRückspiel     varchar)
                               """)

        except Exception as exception:
            print(f"Error initializing database: {exception}")

    def query(self,query="",attributes=[]):
        try:
            with sqlite3.connect(os.path.join("data","vtDatenbase.db")) as connection:
                cursor = connection.cursor()
                cursor.execute(query,attributes)
                data = cursor.fetchall()
                return data

        except Exception as exception:
            print(f"Error executing query: {exception}")


server = Server()
api = fastapi.FastAPI()

origins = [
    "*"
]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def check_received_data():
    pass

@api.get("/")
def get_main_data():
    data = server.query("SELECT * FROM Ergebnisse")
    if data != None and len(data) != 0:
        return {"data": data}
    else:
        return fastapi.HTTPException(status_code=404,detail="ERROR while fetching data")

@api.post("/scores/")
def set_scores(score:Score):
    data = server.query("INSERT INTO Ergebnisse (TeamID1,TeamID2,Spielergebnis1,Spielergebnis2,HinRückspiel) VALUES (?,?,?,?,?)",[score.teamID1,score.teamID2,score.spielergebnis1,score.spielergebnis2,score.hin_rückspiel])
    if data != None:
        return fastapi.HTTPException(status_code=200,detail="SUCCESS")
    else:
        return fastapi.HTTPException(status_code=404,detail="ERROR while fetching data")
    
@api.put("/scores/{scoresID}")
def change_scores(scoresID: str, score:ScoreChange):
    data = server.query("UPDATE Ergebnisse SET Spielergebnis1 = ?, Spielergebnis2 = ? WHERE SpielID = ?",[score.spielergebnis1,score.spielergebnis2, int(scoresID) ])
    if data != None:
        return fastapi.HTTPException(status_code=200,detail="SUCCESS")
    else:
        return fastapi.HTTPException(status_code=404,detail="ERROR while fetching data")