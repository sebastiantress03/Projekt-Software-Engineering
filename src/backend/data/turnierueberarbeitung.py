import random
from datetime import datetime, timedelta
from turnierplangenerator_4 import (
    create_tournament_plan,
    return_plan,
    create_html
)


def extrahiere_zeiten(schedule):
    """
    Ermittelt alle eindeutigen Spielzeiten aus dem Spielplan.

    Parameter:
        - schedule (list): Liste der Matches, die Dictionaries mit 'Uhrzeit' und 'Match Type' enthalten.

    Beispiel:
        - extrahiere_zeiten(schedule)

    Rückgabewert:
        - list[datetime.time]: Sortierte Liste der Zeitpunkte (nur von Matches mit Match Type)

    Fehlerbehandlung:
        - Keine

    Hinweise:
        - Zeiten werden als `datetime.time`-Objekte zurückgegeben.
        - „Pausen“ werden übersprungen.
    """

    zeiten = {
        datetime.strptime(m["Uhrzeit"], "%H:%M").time()
        for m in schedule
        if "Match Type" in m
    }
    return sorted(zeiten)

def initialisiere_status_lists(teams, zeiten):
    """
    Initialisiert für jedes Team eine Statusliste aus 'F' (frei) über alle Zeitslots.

    Parameter:
        - teams (dict): Team-ID → Teamdaten (Name, Gruppe, …)
        - zeiten (list): Liste aller Spielzeitpunkte

    Beispiel:
        - initialisiere_status_lists(teams, zeiten)

    Rückgabewert:
        - dict: team_id → Liste mit 'F' (ein Eintrag pro Zeitslot)

    Fehlerbehandlung:
        - Keine

    Hinweise:
        - Grundlage für die spätere Markierung von Spielen ('S') und Pfeifen ('P')
    """

    return {tid: ['F'] * len(zeiten) for tid in teams}

def slot_index(uhrzeit_str, zeiten):
    """
    Liefert den Index einer Uhrzeit innerhalb der Zeitslot-Liste.

    Parameter:
        - uhrzeit_str (str): Zeit im Format "HH:MM"
        - zeiten (list[time]): Liste gültiger Spielzeiten

    Beispiel:
        - idx = slot_index("13:00", zeiten)

    Rückgabewert:
        - int: Indexposition der Uhrzeit in der Liste

    Fehlerbehandlung:
        - ValueError, wenn Uhrzeit nicht in Liste vorhanden ist
    """

    t = datetime.strptime(uhrzeit_str, "%H:%M").time()
    return zeiten.index(t)


def baue_status_lists(schedule, teams):
    """
    Erstellt Statuslisten für alle Teams über den gesamten Zeitverlauf.

    Parameter:
        - schedule (list): Liste der Spiel-Dictionaries
        - teams (dict): team_id → Teamdaten

    Beispiel:
        - status_lists, zeiten = baue_status_lists(schedule, teams)

    Rückgabewert:
        - tuple:
            - dict: team_id → Liste von Statusbuchstaben ('S', 'P', 'F')
            - list: Liste der verwendeten Zeitpunkte

    Fehlerbehandlung:
        - Keine

    Hinweise:
        - Spiel = 'S', Pfeifen = 'P', sonst 'F' = Frei
        - Schiedsrichter werden über Teamnamen gematcht
    """

    zeiten = extrahiere_zeiten(schedule)
    status_lists = initialisiere_status_lists(teams, zeiten)

    # Umwandlung der Zeit-Strings in time format
    #def slot_index(uhrzeit_str):
     #   t = datetime.strptime(uhrzeit_str, "%H:%M").time()
     #   return zeiten.index(t)

    for match in schedule:
        # ignoriert Pausen und Einspielzeiten
        if 'Match Type' not in match:
            continue

        # setze den index für einen Timeslot
        idx = slot_index(match['Uhrzeit'], zeiten)

        # spielende Teams
        for tid, data in teams.items():
            if data['name'] in (match['Team 1'], match['Team 2']):
                status_lists[tid][idx] = 'S'

        # Schiedsrichter
        ref = match.get('Schiedsrichter')
        if ref and ref not in ('Not required', None):
            ref_tid = next(t for t, d in teams.items() if d['name'] == ref)
            status_lists[ref_tid][idx] = 'P'

    return status_lists, zeiten


