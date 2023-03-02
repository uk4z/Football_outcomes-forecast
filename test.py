from django.test import TestCase
from data import *

class League_TestCases(TestCase):
    """For this series of test, results are based on 2022/2023 football seasons."""

    """Methods not directly used in the main file"""

    def test__match_result(self):
        self.assertIsNone(match_result(['AC Ajaccio','2:1','OGC Nice'], 'RC Lens'))
        self.assertEqual(match_result(['Montpellier HSC', '1:1', 'RC Strasbourg Alsace'], 'RC Strasbourg Alsace'), ['D',1,1])
        self.assertEqual(match_result(['Montpellier HSC', '1:1', 'RC Strasbourg Alsace'], 'RC Strasbourg Alsace'),
                         match_result(['Montpellier HSC', '1:1', 'RC Strasbourg Alsace'], 'Montpellier HSC'))
        self.assertEqual(match_result(['Southampton FC', '3:1', 'Leicester City'], 'Leicester City'), ['L',1,3])
        self.assertEqual(match_result(['Southampton FC', '3:1', 'Leicester City'], 'Southampton FC'), ['W',3,1])


    def test_league_table(self):
        self.assertEqual(ligue_1.league_table(9),{'Paris Saint-Germain': 1, 
                                                  'Olympique Marseille': 2, 
                                                  'FC Lorient': 3, 
                                                  'RC Lens': 4, 
                                                  'AS Monaco': 5, 
                                                  'Stade Rennais FC': 6, 
                                                  'Olympique Lyon': 7, 
                                                  'LOSC Lille': 8, 
                                                  'Clermont Foot 63': 9, 
                                                  'Montpellier HSC': 10, 
                                                  'ESTAC Troyes': 11, 
                                                  'FC Toulouse': 12, 
                                                  'OGC Nice': 13, 
                                                  'AJ Auxerre': 14, 
                                                  'Angers SCO': 15, 
                                                  'FC Nantes': 16, 
                                                  'Stade Reims': 17, 
                                                  'Stade Brestois 29': 18, 
                                                  'RC Strasbourg Alsace': 19, 
                                                  'AC Ajaccio': 20})

        self.assertEqual(bundesliga.league_table(22),{'Bayern Munich': 1, 
                                                      'Borussia Dortmund': 2, 
                                                      '1.FC Union Berlin': 3, 
                                                      'RB Leipzig': 4, 
                                                      'SC Freiburg': 5, 
                                                      'Eintracht Frankfurt': 6, 
                                                      'VfL Wolfsburg': 7, 
                                                      '1.FSV Mainz 05': 8, 
                                                      'SV Werder Bremen': 9, 
                                                      'Borussia Mönchengladbach': 10, 
                                                      'Bayer 04 Leverkusen': 11, 
                                                      '1. FC Köln': 12, 
                                                      'FC Augsburg': 13, 
                                                      'Hertha BSC': 14, 
                                                      'VfB Stuttgart': 15, 
                                                      'TSG 1899 Hoffenheim': 16, 
                                                      'VfL Bochum': 17, 
                                                      'FC Schalke 04': 18})
        
        with self.assertRaises(ValueError): bundesliga.league_table(38)
        
    def test_match_day(self):
        self.assertEqual(serie_a.match_day(36),[['Atalanta BC', 'Hellas Verona'], 
                                                ['US Cremonese', 'Bologna FC 1909'], 
                                                ['FC Empoli', 'Juventus FC'], 
                                                ['US Lecce', 'Spezia Calcio'], 
                                                ['AC Milan', 'UC Sampdoria'], 
                                                ['SSC Napoli', 'Inter Milan'], 
                                                ['AS Roma', 'US Salernitana 1919'], 
                                                ['US Sassuolo', 'AC Monza'], 
                                                ['Torino FC', 'ACF Fiorentina'], 
                                                ['Udinese Calcio', 'SS Lazio']])
        
        self.assertEqual(primera_division.match_day(24), [['Real Sociedad', 'Cádiz CF'], 
                                                          ['Getafe CF', 'Girona FC'], 
                                                          ['UD Almería', 'Villarreal CF'], 
                                                          ['RCD Mallorca', 'Elche CF'], 
                                                          ['Atlético de Madrid', 'Sevilla FC'], 
                                                          ['Real Valladolid CF', 'RCD Espanyol Barcelona'], 
                                                          ['FC Barcelona', 'Valencia CF'], 
                                                          ['Rayo Vallecano', 'Athletic Bilbao'], 
                                                          ['Real Betis Balompié', 'Real Madrid'], 
                                                          ['CA Osasuna', 'Celta de Vigo']])

        with self.assertRaises(ValueError) : self.assertEqual(primera_division.match_day(87))


    def test_result_day(self):
        self.assertEqual(primera_division.result_day(18),[['RCD Mallorca', '1:0', 'Celta de Vigo'], 
                                                          ['Rayo Vallecano', '0:2', 'Real Sociedad'], 
                                                          ['RCD Espanyol Barcelona', '1:0', 'Real Betis Balompié'], 
                                                          ['Atlético de Madrid', '3:0', 'Real Valladolid CF'], 
                                                          ['Sevilla FC', '1:0', 'Cádiz CF'], 
                                                          ['Villarreal CF', '1:0', 'Girona FC'], 
                                                          ['Elche CF', '1:1', 'CA Osasuna'], 
                                                          ['FC Barcelona', '1:0', 'Getafe CF'], 
                                                          ['Athletic Bilbao', '0:2', 'Real Madrid'], 
                                                          ['Valencia CF', '2:2', 'UD Almería']])
        
        self.assertEqual(ligue_1.result_day(25),[['LOSC Lille', '2:1', 'Stade Brestois 29'], 
                                                 ['Angers SCO', '1:3', 'Olympique Lyon'], 
                                                 ['Montpellier HSC', '1:1', 'RC Lens'], 
                                                 ['FC Lorient', '0:1', 'AJ Auxerre'], 
                                                 ['AC Ajaccio', '2:1', 'ESTAC Troyes'], 
                                                 ['Clermont Foot 63', '1:1', 'RC Strasbourg Alsace'], 
                                                 ['FC Nantes', '0:1', 'Stade Rennais FC'], 
                                                 ['Stade Reims', '3:0', 'FC Toulouse'], 
                                                 ['AS Monaco', '0:3', 'OGC Nice'], 
                                                 ['Olympique Marseille', '0:3', 'Paris Saint-Germain']])
        
        with self.assertRaises(ValueError): ligue_1.result_day(40)



