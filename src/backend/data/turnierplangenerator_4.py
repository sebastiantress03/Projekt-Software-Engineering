from datetime import datetime, timedelta
from collections import defaultdict
from data.apiClasses.apiClasses import *
import random
import copy


def calculate_waiting_time(current_time, team_last_played_time):
    """
    Berechnet die Wartezeit eines Teams seit seinem letzten Spiel in Sekunden.

    Parameter:
        - current_time (datetime): Der aktuelle Zeitpunkt.
        - team_last_played_time (datetime): Der Zeitpunkt, an dem das Team zuletzt gespielt hat.

    Rückgabewert:
        - float: Anzahl der Sekunden seit dem letzten Spiel.

    Fehlerbehandlung:
        - Keine spezielle Fehlerbehandlung implementiert.

    Hinweise:
        - Beide Parameter müssen datetime-Objekte sein.
    """
    return (current_time - team_last_played_time).total_seconds()


def assign_fields_to_groups(fields, group_names):
    """
    Weist Spielfelder den angegebenen Gruppen möglichst gleichmäßig zu.

    Parameter:
        - fields (int): Die Gesamtanzahl an Spielfeldern.
        - group_names (list): Eine Liste mit den Namen der Gruppen (str), z.B. ["Gruppe A", "Gruppe B"].

    Rückgabewert:
        - dict: Ein Dictionary, das jeder Gruppe eine Liste ihrer zugewiesenen Felder zuordnet.

    Beispiel:
        - assign_fields_to_groups(4, ["A", "B"]) ergibt z.B. {"A": [1, 3, 4], "B": [2, 3, 4]}

    Fehlerbehandlung:
        - Keine direkte Fehlerbehandlung implementiert.

    Hinweise:
        - Zusätzliche (nicht exakt aufteilbare) Felder werden mit allen Gruppen geteilt.
    """

    field_assignment = {group: [] for group in group_names}
    total_groups = len(group_names)

    base_fields_per_group = fields // total_groups
    remaining_fields = fields % total_groups

    field_counter = 1
    for group in group_names:
        for _ in range(base_fields_per_group):
            field_assignment[group].append(field_counter)
            field_counter += 1

    shared_fields = list(range(field_counter, fields + 1))
    for group in group_names:
        field_assignment[group].extend(shared_fields)

    return field_assignment




consecutive_invalid_rounds = 0
MAX_INVALID_ATTEMPTS = 10

