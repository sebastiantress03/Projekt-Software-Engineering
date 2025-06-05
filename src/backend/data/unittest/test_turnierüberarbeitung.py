import unittest

from turnierueberarbeitung import baue_status_lists, get_statusverlaeufe, extrahiere_zeiten , initialisiere_status_lists       
class TestDeineKomponente(unittest.TestCase):
# Hier wird die Funktinalität der Klasse einfachdruck getestet
    def setUp(self):
        """Wird vor jedem Test ausgeführt."""
        """class TurnamentPlan(BaseModel):
            game_number: int
            field_number: int
            team1: str              # Leistungsgruppe(ersten 2 Buchstaben) + Team + Nummer 
            team2: str           
            referee: str 
            stage_name: str
            score_team1: int
            score_team2: int
            time_of_game: time
        """     
        match1 = {
            "Spiel": 1,
            "Feld": "Field 1",
            "Uhrzeit": "12:30",
            "Team 1": "STeam 1",
            "Team 2": "STeam 2",
            "Schiedsrichter": "STeam 3",
            "Gruppe": "Schwitzer",
            "Ergebnis Team 1": None,
            "Ergebnis Team 2": None,
            "Match Type": "Hinspiel"
        }
        match2 = {
            "Spiel": 2,
            "Feld": "Field 2",
            "Uhrzeit": "12:45",
            "Team 1": "STeam 3",
            "Team 2": "STeam 4",
            "Schiedsrichter": "STeam 1",
            "Gruppe": "Schwitzer",
            "Ergebnis Team 1": None,
            "Ergebnis Team 2": None,
            "Match Type": "Hinspiel"
        }

        # 2) Pause um 13:00 (wird ignoriert)
        pause = {
            "Spiel": 3,
            "Feld": "All Fields",
            "Uhrzeit": "13:00",
            "Team 1": "Pause",
            "Team 2": "Pause",
            "Schiedsrichter": "Not required",
            "Gruppe": "N/A",
            "Ergebnis Team 1": None,
            "Ergebnis Team 2": None,
        }

        # 3) Rückspiel um 13:30
        match3 = {
            "Spiel": 4,
            "Feld": "Field 1",
            "Uhrzeit": "13:15",
            "Team 1": "STeam 2",
            "Team 2": "STeam 1",
            "Schiedsrichter": "STeam 4",
            "Gruppe": "Schwitzer",
            "Ergebnis Team 1": None,
            "Ergebnis Team 2": None,
            "Match Type": "Rückspiel"
        }


        self.schedule = [match1, match2, pause, match3]

        # Teams-Dict so, wie baue_status_lists es erwartet:
        self.teams = {
            "team1": {"name": "STeam 1", "group": "Schwitzer"},
            "team2": {"name": "STeam 2", "group": "Schwitzer"},
            "team3": {"name": "STeam 3", "group": "Schwitzer"},
            "team4": {"name": "STeam 4", "group": "Schwitzer"},
        }

        self.lists= baue_status_lists(self.schedule, self.teams)[0]  # Assuming the first element is the desired dictionary

    def tearDown(self):
        """Wird nach jedem Test ausgeführt (optional)."""
        # z. B. Aufräumen von Dateien, Datenbankverbindungen schließen etc.
        pass

    def test_extrahiereZeiten(self):
        """
        Testet die Funktion `extrahiere_zeiten`, die alle Uhrzeiten aus einem Spielplan extrahiert.

        Beispiel:
            - test_extrahiereZeiten ruft extrahiere_zeiten(self.schedule) auf.

        Rückgabewert:
            - None

        Fehlerbehandlung:
            - Test schlägt fehl, wenn nicht genau 3 Zeit-Slots erkannt werden (eine Pause wird ignoriert).

        Hinweise:
            - Erwartete Zeitpunkte im Beispiel: 12:30, 12:45, 13:15
            - „Pause“-Eintrag wird ignoriert.
            - Es handelt sich um Beispieldaten die generiert wurden
        """

        zeiten = extrahiere_zeiten(self.schedule)
        self.assertEqual(len(zeiten), 3)  # Es gibt 3 verschiedene Zeit-Slots

    def test_initialisiere_status_lists(self):
        """
        Testet die Funktion `initialisiere_status_lists`, welche eine leere Statusliste je Team erstellt.

        Beispiel:
            - test_initialisiere_status_lists ruft initialisiere_status_lists(self.teams, self.schedule) auf.

        Rückgabewert:
            - None

        Fehlerbehandlung:
            - Test schlägt fehl, wenn nicht für jedes Team eine Liste mit vier 'F' erzeugt wird.

        Hinweise:
            - Die Liste enthält für jeden Zeitslot eine Initialisierung mit 'F' (für „Frei“).
            - Dies stellt die korrekte Vorbereitung für spätere Statusauswertung sicher.
        """
        verlauf = initialisiere_status_lists(self.teams, self.schedule)
        self.assertEqual(len(verlauf), 4)
        self.assertEqual(verlauf["team1"], ['F', 'F', 'F', 'F'])
        self.assertEqual(verlauf["team2"], ['F', 'F', 'F', 'F'])
        self.assertEqual(verlauf["team3"], ['F', 'F', 'F', 'F'])
        self.assertEqual(verlauf["team4"], ['F', 'F', 'F', 'F'])

    def test_funktion_standardfall(self):
        """
        Testet die Funktion `get_statusverlaeufe` im Standardfall anhand eines vorbereiteten Spielplans.

        Beispiel:
            - test_funktion_standardfall ruft get_statusverlaeufe(self.lists, self.teams) auf.

        Rückgabewert:
            - None

        Fehlerbehandlung:
            - Test schlägt fehl, wenn die berechneten Statusverläufe nicht mit den erwarteten Werten übereinstimmen.

        Hinweise:
            - Statusverläufe beinhalten:
                - S = Spiel
                - P = Pfeifen
                - F = Frei
            - Erwartete Ergebnisse in diesem Setup:
                - "STeam 1": 'SPS'
                - "STeam 2": 'SFS'
                - "STeam 3": 'PSF'
                - "STeam 4": 'FSP'
        """
        verlauf = get_statusverlaeufe(self.lists, self.teams)
        self.assertEqual(verlauf.get("STeam 1"), 'SPS') 
        self.assertEqual(verlauf.get("STeam 2"), 'SFS')
        self.assertEqual(verlauf.get("STeam 3"), 'PSF')
        self.assertEqual(verlauf.get("STeam 4"), 'FSP')



if __name__ == '__main__':
    unittest.main()
