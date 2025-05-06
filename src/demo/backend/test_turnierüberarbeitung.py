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
        zeiten = extrahiere_zeiten(self.schedule)
        self.assertEqual(len(zeiten), 3)  # Es gibt 3 verschiedene Zeit-Slots

    def test_initialisiere_status_lists(self):
        verlauf = initialisiere_status_lists(self.teams, self.schedule)
        self.assertEqual(len(verlauf), 4)
        self.assertEqual(verlauf["team1"], ['F', 'F', 'F', 'F'])
        self.assertEqual(verlauf["team2"], ['F', 'F', 'F', 'F'])
        self.assertEqual(verlauf["team3"], ['F', 'F', 'F', 'F'])
        self.assertEqual(verlauf["team4"], ['F', 'F', 'F', 'F'])

    def test_funktion_standardfall(self):
        #immer mit den Namen der Schlüssel arbeiten
        verlauf = get_statusverlaeufe(self.lists, self.teams)
        self.assertEqual(verlauf.get("STeam 1"), 'SPS') 
        self.assertEqual(verlauf.get("STeam 2"), 'SFS')
        self.assertEqual(verlauf.get("STeam 3"), 'PSF')
        self.assertEqual(verlauf.get("STeam 4"), 'FSP')



if __name__ == '__main__':
    unittest.main()