def sortiere_schedule(schedule):
    """
    Sortiert den Spielplan chronologisch nach Spielbeginn ('Uhrzeit').

    Parameter:
        - schedule (list): Liste der Matches als Dictionaries mit 'Uhrzeit'

    Beispiel:
        - sortierte_liste = sortiere_schedule(schedule)

    Rückgabewert:
        - list: sortierter Spielplan

    Fehlerbehandlung:
        - ValueError bei ungültigem Zeitformat

    Hinweise:
        - Verändert die Originalreihenfolge nicht (liefert neue Liste)
    """

    return sorted(
        schedule,
        key=lambda s: datetime.strptime(s["Uhrzeit"], "%H:%M")
    )


def drucke_schedule(schedule):
    """
    Gibt den Spielplan formatiert in die Konsole aus.

    Parameter:
        - schedule (list): Liste der Spiele als Dictionaries

    Beispiel:
        - drucke_schedule(schedule)

    Rückgabewert:
        - None

    Fehlerbehandlung:
        - Keine

    Hinweise:
        - Zeigt Spielzeit, Spielnummer, Teams und Schiedsrichter an.
    """

    for m in schedule:
        print(f"{m['Uhrzeit']} – Spiel {m['Spiel']}: "
              f"{m['Team 1']} vs. {m['Team 2']} (Schiri: {m['Schiedsrichter']})")
        

# TODO Anpassung der Funktion an die Anforderungen der Schnittstelle
def aufruf_tournament(team_namen, felder, anzahl_teams, gruppen_namen, anzahl_gruppen, playstyle): 
    """
    Startet die Turniergenerierung mit gegebenen Parametern.

    Parameter:
        - team_namen (list[str]): Teamnamen
        - felder (int): Anzahl der Felder
        - anzahl_teams (int): Teams pro Gruppe
        - gruppen_namen (list[str]): Gruppenbezeichnungen
        - anzahl_gruppen (int): Anzahl Gruppen
        - playstyle (bool): True = Hin- und Rückspiel, False = nur Hinspiel

    Beispiel:
        - schedule, teams = aufruf_tournament(...)

    Rückgabewert:
        - tuple: (schedule, teams)

    Fehlerbehandlung:
        - Keine

    Hinweise:
        - Ruft intern `create_tournament_plan()` und `optimize_referees()` auf
    """

    fields = felder
    performance_groups = anzahl_gruppen
    teams_per_group = anzahl_teams
    start_time = "12:00"
    match_duration = 15
    round_trip = playstyle
    play_in_time = 30
    pause_length = 30
    pause_count = 1
    pause_interval = 2
    group_names = gruppen_namen
    team_names = team_namen

    # Spielplan erzeugen
    schedule, teams = create_tournament_plan(
        fields,
        teams_per_group,
        performance_groups,
        start_time,
        match_duration,
        round_trip,
        play_in_time,
        pause_length,
        pause_count,
        pause_interval,
        group_names,
        team_names
    )

    # Schiedsrichter optimieren
    #  schedule = optimize_referees(schedule, teams, match_duration)

    return schedule, teams

def get_statusverlaeufe(status_lists, teams):
    """
    Wandelt Statuslisten in lesbare Teamverläufe um.

    Parameter:
        - status_lists (dict): team_id → Statusliste
        - teams (dict): team_id → Teamdaten

    Beispiel:
        - verlaeufe = get_statusverlaeufe(status_lists, teams)

    Rückgabewert:
        - dict: teamname → Statusverlauf als String (z. B. "SPF")

    Fehlerbehandlung:
        - Keine
    """

    verlaeufe = {}
    for tid, statuses in status_lists.items():
        name = teams[tid]["name"]
        verlaeufe[name] = "".join(statuses)
    return verlaeufe

