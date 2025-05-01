from enum import Enum
from pydantic import BaseModel
from datetime import time
from typing import List, Optional

'''schedule.append({
        "Spiel": 0,
        "Feld": "All Fields",
        "Uhrzeit": current_time.strftime("%H:%M"),
        "Team 1": "Warm-up",
        "Team 2": "Warm-up",
        "Schiedsrichter": "Not required",
        "Gruppe": "N/A",
        "Ergebnis Team 1": None,
        "Ergebnis Team 2": None,
    })'''

class ReturnMatchOption(str, Enum):
    TRUE = "true"
    FALSE = "false"

class GenerateTournament(BaseModel):
    tournament_name: str
    number_of_fields: int
    return_match: ReturnMatchOption                 # das returnmaches exists 
    number_of_stages: int
    time_to_start: time                             # Uhrzeit
    game_time: int                                  # in min
    warm_up_time: int                               # in min
    number_of_breaks: int
    break_lenght: Optional[List[int]] = None 
    stage_name: Optional[List[str]] = None 
    number_of_teams: Optional[List[int]] = None 
    break_times: Optional[List[time]] = None        

class Match(BaseModel):
    score_team1: int 
    score_team2: int
    time_change: time

class TurnamentPlan(BaseModel):
    game_number: int
    field_number: int
    team1: str              # Leistungsgruppe(ersten 2 Buchstaben) + Team + Nummer 
    team2: str           
    referee: str 
    stage_name: str
    score_team1: int
    score_team2: int
    time_of_game: time
