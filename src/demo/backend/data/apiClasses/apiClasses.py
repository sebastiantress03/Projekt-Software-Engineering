from enum import Enum
from pydantic import BaseModel,validator,root_validator
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
    number_of_fields: int                           # mindestes 1 Feld maximal 4 ist noch zu klären 
    return_match: ReturnMatchOption                 # das returnmaches exists 
    number_of_stages: int
    time_to_start: time                             # Uhrzeit # wert wird schon von Pydantic überprüft ob es sich um eine Time objekt handelt 
    game_time: int                                  # in min
    warm_up_time: int                               # in min
    number_of_breaks: int
    break_length: Optional[List[int]] = None 
    stage_name: List[str]          
    number_of_teams: List[int]
    break_times: Optional[List[time]] = None

    @validator('number_of_fields')
    def right_number_of_fields(cls, v):
        if v < 0:
            raise ValueError("Felder anzahl kann nicht negativ sein! ")
        elif v > 5:
            raise ValueError("Felder anzahl ist zu groß! ")
        return v
        
    @validator('number_of_stages')
    def anz_stages(cls, v):
        if v < 0:
            raise ValueError("Negative Anzahl an Leistungsgruppen ist nicht möglich! ")
        elif v > 2:
            raise ValueError("Maximal 2 Leistungsgruppen! ")
        return v
        
    @validator('game_time','warm_up_time')
    def time_of_game(cls, v, field):
        if not isinstance(v,int):
            raise ValueError(f"{field.name} ist nicht valide! ")
        elif v > 60:
            raise ValueError(f"{field.name} ist zu groß! ")
        return v
    
    @validator('number_of_breaks')
    def valid_anz_breaks(cls,v):
        if v < 0:
            raise ValueError("Die Anzahl der Pausen kann nicht negativ sein! ")
        return v
    
    @validator('break_length', each_item=True)
    def validate_break_length(cls, v):
        if v < 1 or v > 60:
            raise ValueError("Pausenlänge muss zwischen 1 und 60 Minuten liegen.")
        return v
    
    @validator('stage_name', each_item=True)
    def stage_name_exist(cls, v):
        if isinstance(v, str):
            raise ValueError("Leistungsgruppennamen müssen Strings sein")
        return v
    
    @validator('break_times', each_item=True)
    def validate_break_time_format(cls, v):
        if not isinstance(v, time):
            raise ValueError(f"Ungültige Zeit: {v}. Die Zeit muss im Format HH:MM sein.")
        return v

    @root_validator
    def check_breaks_and_lengths(cls, v):
        breaks = v.get('number_of_breaks')
        lengths = v.get('break_length')
        time_breaks = v.get('break_times') 

        if breaks == 0:
            if lengths not in (None, [], ()) or time_breaks not in (None, [], ()):
                raise ValueError("Es wurden keine Pausen angegeben, aber Pausenlängen sind gesetzt.")
        elif breaks is not None and lengths is not None and time_breaks is not None:
            if len(lengths) != breaks or len(time_breaks) != breaks:
                raise ValueError(f"{breaks} Pausen erwartet, aber {len(lengths)} Pausenlängen und {len(time_breaks)} Pausezeiten angegeben.")
        return v
    
    @root_validator(skip_on_failure=True)
    def check_stage_names_and_anz_stages(cls, v):
        anz_stages = v.get('number_of_stages')
        stage_names = v.get('')
        if anz_stages is not None and stage_names is not None:
            if len(stage_names) != anz_stages:
                raise ValueError(f"{anz_stages} Namen von Leistungsgruppen erwarted und {len(stage_names)} erhalten")
        return v



class Match(BaseModel):
    score_team1: int 
    score_team2: int
    time_change: time

    @validator('score_team1', 'score_team2')
    def scores_must_be_positive(cls, v, field):
        if v < 0:   
            raise ValueError(f"{field.name} darf nicht negativ sein! ")
        return v

    @validator('time_change')
    def valid_time(cls,v):

        if isinstance(v,float):
            hours = int(v)
            min = int((v-hours) * 60)
            v = time(hours,min)

        if not isinstance(v, time):
            raise ValueError("Änderungszeit ist nicht valide !")
        return v


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

    @validator('game_number')
    def check_game_number(cls, v):
        if v < 1:
            raise ValueError("Spielnummer kann nicht kleiner 1 sein! ")
        return v

    @validator('field_number')
    def check_field_number(cls,v):
        if v < 1:
            raise ValueError(f"Es muss mindestend ein Feld existieren! ")
        elif v > 5:
            raise ValueError(f"Es sind maximal 5 Felder zulässig! ")
        return v
    
    @validator('team1','team2','referee')
    def check_teams(cls, v, field):
        if not isinstance(v, str):
            raise ValueError(f"{field.name} muss ein String sein")
        return v

    @validator('stage_name')
    def check_stage_names(cls,v ):
        if not isinstance(v, str):
            raise ValueError("Leistungsgruppe muss ein String sein")
        return v
    
    @validator('score_team1', 'score_team2')
    def scores_must_be_positive(cls, v, field):
        if v < 0:   
            raise ValueError(f"{field.name} darf nicht negativ sein! ")
        return v
    
class TeamUpdate(BaseModel):
    team_id: int
    new_name: str

    @validator('new_name')
    def check_new_name(cls,v):
        if not isinstance(v,str):
            raise ValueError("Bei dem Teamnamen muss es sich um ein String handeln")
        return v
    
    @validator('team_id')
    def check_team_id(cls,v):
        if not isinstance(v,int):
            raise ValueError("Bei dem Teamnamen muss es sich um ein String handeln")
        return v