def create_tournament_plan(
    fields, teams_per_group, performance_groups, start_time, match_duration,
    round_trip, play_in_time, pause_length, pause_interval, pause_count,
    group_names=None, team_names=None
):
    """
    Erstellt einen Turnierplan mit Spielfeldern, Gruppen, Teams und Spielpaarungen inkl. Einspielzeit.

    Parameter:
        - fields (int): Anzahl der verfügbaren Spielfelder.
        - teams_per_group (int): Anzahl der Teams pro Leistungsgruppe.
        - performance_groups (int): Anzahl der Leistungsgruppen.
        - start_time (str): Startzeit des Turniers im Format "%H:%M".
        - match_duration (int): Spieldauer in Minuten.
        - round_trip (bool): Ob Hin- und Rückspiele geplant werden sollen.
        - play_in_time (int): Dauer der Einspielzeit vor dem ersten Spiel in Minuten.
        - pause_length (int): Dauer einer Pause in Minuten.
        - pause_interval (int): Intervall zwischen Pausen in Stunden.
        - pause_count (int): Anzahl der geplanten Pausen.
        - group_names (list, optional): Namen der Leistungsgruppen.
        - team_names (list, optional): Namen der Teams.

    Rückgabewert:
        - tuple:
            - schedule (list): Liste der geplanten Spiele mit Uhrzeit, Feld, Teams, etc.
            - teams (dict): Dictionary der Teams mit Namen und Gruppenzugehörigkeit.
            - field_assignment (dict): Zuordnung der Felder zu den Gruppen.

    Fehlerbehandlung:
        - ValueError, wenn die Anzahl der angegebenen Team- oder Gruppennamen nicht zu den berechneten Werten passt.

    Hinweise:
        - Die erste Aktion im Zeitplan ist eine Einspielphase für alle Teams.
        - Matches werden gruppenintern als Hin- und ggf. Rückspiel angelegt.
    """
    total_teams = teams_per_group * performance_groups
    if not team_names:
        team_names = [f"Team {i + 1}" for i in range(total_teams)]
    elif len(team_names) != total_teams:
        raise ValueError("Anzahl der Teamnamen muss mit der Anzahl an Teams übereinstimmen")

    if not group_names:
        group_names = [f"Group {i + 1}" for i in range(performance_groups)]
    elif len(group_names) != performance_groups:
        raise ValueError("Anzahl der Namen der Leistungsgruppen muss mit der Anzahl der Leistungsgruppen übereinstimmen.")
    
    field_assignment = assign_fields_to_groups(fields, group_names)



    teams = {}
    for group_index in range(performance_groups):
        group_teams = team_names[group_index * teams_per_group:(group_index + 1) * teams_per_group]
        for team_index, team_name in enumerate(group_teams):
            teams[f"team_{group_index * teams_per_group + team_index + 1}"] = {
                "name": team_name,
                "group": group_names[group_index]
            }


    team_status = {
        team_id: {
            "plays": 0,
            "ref_count": 0,
            "inactivity_streak": 0,
            "last_active": True  # spielt oder pfeift
        } for team_id in teams
    }



    matches = []
    for group_index in range(performance_groups):
        group_teams = [team_id for team_id, team_data in teams.items()
                       if team_data["group"] == group_names[group_index]]
        for i in range(len(group_teams)):
            for j in range(i + 1, len(group_teams)):
                # Hinspiel
                matches.append((group_teams[i], group_teams[j], group_names[group_index], "Hinspiel"))
                if round_trip:
                    matches.append((group_teams[j], group_teams[i], group_names[group_index], "Rückspiel"))


    schedule = []
    current_time = datetime.strptime(start_time, "%H:%M")
    schedule.append({
        "Spiel": 0,
        "Feld": "All Fields",
        "Uhrzeit": current_time.strftime("%H:%M"),
        "Team 1": "Warm-up",
        "Team 2": "Warm-up",
        "Schiedsrichter": "Not required",
        "Gruppe": "N/A",
        "Ergebnis Team 1": None,
        "Ergebnis Team 2": None,
    })
    current_time += timedelta(minutes=play_in_time)

    remaining_matches = matches.copy()
    round_number = 0
    pauses_planned = 0
    next_pause_time = current_time + timedelta(hours=pause_interval)

    def filter_least_played_matches(remaining_matches, team_status):
        """
        Filtert die verbleibenden Spiele und gibt die mit der geringsten Anzahl an bisherigen Spieleinsätzen der beteiligten Teams zurück.

        Parameter:
            - remaining_matches (list): Liste von Tuple-Spielen (team1, team2, group, match_type).
            - team_status (dict): Dictionary mit Infos über Anzahl der bisherigen Spiele pro Team.

        Rückgabewert:
            - list: Liste der Spiele mit den wenigsten bisherigen Einsätzen der beteiligten Teams.

        Fehlerbehandlung:
            - Gibt eine leere Liste zurück, wenn keine Matches vorhanden sind.

        Hinweise:
            - Dient der gleichmäßigen Verteilung der Spiele auf die Teams.
        """

        match_play_counts = []
        for match in remaining_matches:
            team1, team2, group, match_type = match
            team1_plays = team_status[team1]["plays"]
            team2_plays = team_status[team2]["plays"]
            total_plays = team1_plays + team2_plays
            match_play_counts.append((match, total_plays))

        if not match_play_counts:
            return [] 


        min_plays = min(play_count for _, play_count in match_play_counts)

        least_played_matches = [
            match for match, play_count in match_play_counts if play_count == min_plays
        ]

        return least_played_matches


    last_referees = set()

    exclusive_fields = {}
    for field in range(1, fields + 1):
        owners = [g for g, fs in field_assignment.items() if field in fs]
        if len(owners) == 1:
            exclusive_fields[field] = owners[0]

    while remaining_matches:
        """
        Der zentrale Block innerhalb `create_tournament_plan`, der die Matches auf Spielfelder und Zeitfenster verteilt.

        Fehlerbehandlung:
            - Bricht die Schleife ab, wenn keine gültigen Spiele mehr geplant werden können.
            - Pausen werden automatisch eingeplant, wenn die Zeit erreicht ist.

        Hinweise:
            - Bevorzugt Spielfelder, die einer Gruppe exklusiv zugewiesen sind.
            - Ein Rückspiel wird direkt nach dem Hinspiel eingeplant, wenn `round_trip` aktiv ist.
            - Plant „Einspielzeit“ und „Pause“-Blöcke separat ein.
        """
        round_matches = []
        playing_teams = set()
        assigned_referees = set()
        available_fields = set(range(1, fields + 1))


        if pauses_planned < pause_count and current_time >= next_pause_time:
            schedule.append({
                "Spiel": len(schedule) + 1,
                "Feld": "All Fields",
                "Uhrzeit": current_time.strftime("%H:%M"),
                "Team 1": "Pause",
                "Team 2": "Pause",
                "Schiedsrichter": "Not required",
                "Gruppe": "N/A",
                "Ergebnis Team 1": None,
                "Ergebnis Team 2": None,
            })
            current_time += timedelta(minutes=pause_length)
            next_pause_time += timedelta(hours=pause_interval)
            pauses_planned += 1
            continue

        for group in group_names:
            group_matches = [
                m for m in filter_least_played_matches(remaining_matches, team_status)
                if m[2] == group
            ]
            preferred_fields = field_assignment[group]

            for field in preferred_fields:
                if field not in available_fields:
                    continue

                for match in group_matches:
                    team1, team2, group_name, match_type = match
                    if team1 in playing_teams or team2 in playing_teams:
                        continue

                    ref_candidates = [
                        tid for tid in teams
                        if tid not in playing_teams and tid not in [team1, team2] and teams[tid]["group"] == group_name
                    ]
                    ref_id = ref_candidates[0] if ref_candidates else None
                    ref_name = teams[ref_id]["name"] if ref_id else "KEIN SCHIRI"

                    round_matches.append({
                        "Spiel": len(schedule) + len(round_matches) + 1,
                        "Feld": f"Field {field}",
                        "Uhrzeit": current_time.strftime("%H:%M"),
                        "Team 1": teams[team1]["name"],
                        "Team 2": teams[team2]["name"],
                        "Schiedsrichter": ref_name,
                        "Gruppe": group_name,
                        "Ergebnis Team 1": None,
                        "Ergebnis Team 2": None,
                        "Match Type": match_type,
                    })
                    playing_teams.update([team1, team2])
                    team_status[team1]["plays"] += 1
                    team_status[team2]["plays"] += 1
                    available_fields.remove(field)
                    remaining_matches.remove(match)
                    if ref_id:
                        playing_teams.add(ref_id)
                        team_status[ref_id]["ref_count"] += 1


                    if match_type == "Hinspiel" and round_trip:
                        reverse_match = (team2, team1, group_name, "Rückspiel")
                        if reverse_match in remaining_matches:
                            round_matches.append({
                                "Spiel": len(schedule) + len(round_matches) + 1,
                                "Feld": f"Field {field}",
                                "Uhrzeit": (current_time + timedelta(minutes=match_duration)).strftime("%H:%M"),
                                "Team 1": teams[team2]["name"],
                                "Team 2": teams[team1]["name"],
                                "Schiedsrichter": ref_name,
                                "Gruppe": group_name,
                                "Ergebnis Team 1": None,
                                "Ergebnis Team 2": None,
                                "Match Type": "Rückspiel",
                            })
                            playing_teams.update([team2, team1])
                            team_status[team2]["plays"] += 1
                            team_status[team1]["plays"] += 1
                            remaining_matches.remove(reverse_match)
                            if ref_id:
                                playing_teams.add(ref_id)
                                team_status[ref_id]["ref_count"] += 1
                    break  


        for field in list(available_fields):
            for match in filter_least_played_matches(remaining_matches, team_status):
                team1, team2, group_name, match_type = match
                

                if field not in field_assignment[group_name]:
                    continue
                team1, team2, group_name, match_type = match
                if team1 in playing_teams or team2 in playing_teams:
                    continue
                
                ref_candidates = [
                    tid for tid in teams
                    if tid not in playing_teams and tid not in [team1, team2] and teams[tid]["group"] == group_name
                ]
                ref_id = ref_candidates[0] if ref_candidates else None
                ref_name = teams[ref_id]["name"] if ref_id else "KEIN SCHIRI"

                round_matches.append({
                    "Spiel": len(schedule) + len(round_matches) + 1,
                    "Feld": f"Field {field}",
                    "Uhrzeit": current_time.strftime("%H:%M"),
                    "Team 1": teams[team1]["name"],
                    "Team 2": teams[team2]["name"],
                    "Schiedsrichter": ref_name,
                    "Gruppe": group_name,
                    "Ergebnis Team 1": None,
                    "Ergebnis Team 2": None,
                    "Match Type": match_type,
                })
                playing_teams.update([team1, team2])
                team_status[team1]["plays"] += 1
                team_status[team2]["plays"] += 1
                if ref_id:
                    playing_teams.add(ref_id)
                    team_status[ref_id]["ref_count"] += 1
                remaining_matches.remove(match)
                available_fields.remove(field)
                if match_type == "Hinspiel" and round_trip:
                    reverse_match = (team2, team1, group_name, "Rückspiel")
                    if reverse_match in remaining_matches:
                        round_matches.append({
                            "Spiel": len(schedule) + len(round_matches) + 1,
                            "Feld": f"Field {field}",
                            "Uhrzeit": (current_time + timedelta(minutes=match_duration)).strftime("%H:%M"),
                            "Team 1": teams[team2]["name"],
                            "Team 2": teams[team1]["name"],
                            "Schiedsrichter": ref_name,
                            "Gruppe": group_name,
                            "Ergebnis Team 1": None,
                            "Ergebnis Team 2": None,
                            "Match Type": "Rückspiel",
                        })
                        playing_teams.update([team2, team1])
                        team_status[team2]["plays"] += 1
                        team_status[team1]["plays"] += 1
                        remaining_matches.remove(reverse_match)
                        if ref_id:
                            playing_teams.add(ref_id)
                            team_status[ref_id]["ref_count"] += 1
                break


        if round_matches:
            time_increment = timedelta(minutes=match_duration * 2 if round_trip else match_duration)
            schedule.extend(round_matches)
            round_number += 1

            round_invalid = False
            for team_id in teams:
                if team_id in playing_teams:
                    team_status[team_id]["inactivity_streak"] = 0
                    team_status[team_id]["last_active"] = True
                else:
                    team_status[team_id]["inactivity_streak"] += 1
                    team_status[team_id]["last_active"] = False

                    if team_status[team_id]["inactivity_streak"] >= 2:
                        round_invalid = True
                        break

            if round_invalid:
                consecutive_invalid_rounds += 1
                if consecutive_invalid_rounds < MAX_INVALID_ATTEMPTS:
                    for m in round_matches:
                        schedule.remove(m)

                        team1_id = next(k for k, v in teams.items() if v["name"] == m["Team 1"])
                        team2_id = next(k for k, v in teams.items() if v["name"] == m["Team 2"])
                        match_type = m["Match Type"]
                        group = m["Gruppe"]

                        remaining_matches.append((team1_id, team2_id, group, match_type))

                        team_status[team1_id]["plays"] -= 1
                        team_status[team2_id]["plays"] -= 1

                        if m["Schiedsrichter"] != "KEIN SCHIRI":
                            ref_id = next(k for k, v in teams.items() if v["name"] == m["Schiedsrichter"])
                            team_status[ref_id]["ref_count"] -= 1

                    continue  
                else:
                    current_time += time_increment
                    consecutive_invalid_rounds = 0  
            else:
                current_time += time_increment
                consecutive_invalid_rounds = 0  

        else:
            break


        for team_id in teams:
            if team_id not in playing_teams:
                team_status[team_id]["consecutive_plays"] = 0

    return schedule, teams, field_assignment