def analysiere_verlauf(name, verlauf, playstyle):
    """
    Analysiert Statusverlauf eines Teams und prüft auf Regelverstöße.

    Parameter:
        - name (str): Teamname
        - verlauf (str): Statusfolge des Teams
        - playstyle (bool): True = Hin- und Rückspiel, False = nur Hinspiel

    Beispiel:
        - fehler = analysiere_verlauf("STeam 1", "SFPFP", True)

    Rückgabewert:
        - list[str]: Liste erkannter Fehlertexte

    Fehlerbehandlung:
        - Keine

    Hinweise:
        - Regeln hängen vom Modus ab (z. B. keine doppelten Pausen)
    """

    fehler = []

    if playstyle == True:
        # hier werden die Spielverläufe mit dem playstyle Hin- und Rückspiel analysiert
        if "FFF" in verlauf:
            fehler.append(f"{name} – doppelte Pause")

        if "PPP" in verlauf:
            fehler.append(f"{name} – doppelte Schiedsrichter")

        if "PFP" in verlauf or "PPFFPP" in verlauf:
            fehler.append(f"{name} – ungültige Kombination pfeifen-frei-pfeifen")
    else: 
        # hier werden die Spielverläufe mit dem playstyle Hinspiel analysiert
        if "FF" in verlauf:
            fehler.append(f"{name} – doppelte Pause")
        if "PP" in verlauf:
            fehler.append(f"{name} – doppelte Schiedsrichter")
        if "PFP" in verlauf:
            fehler.append(f"{name} – ungültige Kombination pfeifen-frei-pfeifen")

    return fehler

# TODO Anpassung an die Anforderungen der Schnittstelle
def main(team_namen, felder, anzahl_teams, gruppen_namen, anzahl_gruppen, playstyle): 
    """
    Hauptfunktion zur Generierung eines möglichst fehlerfreien Spielplans.

    Parameter:
        - team_namen (list[str])
        - felder (int)
        - anzahl_teams (int)
        - gruppen_namen (list[str])
        - anzahl_gruppen (int)
        - playstyle (bool)

    Beispiel:
        - schedule, teams, fehler = main(...)

    Rückgabewert:
        - tuple: (schedule, teams, anzahl_fehler)

    Fehlerbehandlung:
        - Wiederholt Generierung maximal 30×, bis fehlerarmer Plan gefunden wurde.

    Hinweise:
        - Gibt den besten bisher gefundenen Plan zurück.
    """

    fehler_temp = 1000
    fehler = 100 
    maxtime = 30
    while fehler > 0 and maxtime > 0: 

        schedule, teams = aufruf_tournament(team_namen, felder, anzahl_teams, gruppen_namen, anzahl_gruppen, playstyle)
        
        
        #html_output = create_html(schedule, felder)
        #with open("turnierplan.html", "w", encoding="utf-8") as file:
        #   file.write(html_output)
        #print("HTML-Datei 'turnierplan.html' wurde geschrieben.")

        status_lists, zeiten = baue_status_lists(schedule, teams)

        #print("\nStatus-Listen pro Team:")
        #for tid, lst in status_lists.items():
        #    name = teams[tid]["name"]
        #    print(f"{name}: {lst}")
        
        verlaeufe = get_statusverlaeufe(status_lists, teams)
        count = 0
        for name, verlauf in verlaeufe.items():
        #    print(f"{name}: {verlauf}")
            fehler = analysiere_verlauf(name, verlauf, playstyle)
            for f in fehler:
                # print(f"Fehler: {f}") # hat debugging gründe könnte entfernt werden 
                count += 1
        if fehler_temp > count:         
            schedule_temp, fehler_temp = schedule, count
        fehler = count
        maxtime -= 1
    
    return schedule_temp, teams, fehler_temp

def show_bestplan(schedule_temp, teams, fehler): 
    """
    Zeigt den finalen Spielplan in der Konsole an.

    Parameter:
        - schedule_temp (list): Spielplan
        - teams (dict): Teaminformationen
        - fehler (int): Anzahl der Fehler im Plan

    Beispiel:
        - show_bestplan(schedule, teams, fehler)

    Rückgabewert:
        - None

    Fehlerbehandlung:
        - Keine

    Hinweise:
        - Ausgabe in menschenlesbarer Form zur Prüfung und Debugging.
    """

    print("\nErstellter Spielplan:")
    print("=" * 50)
    for match in schedule_temp:
        print(f"Spiel {match['Spiel']}:")
        print(f"  Uhrzeit: {match['Uhrzeit']}")
        print(f"  Feld: {match['Feld']}")
        print(f"  Team 1: {match['Team 1']}")
        print(f"  Team 2: {match['Team 2']}")
        print(f"  Schiedsrichter: {match['Schiedsrichter']}")
        print(f"  Gruppe: {match['Gruppe']}")
        if match['Ergebnis Team 1'] is not None and match['Ergebnis Team 2'] is not None:
            print(f"  Ergebnis: {match['Ergebnis Team 1']} : {match['Ergebnis Team 2']}")
        else:
            print(f"  Ergebnis: Noch offen")
        print("-" * 50)
    print(f"der Plan hier hatte {fehler} Fehler")

