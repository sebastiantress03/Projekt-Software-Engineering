import unittest
from basetest import Testmygenerator
from turnierueberarbeitung import main, baue_status_lists, get_statusverlaeufe

class Test4M1L1F_HR(Testmygenerator):

    @classmethod
    def setUpClass(cls):
        cls.anzahl_teams = 4
        cls.felder = 1
        cls.anzahl_gruppen = 1
        cls.gruppen_namen = ["Schwitzer"]
        cls.playstyle = True
        cls.team_namen = cls.getnames(cls, cls.anzahl_teams, cls.anzahl_gruppen)

        cls.schedule, cls.teams, cls.fehler = main(
            cls.team_namen, cls.felder, cls.anzahl_teams, cls.gruppen_namen, cls.anzahl_gruppen, cls.playstyle
        )
        cls.status_list, _ = baue_status_lists(cls.schedule, cls.teams)
        cls.verlauf = get_statusverlaeufe(cls.status_list, cls.teams)

    def test_spieleniemalsgegendichselbst(self):
        self.spieleniemalsgegendichselbst(self.schedule)

    def test_pfeifeniemalsgegendichselbst(self):
        self.pfeifeniemalsgegendichselbst(self.schedule)

    def test_refereeexists(self):
        self.checkifrefereeexists(self.schedule, self.team_namen)

    def test_gleichverteilung(self):
        self.checkgleichverteilung(self.anzahl_teams, self.verlauf, "STeam")
        self.checkgleichverteilung(self.anzahl_teams, self.verlauf, "FTeam")

    def test_statusverlaeufe(self):
        self.checkstatusverlaeufe(self.verlauf)

    def test_number_of_games(self):
        self.checknumberofgames(self.anzahl_teams, self.anzahl_gruppen, self.schedule, self.playstyle)

    def test_keine_fehler(self):
        self.checkfails(self.fehler)
