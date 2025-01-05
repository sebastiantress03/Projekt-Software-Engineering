from pydantic import BaseModel

class Score(BaseModel):
    teamID1: int
    teamID2: int
    spielergebnis1: int 
    spielergebnis2: int
    hinRückspiel: str

class ScoreChange(BaseModel):
    spielergebnis1: int 
    spielergebnis2: int