def rekonstruiere_teams(teams_per_group, group_names):
    """
    Rekonstruiert das `teams`-Dictionary basierend auf der gleichen Logik wie in `return_plan`.

    Parameter:
        - teams_per_group (list[int]): Anzahl Teams pro Gruppe
        - group_names (list[str]): Namen der Gruppen

    Rückgabe:
        - dict: team_id → Teamdaten mit 'name' und 'gruppe'
    """
    teams = {}
    team_names = []
    tid_counter = 0

    for i, num_teams in enumerate(teams_per_group):
        gruppe = group_names[i] if i < len(group_names) else f"Gruppe_{i}"
        for j in range(num_teams):
            if i == 0:
                name = f"FTeam_{j}"
            else:
                name = f"STeam_{j}"
            team_id = f"T{tid_counter}"
            teams[team_id] = {
                "name": name,
                "gruppe": gruppe
            }
            team_names.append(name)
            tid_counter += 1

    return teams


if __name__ == "__main__":
    # Beispielaufruf
    """
    anzahl_teams = 6
    felder = 4
    anzahl_gruppen = 2 
    gruppen_namen = ["Schwitzer", "Fun"]
    team_namen = ["STeam 1", "STeam 2", "STeam 3", "STeam 4", "STeam 5",
                  "FTeam 1", "FTeam 2", "FTeam 3", "FTeam 4", "FTeam 5"]
    playstyle = False # True = Hin- und Rückspiel, False = nur Hinspiel

    schedule, teams, fehler= main(team_namen, felder, anzahl_teams, gruppen_namen, anzahl_gruppen, playstyle)
    show_bestplan(schedule, teams, fehler)
    html = create_html(schedule, felder)
    # for tid, statuses in status_lists.items():
    #     name = teams[tid]["name"]
    #     # Verbinde alle Einträge mit einem Leerzeichen oder Komma
    #     verlauf = "".join(statuses)      # liefert z. B. "FSPFF"
    #     print(f"{name}: {verlauf}")
        
    #     # suche nach doppelt frei -> Wenn ja breche ab und zeige Fehler an 
    #     if "FFF" in verlauf: 
    #         print(f"Fehler in {name} – doppelte Pause")
    #         continue

    #     # such nach doppelten Schiris -> Wenn ja breche ab und zeige Fehler an 
    #     if "PPP" in verlauf: 
    #         print(f"Fehler in {name} – doppelte Schiedsrichter")
    #         continue

    #     # suche nach der Kombination pfeifen-frei-pfeifen -> if exits zeige Fehler an 
    #     if "PPFFPP" in verlauf: 
    #         print(f"Fehler in {name} – ungültige Kombination pfeifen-frei-pfeifen")
    #         continue

   # print(schedule)

   # print("\n\n\n")
    #print(teams)
"""

fields = 1
performance_groups = 1
teams_per_group = [4]
start_time = "12:00"
match_duration = 15
round_trip = True
play_in_time = 30
pause_length = [30]
pause_count = 2
pause_interval = 4
group_names = ["Fun"]
team_names = [
    "STeam 1", "STeam 2", "STeam 3", "STeam 4"]
break_times = []

teams = rekonstruiere_teams(teams_per_group, group_names)

schedule = return_plan(fields, teams_per_group, start_time, match_duration, round_trip, play_in_time, pause_length, pause_count, break_times, group_names)

status_list, zeiten = baue_status_lists(schedule, teams)

verlauf = get_statusverlaeufe(status_list, teams)


print(verlauf)

