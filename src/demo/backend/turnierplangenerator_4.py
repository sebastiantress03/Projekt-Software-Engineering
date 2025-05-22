import random
from datetime import datetime, timedelta


def calculate_waiting_time(current_time, team_last_played_time):
    return (current_time - team_last_played_time).total_seconds()


def assign_fields_to_groups(fields, group_names):
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





def create_tournament_plan(
    fields, teams_per_group, performance_groups, start_time, match_duration,
    round_trip, play_in_time, pause_length, pause_interval, pause_count,
    group_names=None, team_names=None
):
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


    team_status = {team_id: {"plays": 0, "ref_count": 0} for team_id in teams}


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


                    round_matches.append({
                        "Spiel": len(schedule) + len(round_matches) + 1,
                        "Feld": f"Field {field}",
                        "Uhrzeit": current_time.strftime("%H:%M"),
                        "Team 1": teams[team1]["name"],
                        "Team 2": teams[team2]["name"],
                        "Schiedsrichter": None,
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


                    if match_type == "Hinspiel" and round_trip:
                        reverse_match = (team2, team1, group_name, "Rückspiel")
                        if reverse_match in remaining_matches:
                            round_matches.append({
                                "Spiel": len(schedule) + len(round_matches) + 1,
                                "Feld": f"Field {field}",
                                "Uhrzeit": (current_time + timedelta(minutes=match_duration)).strftime("%H:%M"),
                                "Team 1": teams[team2]["name"],
                                "Team 2": teams[team1]["name"],
                                "Schiedsrichter": None,
                                "Gruppe": group_name,
                                "Ergebnis Team 1": None,
                                "Ergebnis Team 2": None,
                                "Match Type": "Rückspiel",
                            })
                            playing_teams.update([team2, team1])
                            team_status[team2]["plays"] += 1
                            team_status[team1]["plays"] += 1
                            remaining_matches.remove(reverse_match)
                    break  


        for field in list(available_fields):
            for match in filter_least_played_matches(remaining_matches, team_status):
                team1, team2, group_name, match_type = match
                

                if field not in field_assignment[group_name]:
                    continue
                team1, team2, group_name, match_type = match
                if team1 in playing_teams or team2 in playing_teams:
                    continue
                round_matches.append({
                    "Spiel": len(schedule) + len(round_matches) + 1,
                    "Feld": f"Field {field}",
                    "Uhrzeit": current_time.strftime("%H:%M"),
                    "Team 1": teams[team1]["name"],
                    "Team 2": teams[team2]["name"],
                    "Schiedsrichter": None,
                    "Gruppe": group_name,
                    "Ergebnis Team 1": None,
                    "Ergebnis Team 2": None,
                    "Match Type": match_type,
                })
                playing_teams.update([team1, team2])
                team_status[team1]["plays"] += 1
                team_status[team2]["plays"] += 1
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
                            "Schiedsrichter": None,
                            "Gruppe": group_name,
                            "Ergebnis Team 1": None,
                            "Ergebnis Team 2": None,
                            "Match Type": "Rückspiel",
                        })
                        playing_teams.update([team2, team1])
                        team_status[team2]["plays"] += 1
                        team_status[team1]["plays"] += 1
                        remaining_matches.remove(reverse_match)
                break


        if round_matches:
            schedule.extend(round_matches)
            last_referees = {
                team_id for match in round_matches
                for team_id, team_data in teams.items()
                if match["Schiedsrichter"] == team_data["name"]
            }

            if round_trip:
                current_time += timedelta(minutes=match_duration * 2)
            else:
                current_time += timedelta(minutes=match_duration)    
            round_number += 1
        else:
            print("No valid matches available. Exiting.")
            break


        for team_id in teams:
            if team_id not in playing_teams:
                team_status[team_id]["consecutive_plays"] = 0

    return schedule, teams
