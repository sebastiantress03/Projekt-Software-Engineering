import unittest
from turnierueberarbeitung import baue_status_lists, get_statusverlaeufe, extrahiere_zeiten , initialisiere_status_lists, main
import logging
import time
import random

class Testmygenerator(unittest.TestCase):

    def setUp(self):
        random.seed(42)  # Setze den Zufallszahlengenerator auf einen festen Wert für reproduzierbare Ergebnisse
    
    def pfeifeniemalsgegendichselbst(self, schedule): 
        """
        Testet, ob in einem gegebenen Spielplan (schedule) kein Team als Schiedsrichter bei seinem eigenen Spiel eingesetzt wird.

        Parameter:
            - schedule (list): Eine Liste von Dictionaries, die Spielinformationen enthalten (z.B. 'Team 1', 'Team 2', 'Schiedsrichter').

        Beispiel:
            - self.pfeifeniemalsgegendichselbst(generierter_spielplan)

        Rückgabewert:
            - None (wird im Rahmen eines UnitTests verwendet)

        Fehlerbehandlung:
            - Löst einen AssertionError aus, falls ein Team in seinem eigenen Spiel als Schiedsrichter eingetragen ist.

        Hinweise:
            - Funktioniert nur, wenn das Feld "Match Type" vorhanden und gesetzt ist (z. B. zum Filtern von echten Spielen).
        """

        for match in schedule: 
            if match.get("Match Type"): 
                team1 = match.get("Team 1")
                team2 = match.get("Team 2")
                schiedsrichter = match.get("Schiedsrichter")
                self.assertNotEqual(team1, schiedsrichter)
                self.assertNotEqual(team2, schiedsrichter)


    def spieleniemalsgegendichselbst(self, schedule): 
        """
        Testet, ob ein Team niemals gegen sich selbst spielt.

        Parameter:
            - schedule (list): Eine Liste von Dictionaries mit Spielinformationen ('Team 1', 'Team 2').

        Beispiel:
            - self.spieleniemalsgegendichselbst(generierter_spielplan)

        Rückgabewert:
            - None

        Fehlerbehandlung:
            - Löst AssertionError, wenn Team 1 und Team 2 gleich sind.

        Hinweise:
            - Prüft nur Einträge mit gesetztem "Match Type".
        """

        for match in schedule:
            if match.get("Match Type"): 
                team1 = match.get("Team 1")
                team2 = match.get("Team 2")
                self.assertNotEqual(team1, team2)

    def checkstatusverlaeufe(self, verlaeufe):
        """
        Validiert die Statusverläufe aller Teams hinsichtlich unzulässiger Kombinationen.

        Parameter:
            - verlaeufe (dict): Ein Dictionary mit Teamnamen als Keys und Status-Strings als Values (z.B. "SSFPF").

        Beispiel:
            - self.checkstatusverlaeufe(get_statusverlaeufe(spielplan))

        Rückgabewert:
            - None

        Fehlerbehandlung:
            - Löst AssertionError bei:
                - Vier aufeinanderfolgenden Pausen ("FFFF")
                - Pfeifen-frei-pfeifen-Kombination ("PPFFPP")
                - Viermaligem Pfeifen ("PPPP")

        Hinweise:
            - Nutzt `subTest`, um genaue Fehlermeldungen je Teamname auszugeben.
        """
        for name, status in verlaeufe.items():
            with self.subTest(team=name):
                self.assertNotIn("FFFF", status, f"{name} hat doppelte Pause")
                self.assertNotIn("PPFFPP", status, f"{name} hat ungültige Kombination pfeifen-frei-pfeifen")
                self.assertNotIn("PPPP", status, f"{name} hat mehrfaches Pfeifen")

    def checkfails(self, fehler):
        """
        Prüft, ob ein generierter Spielplan fehlerfrei ist.

        Parameter:
            - fehler (int): Anzahl an Fehlerfällen (z. B. nicht erfüllte Bedingungen bei der Planerstellung).

        Beispiel:
            - self.checkfails(anzahl_fehler)

        Rückgabewert:
            - None

        Fehlerbehandlung:
            - AssertionError, wenn Fehleranzahl ungleich Null ist.
        """

        self.assertEqual(fehler, 0, "Keinen passenden Spielplan generiert!")

    def checknumberofgames(self, anz_teams, anz_gruppen, schedule, playstyle): 
        """
        Überprüft, ob die erwartete Anzahl an Spielen im Spielplan enthalten ist.

        Parameter:
            - anz_teams (int): Anzahl der Teams pro Gruppe.
            - anz_gruppen (int): Anzahl der Gruppen.
            - schedule (list): Der generierte Spielplan (Liste von Matches).
            - playstyle (bool): Gibt an, ob Hin- und Rückspiel aktiviert sind.

        Beispiel:
            - self.checknumberofgames(6, 2, spielplan, True)

        Rückgabewert:
            - None

        Fehlerbehandlung:
            - AssertionError, wenn Spielanzahl nicht mit der Erwartung übereinstimmt.

        Hinweise:
            - Es werden immer +2 Spiele für Pause und Einspielzeit angenommen.
        """

        if playstyle == True: 
            number_games = (anz_teams*(anz_teams-1)) * anz_gruppen + 2 # die plus zwei stehen hier für 1 Pause und eine Einspielzeit
            self.assertEqual(len(schedule), number_games)
        else: 
            number_games = (anz_teams*(anz_teams-1) // 2) * anz_gruppen + 2 # die plus zwei stehen hier für 1 Pause und eine Einspielzeit
            self.assertEqual(len(schedule), number_games)

    def checkgleichverteilung(self, anz_teams, verlauf, strartdesnamens): 
        """
        Stellt sicher, dass die Anzahl der 'P'-Status (z. B. Pfeifen) gleichmäßig über die Teams verteilt ist.

        Parameter:
            - anz_teams (int): Anzahl der Teams pro Gruppe.
            - verlauf (dict): Teamname → Status-String (z. B. "SSPFP").
            - strartdesnamens (str): Präfix der Teamnamen ("Team", "FTeam", etc.)

        Beispiel:
            - self.checkgleichverteilung(6, status_dict, "Team")

        Rückgabewert:
            - None

        Fehlerbehandlung:
            - AssertionError, wenn ein Team mehr als ±2 Abweichung vom Durchschnitt hat.

        Hinweise:
            - Berücksichtigt nur 'P'-Status.
        """
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
        """
        Erzeugt die Teamnamen basierend auf der Anzahl der Gruppen und Teams.

        Parameter:
            - anzahl_teams (int): Anzahl der Teams pro Gruppe.
            - anzahl_gruppen (int): Anzahl der Gruppen (1 oder 2).

        Beispiel:
            - teamnamen = self.getnames(6, 2)

        Rückgabewert:
            - list[str]: Liste der Teamnamen, z. B. ["Team 1", "Team 2", ..., "FTeam 1", ...]

        Hinweise:
            - Bei zwei Gruppen werden "STeam" und "FTeam" verwendet.
        """
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
        """
        Stellt sicher, dass jedes Spiel einen gültigen Schiedsrichter aus der Teamliste zugewiesen hat.

        Parameter:
            - schedule (list): Liste von Spielen als Dictionaries.
            - team_namen (list): Liste gültiger Teamnamen.

        Beispiel:
            - self.checkifrefereeexists(spielplan, team_namen)

        Rückgabewert:
            - None

        Fehlerbehandlung:
            - AssertionError bei fehlendem oder ungültigem Schiedsrichtereintrag.

        Hinweise:
            - 'Schiedsrichter' darf nicht None oder "Not required" sein.
            - Prüfung erfolgt nur für echte Matches mit gesetztem "Match Type".
        """
        for match in schedule:
            if match.get("Match Type"):  # Nur echte Spiele prüfen
                schiri = match.get("Schiedsrichter")
                # Assert: Schiedsrichter muss ein Teamname sein
                with self.subTest(spiel=match.get("Spiel", "?")):
                    self.assertIsNotNone(schiri, "Schiedsrichter ist None!")
                    self.assertNotEqual(schiri, "Not required", "Schiedsrichter darf nicht 'Not required' sein!")
                    self.assertIn(schiri, team_namen, f"Schiedsrichter '{schiri}' nicht in der Teamliste!")