class Club_TestCases(TestCase):
    """For this series of test, results are based on 2022/2023 football seasons."""

    def test_game(self):
        self.assertEqual(Lille.game(25),['LOSC Lille', 'Stade Brestois 29'])

        with self.assertRaises(ValueError): Barcelona.game(52)

    def test_game_form(self):
        with self.assertRaises(SyntaxError): Real_madrid.game_form(2, 4)
        with self.assertRaises(ValueError): Wolsburg.game_form(5, 3, defense=True)
        with self.assertRaises(ValueError): Wolsburg.game_form(5, 45, defense=True)

        self.assertEqual(Real_sociedad.game_form(2, 4, attack=True), {'Real Sociedad': [[1, 1]], 'Atlético de Madrid': [[1, 0]]})
        self.assertEqual(Monza.game_form(4, 19, attack=True, defense=True, performance=True),
                         {'AC Monza': [['W', 'D', 'D', 'W'], [3, 2, 1, 3], [2, 2, 1, 0]], 
                        'US Sassuolo': [['L', 'L', 'L', 'L'], [0, 1, 1, 0], [2, 2, 2, 3]]})
        
    def test_club_form(self):
        with self.assertRaises(ValueError): Arsenal.club_form(6,6, performance=True)
        with self.assertRaises(ValueError): Arsenal.club_form(2,39, attack=True)
        with self.assertRaises(SyntaxError): Lyon.club_form(4, 7)

        self.assertEqual(Espagnol_barcelona.club_form(2, 17, defense=True, performance=True), [['D', 'D'], [2, 1]])

    def test_rank(self):
        with self.assertRaises(ValueError): Liverpool.rank(87)
        
        self.assertEqual(Liverpool.rank(8), 7)

    def test_rank_confrontation(self):
        with self.assertRaises(ValueError): Liverpool.rank_confrontation(39)

        self.assertEqual(Liverpool.rank_confrontation(5), Newcastle.rank_confrontation(5))
        self.assertEqual(Liverpool.rank_confrontation(5), [9,7] )

    def test_form_confrontation(self):
        with self.assertRaises(ValueError): Marseille.form_confrontation(53, 2, attack=True)
        with self.assertRaises(SyntaxError): Marseille.form_confrontation(12,3)
        with self.assertRaises(ValueError): Marseille.form_confrontation(12, 13, attack=True)
        
        self.assertEqual(Marseille.form_confrontation(23,3,attack=True,performance=True),
                        {'Clermont Foot 63': [['L', 'D', 'D'], [0, 0, 0]], 'Olympique Marseille': [['L', 'W', 'D'], [1, 2, 1]]})


    


        
    