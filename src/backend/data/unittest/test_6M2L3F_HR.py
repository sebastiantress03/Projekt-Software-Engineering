import unittest
from basetest import Testmygenerator
from turnierueberarbeitung import main, baue_status_lists, get_statusverlaeufe

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
        cls.anzahl_teams = 6
        cls.felder = 3
        cls.anzahl_gruppen = 2
        cls.gruppen_namen = ["Schwitzer", "Fun"]
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