def optimize_schedule(schedule, teams, match_duration, fields, field_assignment):
    """
    Optimiert den Spielplan hinsichtlich Fairness, Gleichverteilung und Vermeidung von Schiedsrichterkonflikten.

    Parameter:
        - schedule (list): Der bestehende Spielplan.
        - teams (dict): Dictionary mit Teamdaten (Name, Gruppe).
        - match_duration (int): Dauer eines Spiels in Minuten.
        - fields (int): Anzahl der verfügbaren Spielfelder.
        - field_assignment (dict): Feld-Zuweisung pro Gruppe.

    Rückgabewert:
        - list: Optimierter Spielplan, sortiert nach Zeit und Feld.

    Fehlerbehandlung:
        - Keine direkte Exception-Behandlung, aber Fallback auf besten bekannten Spielplan bei schlechter Optimierung.

    Hinweise:
        - Bewertet Pläne mit einer Kostenfunktion (`cost()`), u.a. für Leerlaufzeiten, Schiri-Konflikte, ungenutzte Felder.
        - Optimierung durch Tauschen von Spielpaaren (Hin-/Rückspiel).
    """   

    time_format = "%H:%M"
    rng = random.Random(42)

    def time_obj(t):
        """
        Konvertiert einen Zeit-String in ein datetime-Objekt.

        Parameter:
            - t (str): Zeitangabe im Format "%H:%M".

        Rückgabewert:
            - datetime: Zeit als datetime-Objekt.

        Fehlerbehandlung:
            - Kein spezielles Handling – Fehler bei falschem Format.
        """        
        return datetime.strptime(t, time_format)

    def build_match_pairs(matches):
        """
        Sucht passende Hin- und Rückspiel-Paare im Spielplan.

        Parameter:
            - matches (list): Liste der Spiel-Dictionaries.

        Rückgabewert:
            - list: Liste von Tupeln mit je einem Hin- und Rückspiel.

        Hinweise:
            - Nur Matches mit "Hinspiel" werden betrachtet.
            - Paarung erfolgt nach Teamnamen und Gruppenabgleich.
        """
        pairs, used = [], set()
        for i, m1 in enumerate(matches):
            if i in used or m1.get("Match Type") != "Hinspiel":
                continue
            for j, m2 in enumerate(matches):
                if j in used or j == i:
                    continue
                if (m2.get("Match Type") == "Rückspiel"
                    and m1["Team 1"] == m2["Team 2"]
                    and m1["Team 2"] == m2["Team 1"]
                    and m1["Gruppe"] == m2["Gruppe"]):
                    pairs.append((m1, m2))
                    used.update([i, j])
                    break
        return pairs

    def cost(schedule):
        """
        Bewertet den Spielplan nach Fairness, Feldnutzung und Schiri-Verteilung.

        Parameter:
            - schedule (list): Liste der Spiel-Dictionaries.

        Rückgabewert:
            - int: Kostenwert – je niedriger, desto besser.

        Bewertungsfaktoren:
            - Ungenutzte Felder (Leerlaufzeiten)
            - Enge Schiedsrichter-Zeitabstände
            - Ungleichmäßige Feldauslastung
            - Inaktivitätsphasen für Teams

        Hinweise:
            - Berücksichtigt auch den Fall "KEIN SCHIRI" mit Strafkosten.
        """
    
        field_usage = defaultdict(int)
        time_field = defaultdict(set)
        referee_timeline = defaultdict(list)
        penalty = 0

        time_slots = sorted(set(datetime.strptime(m["Uhrzeit"], time_format) for m in schedule if "Match Type" in m))
        time_strs = [t.strftime(time_format) for t in time_slots]
        team_timelines = {t["name"]: ['-'] * len(time_slots) for t in teams.values()}

        for m in schedule:
            if "Match Type" not in m:
                continue
            t = m["Uhrzeit"]
            f = m["Feld"]
            time_field[t].add(f)
            field_idx = int(f.split()[-1]) - 1
            field_usage[field_idx] += 1

            for team in [m["Team 1"], m["Team 2"]]:
                if team in team_timelines:
                    idx = time_strs.index(t)
                    team_timelines[team][idx] = 'P'

            ref = m.get("Schiedsrichter")
            if ref:
                referee_timeline[ref].append(t)
                if ref in team_timelines:
                    idx = time_strs.index(t)
                    if team_timelines[ref][idx] == '-':
                        team_timelines[ref][idx] = 'R'

            if ref == "KEIN SCHIRI":
                penalty += 500

        empty_fields = sum(fields - len(time_field[t]) for t in time_field)

        for ref, times in referee_timeline.items():
            times_sorted = sorted(datetime.strptime(t, time_format) for t in times)
            for i in range(len(times_sorted) - 1):
                delta = (times_sorted[i+1] - times_sorted[i]).total_seconds() / 60
                if delta == match_duration:
                    penalty += 10000 
                elif delta == match_duration * 2:
                    penalty += 500  

        variance_penalty = 0
        if field_usage:
            avg = sum(field_usage.values()) / fields
            variance_penalty = sum(abs(field_usage[i] - avg) for i in field_usage)

        INACTIVITY_WEIGHT = 10000

        inactivity_penalty = 0
        for team, timeline in team_timelines.items():
            for i in range(1, len(timeline)):
                if timeline[i - 1] == '-' and timeline[i] == '-':
                    inactivity_penalty += 1_000_000  


            gap_length = 0
            for status in timeline:
                if status == '-':
                    gap_length += 1
                else:
                    if gap_length > 0:
                        inactivity_penalty += (gap_length ** 2) * INACTIVITY_WEIGHT
                        gap_length = 0
            if gap_length > 0:
                inactivity_penalty += (gap_length ** 2) * INACTIVITY_WEIGHT




        return (
            empty_fields * 200
            + penalty
            + variance_penalty * 5
            + inactivity_penalty * 25
        )

    def assign_referees_strict(schedule, teams, match_duration):
        """
        Weist Schiedsrichter so zu, dass Gruppenlogik eingehalten und Belastung verteilt wird.

        Parameter:
            - schedule (list): Spielplan mit Hin- und Rückspielen.
            - teams (dict): Dictionary mit Teamdaten (inkl. Gruppenzugehörigkeit).
            - match_duration (int): Dauer eines Spiels in Minuten.

        Hinweise:
            - Schiedsrichter dürfen nicht direkt davor oder danach gespielt haben.
            - Schiedsrichter kommen aus derselben Gruppe wie das Match.
            - Falls kein Schiedsrichter verfügbar, wird "KEIN SCHIRI" eingetragen.
        """
        from collections import defaultdict
        from datetime import datetime, timedelta

        time_format = "%H:%M"
        referee_timeline = defaultdict(list)
        time_team_map = defaultdict(set)
        time_ref_map = defaultdict(set)
        team_use_count = {t['name']: {'P': 0, 'R': 0} for t in teams.values()}


        schedule_by_time_field = {
            (m['Uhrzeit'], m['Feld']): m for m in schedule if m.get('Match Type') in ["Hinspiel", "Rückspiel"]
        }


        for m in schedule:
            if "Match Type" not in m:
                continue
            time_team_map[m["Uhrzeit"]].update([m["Team 1"], m["Team 2"]])

        for m in schedule:
            if m.get("Match Type") != "Hinspiel":
                continue

            t1 = datetime.strptime(m["Uhrzeit"], time_format)
            t2_dt = t1 + timedelta(minutes=match_duration)
            t2_str = t2_dt.strftime(time_format)
            field = m["Feld"]

            # Rückspiel suchen
            m2 = schedule_by_time_field.get((t2_str, field))
            if not m2 or m2.get("Match Type") != "Rückspiel":
                continue
            if not (m2["Team 1"] == m["Team 2"] and m2["Team 2"] == m["Team 1"]):
                continue

            group = m["Gruppe"]
            all_teams = {m["Team 1"], m["Team 2"], m2["Team 1"], m2["Team 2"]}
            t1_str = m["Uhrzeit"]


            forbidden = time_team_map[t1_str] | time_team_map[t2_str] | time_ref_map[t1_str] | time_ref_map[t2_str] | all_teams

  
            def recent_ref_penalty(candidate_name):
                times = referee_timeline[candidate_name]
                penalty = 0
                for past_str in times:
                    past_dt = datetime.strptime(past_str, time_format)
                    diff = abs((t1 - past_dt).total_seconds()) / 60
                    if diff == match_duration:
                        penalty += 10000
                    elif diff == 2 * match_duration:
                        penalty += 500
                return penalty


            candidates = [
                t for t in teams.values()
                if t["group"] == group and t["name"] not in forbidden
            ]


            candidates.sort(
                key=lambda c: (
                    recent_ref_penalty(c["name"]),
                    team_use_count[c["name"]]["R"],
                    team_use_count[c["name"]]["P"]
                )
            )

            if candidates:
                ref = candidates[0]["name"]
                m["Schiedsrichter"] = ref
                m2["Schiedsrichter"] = ref
                referee_timeline[ref].extend([t1_str, t2_str])
                time_ref_map[t1_str].add(ref)
                time_ref_map[t2_str].add(ref)
                team_use_count[ref]["R"] += 2
                for team in all_teams:
                    team_use_count[team]["P"] += 1
            else:
                m["Schiedsrichter"] = "KEIN SCHIRI"
                m2["Schiedsrichter"] = "KEIN SCHIRI"



    matches = [m for m in schedule if "Match Type" in m]
    best_schedule = copy.deepcopy(matches)
    assign_referees_strict(best_schedule, teams, match_duration)
    best_cost = cost(best_schedule)

    for _ in range(40):
        pairs = build_match_pairs(matches)
        rng.shuffle(pairs)

        for m1, m2 in pairs:
            old_t = time_obj(m1["Uhrzeit"])
            old_f = int(m1["Feld"].split()[-1]) - 1

            candidate_slots = sorted(set(time_obj(m["Uhrzeit"]) for m in matches))
            rng.shuffle(candidate_slots)

            for t in candidate_slots:
                t2 = t + timedelta(minutes=match_duration)
                group = m1["Gruppe"]
                allowed_fields = [f for f in field_assignment[group]]
                rng.shuffle(allowed_fields)
                for f in allowed_fields:
                    f_str = f"Field {f}"
                    occupied = any(
                        (m["Uhrzeit"] == t.strftime(time_format) or m["Uhrzeit"] == t2.strftime(time_format))
                        and m["Feld"] == f_str for m in matches)
                    if not occupied:
                        m1["Uhrzeit"], m1["Feld"] = t.strftime(time_format), f_str
                        m2["Uhrzeit"], m2["Feld"] = t2.strftime(time_format), f_str

                        assign_referees_strict(schedule, teams, match_duration)

                        new_cost = cost(matches)
                        if new_cost < best_cost:
                            best_cost = new_cost
                            best_schedule = copy.deepcopy(matches)
                        else:
                            m1["Uhrzeit"], m1["Feld"] = old_t.strftime(time_format), f"Field {old_f+1}"
                            m2["Uhrzeit"], m2["Feld"] = (old_t + timedelta(minutes=match_duration)).strftime(time_format), f"Field {old_f+1}"
                        break
                else:
                    continue
                break

    return sorted(best_schedule, key=lambda m: (time_obj(m["Uhrzeit"]), m["Feld"]))


