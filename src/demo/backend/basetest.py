import unittest
from turnierueberarbeitung import baue_status_lists, get_statusverlaeufe, extrahiere_zeiten , initialisiere_status_lists, main
import logging
import time
import random

class Testmygenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Setze den Zufallszahlengenerator auf einen festen Wert für reproduzierbare Ergebnisse
    
    def pfeifeniemalsgegendichselbst(self, schedule): 
        # Pfeife dich niemals selsbt
        for match in schedule: 
            if match.get("Match Type"): 
                team1 = match.get("Team 1")
                team2 = match.get("Team 2")
                schiedsrichter = match.get("Schiedsrichter")
                self.assertNotEqual(team1, schiedsrichter)
                self.assertNotEqual(team2, schiedsrichter)


    def spieleniemalsgegendichselbst(self, schedule): 
        #Spiele nie gegen sich selbst 
        for match in schedule:
            if match.get("Match Type"): 
                team1 = match.get("Team 1")
                team2 = match.get("Team 2")
                self.assertNotEqual(team1, team2)

    def checkstatusverlaeufe(self, verlaeufe):
        for name, status in verlaeufe.items():
            with self.subTest(team=name):
                self.assertNotIn("FFFF", status, f"{name} hat doppelte Pause")
                self.assertNotIn("PPFFPP", status, f"{name} hat ungültige Kombination pfeifen-frei-pfeifen")
                self.assertNotIn("PPPP", status, f"{name} hat mehrfaches Pfeifen")

    def checkfails(self, fehler): 
        self.assertEqual(fehler, 0, "Keinen passenden Spielplan generiert!")

    def checknumberofgames(self, anz_teams, anz_gruppen, schedule, playstyle): 
        # Überprüfen, ob der Spielplan korrekt ist
        if playstyle == True: 
            number_games = (anz_teams*(anz_teams-1)) * anz_gruppen + 2 # die plus zwei stehen hier für 1 Pause und eine Einspielzeit
            self.assertEqual(len(schedule), number_games)
        else: 
            number_games = (anz_teams*(anz_teams-1) // 2) * anz_gruppen + 2 # die plus zwei stehen hier für 1 Pause und eine Einspielzeit
            self.assertEqual(len(schedule), number_games)

    def checkgleichverteilung(self, anz_teams, verlauf, strartdesnamens): 
        #Gleichverteilung ermitteln
        x = anz_teams + 1 
        zaehlungen = {f"{strartdesnamens} {i}": 0 for i in range(1, x)}

        for name, verlauf_str in verlauf.items():
            
            if name in zaehlungen:
                zaehlungen[name] = verlauf_str.count("P")
        sum = 0
        for i in range(1, x): 
            sum = sum + zaehlungen[f"{strartdesnamens} {i}"]  

        durchschnitt = sum / anz_teams

        for teamname, wert in zaehlungen.items():
            with self.subTest(team = teamname):
                self.assertTrue(abs(wert- durchschnitt) <= 2, "Die Anzahl der Spiele ist nicht gleichmäßig verteilt.")
        # debugging
        # print("Zählungen:", zaehlungen)
        # print("Durchschnitt:", durchschnitt)

    def getnames(self, anzahl_teams, anzahl_gruppen):
        team_namen = []
        if anzahl_gruppen == 2: 
            for i in range(1, anzahl_teams +1): 
                team_namen.append(f"STeam {i}")
            for i in range(1, anzahl_teams +1): 
                team_namen.append(f"FTeam {i}")
        if anzahl_gruppen == 1: 
            for i in range(1, anzahl_teams +1): 
                team_namen.append(f"Team {i}")
        return team_namen
    
    def checkifrefereeexists(self, schedule, team_namen):
        for match in schedule:
            if match.get("Match Type"):  # Nur echte Spiele prüfen
                schiri = match.get("Schiedsrichter")
                # Assert: Schiedsrichter muss ein Teamname sein
                with self.subTest(spiel=match.get("Spiel", "?")):
                    self.assertIsNotNone(schiri, "Schiedsrichter ist None!")
                    self.assertNotEqual(schiri, "Not required", "Schiedsrichter darf nicht 'Not required' sein!")
                    self.assertIn(schiri, team_namen, f"Schiedsrichter '{schiri}' nicht in der Teamliste!")