def optimize_referees(schedule, teams, match_duration):
    from datetime import datetime, timedelta
    from collections import defaultdict, Counter
    import random

    def time_obj(t):
        return datetime.strptime(t, "%H:%M")

    team_play_times = defaultdict(list)
    time_slots = sorted(set(time_obj(m["Uhrzeit"]) for m in schedule if "Match Type" in m))

    for match in schedule:
        if "Match Type" not in match:
            continue
        t = time_obj(match["Uhrzeit"])
        for team_id, team in teams.items():
            if team["name"] in [match["Team 1"], match["Team 2"]]:
                team_play_times[team_id].append(t)

    match_pairs = []
    used = set()
    for i, m1 in enumerate(schedule):
        if i in used or "Match Type" not in m1 or m1["Match Type"] != "Hinspiel":
            continue
        for j, m2 in enumerate(schedule):
            if j in used or i == j:
                continue
            if (m2.get("Match Type") == "Rückspiel"
                and m2["Team 1"] == m1["Team 2"]
                and m2["Team 2"] == m1["Team 1"]
                and m2["Gruppe"] == m1["Gruppe"]):
                match_pairs.append((m1, m2))
                used.add(i)
                used.add(j)
                break
        else:
            match_pairs.append((m1, None))
            used.add(i)


    referee_assignment = [None for _ in match_pairs]


    def build_referee_map(assignments):
        ref_map = defaultdict(set)  
        for (m1, m2), ref_id in zip(match_pairs, assignments):
            if not ref_id:
                continue
            t1 = time_obj(m1["Uhrzeit"])
            t2 = time_obj(m2["Uhrzeit"]) if m2 else t1 + timedelta(minutes=match_duration)
            name = teams[ref_id]["name"]
            ref_map[t1].add(name)
            ref_map[t2].add(name)
        return ref_map

    def get_valid_candidates(index, current_assignment):
        m1, m2 = match_pairs[index]
        group = m1["Gruppe"]
        t1 = time_obj(m1["Uhrzeit"])
        t2 = time_obj(m2["Uhrzeit"]) if m2 else t1 + timedelta(minutes=match_duration)
        ref_map = build_referee_map(current_assignment)

        valid = []
        for tid, team in teams.items():
            if team["group"] != group:
                continue
            if team["name"] in [m1["Team 1"], m1["Team 2"]]:
                continue
            if any(abs((t - pt).total_seconds()) < match_duration * 60
                   for t in [t1, t2]
                   for pt in team_play_times[tid]):
                continue
     
            if team["name"] in ref_map[t1] or team["name"] in ref_map[t2]:
                continue
            valid.append(tid)
        return valid


    referee_counts = Counter()
    for i in range(len(match_pairs)):
        candidates = get_valid_candidates(i, referee_assignment)
        if candidates:
            chosen = random.choice(candidates)
            referee_assignment[i] = chosen
            referee_counts[teams[chosen]["name"]] += 1


    def build_timelines(assignments):
        timelines = {tid: [] for tid in teams}
        for t in time_slots:
            for tid in teams:
                name = teams[tid]["name"]

                is_playing = t in team_play_times[tid]

                is_ref = False
                for (m1, m2), ref_id in zip(match_pairs, assignments):
                    if ref_id == tid:
                        t1 = time_obj(m1["Uhrzeit"])
                        t2 = time_obj(m2["Uhrzeit"]) if m2 else t1 + timedelta(minutes=match_duration)
                        if t in [t1, t2]:
                            is_ref = True
                            break
                if is_playing:
                    timelines[tid].append("P")
                elif is_ref:
                    timelines[tid].append("R")
                else:

                    if any(m["Team 1"] == "Pause" and m["Uhrzeit"] == t.strftime("%H:%M") for m in schedule):
                        timelines[tid].append("P")
                    else:
                        timelines[tid].append("-")

        return timelines


    def cost(assignments):
        counts = Counter()
        for rid in assignments:
            if rid:
                counts[teams[rid]["name"]] += 1
        avg = sum(counts.values()) / len(teams)
        fairness_cost = sum((v - avg) ** 2 for v in counts.values())

        timelines = build_timelines(assignments)
        idle_cost = 0
        double_ref_cost = 0
        isolated_ref_cost = 0

        for line in timelines.values():
            for i in range(len(line) - 1):
                if line[i] == '-' and line[i + 1] == '-':
                    idle_cost += 1
                if line[i] == 'R' and line[i + 1] == 'R':
                    double_ref_cost += 1


            for i in range(len(line) - 2):
                if line[i] == 'R' and line[i+2] == 'R' and line[i+1] in ['-', 'P']:
                    isolated_ref_cost += 1


        return fairness_cost + idle_cost * 3 + double_ref_cost * 2 + isolated_ref_cost * 4



    for _ in range(100):
        i = random.randint(0, len(match_pairs) - 1)
        current = referee_assignment[i]
        candidates = get_valid_candidates(i, referee_assignment)
        if not candidates:
            continue

        best_ref = current
        best_cost = cost(referee_assignment)

        for cand in candidates:
            if cand == current:
                continue
            referee_assignment[i] = cand
            new_cost = cost(referee_assignment)
            if new_cost < best_cost:
                best_cost = new_cost
                best_ref = cand
            referee_assignment[i] = current  

        referee_assignment[i] = best_ref


    for (m1, m2), ref_id in zip(match_pairs, referee_assignment):
        if ref_id:
            name = teams[ref_id]["name"]
            m1["Schiedsrichter"] = name
            if m2:
                m2["Schiedsrichter"] = name

    return schedule




def main():
    fields = 3
    performance_groups = 2
    teams_per_group = 6
    start_time = "12:00"
    match_duration = 15
    round_trip = False
    play_in_time = 30
    pause_length = 30
    pause_count = 1
    pause_interval = 2
    group_names = ["Schwitzer", "Fun"]
    team_names = [
        "STeam 1", "STeam 2", "STeam 3", "STeam 4", "STeam 5", "STeam 6",
        "FTeam1", "FTeam2", "FTeam 3", "FTeam 4", "FTeam 5", "FTeam 6"
        
    ]

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
    schedule = optimize_referees(schedule, teams, match_duration)
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
    
    html_output = create_html(schedule, fields)
    with open("turnierplan.html", "w", encoding="utf-8") as file:
        file.write(html_output)
    print("HTML-Datei 'turnierplan.html' wurde geschrieben.")

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


if __name__ == "__main__":
    main()