def insert_pauses(schedule, start_time, play_in_time, pause_interval, pause_length, pause_count):
    """
    Fügt feste Pausen zu definierten Zeiten in den Spielplan ein.

    Parameter:
        - schedule (list): Der Spielplan, in den Pausen eingefügt werden.
        - start_time (str): Startzeit des Turniers (Format "%H:%M").
        - play_in_time (int): Dauer der Einspielzeit in Minuten.
        - pause_interval (int): Stunden bis zur nächsten Pause.
        - pause_length (int): Dauer einer Pause in Minuten.
        - pause_count (int): Anzahl der Pausen.

    Rückgabewert:
        - list: Neuer Spielplan mit eingefügten Pausen.

    Fehlerbehandlung:
        - Überspringt doppelte Pausenzeiten.

    Hinweise:
        - Pausen werden vor dem ersten Spiel nach Erreichen der definierten Zeit eingefügt.
    """
    from datetime import datetime, timedelta

    time_format = "%H:%M"
    start_dt = datetime.strptime(start_time, time_format) + timedelta(minutes=play_in_time)
    pause_times = [start_dt + timedelta(hours=pause_interval * i) for i in range(1, pause_count + 1)]

    pause_times_str = [pt.strftime(time_format) for pt in pause_times]


    updated_schedule = []
    pause_inserted = set()
    for match in schedule:
 
        while pause_times_str and match["Uhrzeit"] >= pause_times_str[0] and pause_times_str[0] not in pause_inserted:
            updated_schedule.append({
                "Spiel": len(updated_schedule) + 1,
                "Feld": "All Fields",
                "Uhrzeit": pause_times_str[0],
                "Team 1": "Pause",
                "Team 2": "Pause",
                "Schiedsrichter": "Not required",
                "Gruppe": "N/A",
                "Ergebnis Team 1": None,
                "Ergebnis Team 2": None,
            })
            pause_inserted.add(pause_times_str[0])
            pause_times_str.pop(0)
        updated_schedule.append(match)

    # Falls Pausezeiten am Ende liegen und noch nicht eingefügt wurden
    for remaining_pause in pause_times_str:
        updated_schedule.append({
            "Spiel": len(updated_schedule) + 1,
            "Feld": "All Fields",
            "Uhrzeit": remaining_pause,
            "Team 1": "Pause",
            "Team 2": "Pause",
            "Schiedsrichter": "Not required",
            "Gruppe": "N/A",
            "Ergebnis Team 1": None,
            "Ergebnis Team 2": None,
        })

    return updated_schedule




