import unittest

import sys
import os
sys.path.append(os.path.abspath(".."))


from basetest import Testmygenerator

from turnierueberarbeitung import main, baue_status_lists, get_statusverlaeufe, rekonstruiere_teams
from turnierplangenerator_4 import return_plan

class Test6M2L3F_HR(Testmygenerator):
    """
    Testklasse für den konkreten Turnierfall: 6 Teams, 3 Felder, 2 Gruppen, Hin- und Rückspiel aktiviert.

    Es wird überprüft, ob der generierte Spielplan valide, fair verteilt und korrekt ausgewertet ist.

    SetUp:
        - Es werden automatisch ein Spielplan (schedule), die Teams, Statuslisten und Statusverläufe generiert.
        - Die Daten basieren auf dem Aufruf der main()-Funktion aus der turnierueberarbeitung-Klasse mit den angegebenen Parametern.

    Hinweise:
        - Diese Klasse erbt von Testmygenerator und nutzt deren Testhilfsmethoden für Validierungen.
    """

    @classmethod
    def setUpClass(cls):

        cls.fields = 3
        cls.performance_groups = 2
        cls.teams_per_group = [6, 6]
        cls.start_time = "12:00"
        cls.match_duration = 15
        cls.round_trip = True
        cls.play_in_time = 30
        cls.pause_length = [30]
        cls.pause_count = 2
        cls.pause_interval = 4
        cls.group_names = ["Fun", "Schwitzer"]
        cls.break_times = []

        # Rekonstruiere teams passend zu Namen und Gruppen
        cls.teams = rekonstruiere_teams(
            cls.teams_per_group, cls.group_names)

        cls.team_namen = [f"{'FTeam' if i == 0 else 'STeam'}_{j}"
                            for i, anz in enumerate(cls.teams_per_group)
                                for j in range(anz)
        ]
        # Turnierplan erzeugen
        cls.schedule = return_plan(
            cls.fields,
            cls.teams_per_group,
            cls.start_time,
            cls.match_duration,
            cls.round_trip,
            cls.play_in_time,
            cls.pause_length,
            cls.pause_count,
            cls.break_times,
            cls.group_names
        )

        # Status erzeugen
        cls.status_list, _ = baue_status_lists(cls.schedule, cls.teams)
        cls.verlauf = get_statusverlaeufe(cls.status_list, cls.teams)

    def test_spieleniemalsgegendichselbst(self):
        self.spieleniemalsgegendichselbst(self.schedule)

    def test_pfeifeniemalsgegendichselbst(self):
        self.pfeifeniemalsgegendichselbst(self.schedule)

    def test_refereeexists(self):
        self.checkifrefereeexists(self.schedule, self.team_namen)

    def test_gleichverteilung(self):
        self.checkgleichverteilung(self.teams_per_group[0], self.verlauf, "STeam")
        self.checkgleichverteilung(self.teams_per_group[0], self.verlauf, "FTeam")

    def test_statusverlaeufe(self):
        self.checkstatusverlaeufe(self.verlauf)

    def test_number_of_games(self):
        self.checknumberofgames(self.teams_per_group[0], len(self.group_names), self.schedule, self.round_trip)

#   def test_keine_fehler(self):
#        self.checkfails(self.fehler)
