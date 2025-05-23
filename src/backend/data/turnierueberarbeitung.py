import random
from datetime import datetime, timedelta
from turnierplangenerator_4 import (
    create_tournament_plan,
    optimize_referees,
    create_html
)

# @pytest.fixture(autouse=True)
def fixed_random_seed():
    random.seed(42)


def extrahiere_zeiten(schedule):
    """
    Ermittelt alle eindeutigen Spielzeiten (als datetime-Objekte) aus dem Zeitplan.
    Nur Spiele mit Schlüssel 'Match Type' werden berücksichtigt.
    """
    zeiten = {
        datetime.strptime(m["Uhrzeit"], "%H:%M").time()
        for m in schedule
        if "Match Type" in m
    }
    return sorted(zeiten)

def initialisiere_status_lists(teams, zeiten):
    """
    Erstellt ein Dict team_id → Liste von 'F'-Einträgen für alle Zeitslots.
    """
    return {tid: ['F'] * len(zeiten) for tid in teams}

def slot_index(uhrzeit_str, zeiten):
    """
    Gibt den Index eines Uhrzeit-Strings (z. B. "13:00") in der Zeitslot-Liste zurück.
    """
    t = datetime.strptime(uhrzeit_str, "%H:%M").time()
    return zeiten.index(t)


def baue_status_lists(schedule, teams):
    """
    Erzeugt für jede Mannschaft eine Liste von Zuständen über alle Zeit-Slots:
      - 'S' = spielt selbst
      - 'P' = pfeift als Schiedsrichter
      - 'F' = frei
    Gibt ein dict team_id → Liste der Zustände sowie die Liste der Zeit-Slots zurück.
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
    Sortiert die schedule-Liste nach dem Zeit-String 'Uhrzeit' aufsteigend
    und gibt die neue, sortierte Liste zurück.
    """
    return sorted(
        schedule,
        key=lambda s: datetime.strptime(s["Uhrzeit"], "%H:%M")
    )


def drucke_schedule(schedule):
    """
    Druckt den Spielplan formatiert in die Konsole.
    """
    for m in schedule:
        print(f"{m['Uhrzeit']} – Spiel {m['Spiel']}: "
              f"{m['Team 1']} vs. {m['Team 2']} (Schiri: {m['Schiedsrichter']})")

def aufruf_tournament(team_namen, felder, anzahl_teams, gruppen_namen, anzahl_gruppen, playstyle): 
    # Parameterdefinition
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
        fields=fields,
        teams_per_group=teams_per_group,
        performance_groups=performance_groups,
        start_time=start_time,
        match_duration=match_duration,
        round_trip=round_trip,
        play_in_time=play_in_time,
        pause_length=pause_length,
        pause_count=pause_count,
        pause_interval=pause_interval,
        group_names=group_names,
        team_names=team_names
    )

    # Schiedsrichter optimieren
    schedule = optimize_referees(schedule, teams, match_duration)

    return schedule, teams

def get_statusverlaeufe(status_lists, teams):
    """
    Gibt ein Dict zurück: Teamname → Statusverlauf als String, z. B. {"STeam 1": "SFPFS"}
    """
    verlaeufe = {}
    for tid, statuses in status_lists.items():
        name = teams[tid]["name"]
        verlaeufe[name] = "".join(statuses)
    return verlaeufe

def analysiere_verlauf(name, verlauf, playstyle):
    """
    Prüft den Spielverlauf eines Teams auf Regelverstöße.

    Gibt eine Liste von Fehlern (Strings) zurück.
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

def main(team_namen, felder, anzahl_teams, gruppen_namen, anzahl_gruppen, playstyle): 
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
    Gibt den besten Spielplan und die Teams aus.
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

if __name__ == "__main__":
    # Beispielaufruf
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