if __name__ == '__main__':
    fields = 2
    performance_groups = 2
    teams_per_group = 6
    start_time = "12:00"
    match_duration = 15
    round_trip = True
    play_in_time = 30
    pause_length = 30
    pause_count = 2
    pause_interval = 4
    group_names = ["Schwitzer", "Fun"]
    team_names = [
        "STeam 1", "STeam 2", "STeam 3", "STeam 4", "STeam 5", "STeam 6",
        "FTeam1", "FTeam2", "FTeam 3", "FTeam 4", "FTeam 5", "FTeam 6"
        
    ]

    schedule, teams, field_assignment = create_tournament_plan(
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
    schedule = optimize_schedule(schedule, teams, match_duration, fields, field_assignment)

    schedule = insert_pauses(
        schedule=schedule,
        start_time=start_time,
        play_in_time=play_in_time,
        pause_interval=pause_interval,
        pause_length=pause_length,
        pause_count=pause_count
    )







    if not schedule:


        print("Es konnten keine Spiele geplant werden.")
    else:
        print("\nErstellter Spielplan:")
        print("=" * 50)
        for match in schedule:
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


def return_plan(fields: int, teams_per_group: List[int], start_time:str, match_duration:int, round_trip:str, play_in_time:int, pause_length:List[int], pause_count:int, break_times:List[str], group_names:List):
    """
    Generiert einen Spielplan für ein Turnier auf Basis der gegebenen Parameter.

    Parameter:
        - fields (int): Anzahl der verfügbaren Spielfelder.
        - teams_per_group (List[int]): Liste mit der Anzahl an Teams pro Gruppe.
        - start_time (str): Startzeit des Turniers im Format "HH:MM".
        - match_duration (int): Dauer eines Spiels in Minuten.
        - round_trip (str): Gibt an, ob Hin- und Rückrunde gespielt wird.
        - play_in_time (int): Zeit in Minuten für das Einspielen vor dem Spiel.
        - pause_length (List[int]): Liste mit Pausenlängen.
        - pause_count (int): Anzahl der Pausen, die während des Turniers gemacht werden sollen.
        - break_times (List[str]): Liste geplanter Pausenzeiten im Format "HH:MM".
        - group_names (List): Namen der Gruppen.

    Rückgabe:
        - schedule (List[dict]): Spielplan bestehend aus Spielen mit folgenden Schlüsseln:
            - 'Spiel' (int): Spielnummer.
            - 'Feld' (str): Bezeichnung des Spielfelds.
            - 'Uhrzeit' (str): Startzeit des Spiels.
            - 'Team 1' (str): Name des ersten Teams.
            - 'Team 2' (str): Name des zweiten Teams.
            - 'Schiedsrichter' (str): Name des Schiedsrichter-Teams.
            - 'Gruppe' (str): Gruppenname.
            - 'Ergebnis Team 1' (Optional[int]): Spielergebnis Team 1 (initial `None`).
            - 'Ergebnis Team 2' (Optional[int]): Spielergebnis Team 2 (initial `None`).
            - 'Match Type' (str): Typ des Spiels ("Hinspiel" oder "Rückspiel").

    Hinweise:
        - Die tatsächliche Planung erfolgt durch `create_tournament_plan(...)` und wird anschließend durch
          `optimize_schedule(...)` optimiert.
        - Die Teamnamen werden automatisch generiert ("FTeam_0", "STeam_1").
    """


    pause_interval = 2
    team_names = []
    
    for i, num_teams in enumerate(teams_per_group):
        for j in range(num_teams):
            if i == 0:
                team_names.append(f"FTeam_{j}")
            else:
                team_names.append(f"STeam_{j}")


    if(len(group_names) == 2): 
        numberOfTeams = len(team_names)//2
    else: 
        numberOfTeams = len(team_names)

    # Debug
    print(f"fields: {fields}, numberOfTeams: {numberOfTeams}, len(group_names): {len(group_names)}, start_time: {start_time}, match_duration: {match_duration},  round_trip: {round_trip}, play_in_time: {play_in_time}, pause_length: {pause_length}, pause_count: {pause_count},  pause_interval: {pause_interval}, group_names: {group_names}, team_names:{team_names}")
    # pause_length ist eine Liste und muss eigentlich auch als liste entgegen genommen werden
    schedule, teams, field_assignment = create_tournament_plan(fields, numberOfTeams, len(group_names), start_time, match_duration, round_trip, play_in_time, 0 if len(pause_length) == 0 else pause_length[0], pause_count, pause_interval, group_names, team_names)

    schedule = optimize_schedule(schedule, teams, match_duration, fields, field_assignment)

    return schedule



def create_html(schedule, fields):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Turnierplan</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px auto;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }
            th {
                background-color: #f4f4f4;
            }
            .time-column {
                width: 10%;
                font-weight: bold;
                background-color: #e8e8e8;
            }
        </style>
    </head>
    <body>
        <h1>Turnierplan</h1>
        <table>
            <thead>
                <tr>
                    <th class="time-column">Uhrzeit</th>
    """

    for field in range(1, fields + 1):
        html += f"<th>Feld {field}</th><th>Schiri Feld {field}</th>"
    html += "</tr></thead><tbody>"

    grouped_schedule = {}
    for match in schedule:
        time = match["Uhrzeit"]
        if time not in grouped_schedule:
            grouped_schedule[time] = [("", "")] * fields
        

        if match["Feld"] == "All Fields":
            field_index = None
        else:
            try:
                field_index = int(match["Feld"].split()[-1]) - 1
            except ValueError:
                field_index = None
        
        if field_index is not None:
            grouped_schedule[time][field_index] = (
                f"{match['Team 1']} - {match['Team 2']} ({match['Match Type']})",
                match["Schiedsrichter"],
            )
        else:

            activity = "Pause" if match["Team 1"] == "Pause" else "Einspielzeit"
            grouped_schedule[time] = [(activity, "Nicht benötigt")] * fields


    for time, matches in grouped_schedule.items():
        html += f"<tr><td>{time}</td>"
        for field_match, referee in matches:
            html += f"<td>{field_match}</td><td>{referee}</td>"
        html += "</tr>"

    html += """
            </tbody>
        </table>
    </body>
    </html>
    """
    return html



#html_output = create_html(schedule, fields)

#with open("turnierplan.html", "w", encoding="utf-8") as file:
#    file.write(html_output)
