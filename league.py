from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# starting webdriver
options = Options()
options.add_argument("--headless=new")

driver_path = r"C:\Users\33652\Selenium webdriver\chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

from club import Club

class League :
    #variables written with capital letters are related to driver elements
    def __init__(self, id_transfermarkt, tag, year, nClubs, id_understat):
        """
        Arguments: 
            id_transfermarkt (string): name of the league appearing in the url of the transfermarkt website 
            id_understat (string): name of the league appearing in the url of the understat website 
            tag (string): tag of the league appearing in the url
            year (integer): year of the league season
            nClubs (integer): number of clubs in the league
        """
        self.id_transfermarkt = id_transfermarkt    
        self.tag = tag
        self.year = year
        self.nClubs = nClubs
        self.id_understat = id_understat

    """Methods that are not to be used directly from the main file"""
    
    
        
    def form(self, name_club, nMatch, matchDay, attack = False, defense = False, performance = False):
        """
        Returns the recent performance of a given club including attack and defense. 

        Arguments:
            nMatch (integer): the number of previous games considered in order to give the past performance of a club
            name_club (string): name of the club concerned
            attack (bool): if the attack data will be in the output
            defense (bool): if the defense data will be in the output
            performance (bool): if the performance data will be in the output

        Returns:
            list[list]: [performance, attack, defense] data from the previous games
        """
        if not (attack or defense or performance):
            raise SyntaxError ("""Missing one argument: must chose at least on statistic to study from attack, defense or performance""")
        
        if nMatch >= matchDay :
            raise ValueError("""There is not enough games played""")
        
        if matchDay > (self.nClubs-2)*2 :
            raise ValueError("""There is not enough games in a season.""")
        
        outcome, goals, goals_against = [], [], []
        i = matchDay - 1
        while i >= matchDay - nMatch and i >=  0:
            resultDay = self.result_day(i)
            for match in resultDay:
                result = match_result(match, name_club)
                outcome = outcome + [result[0]] if result else outcome
                goals = goals + [result[1]] if result else goals
                goals_against = goals_against + [result[2]] if result else goals_against
            i -= 1
        
        #create the output according to the wanted data
        output = []
        output = output + [outcome] if performance else output
        output = output + [goals] if attack else output
        output = output + [goals_against] if defense else output

        return output
    
    def xStats_table(self):
        """
        Gives a list of expected statistics for each team in sorted according to the rank of the class matchday (self.matchDay).  

        Returns:
           list[list[str(int)]]: [["goals", "goals against", "points"]]
        """
        #accessing the correct webpage
        url = "https://understat.com/league/" + self.id_understat
        driver.get(url)

        #scraping the statistics of each club
        STATS = driver.find_elements(By.CLASS_NAME, "align-right.nowrap") #list of Xpaths
        stats = [STATS[i].text for i in range(len(STATS))] #list of integers

        #cleaning data: the raw information contains "+/-" depending on the (over/under)performance of a given team
        for k in range(len(stats)):
            i = 0
            while i < len(stats[k]) and  stats[k][i] != '+' and stats[k][i] != '-':
                i += 1
            stats[k] = stats[k][:i]
        xstats = [[stats[i], stats[i + 1], stats[i + 2]] for i in range(0, len(stats) - 2, 3)]
        
        return xstats
    
    def repartition(self, x, nMatch, target_outcome = "", performance = False, attack = False, defense = False):
        """
        According to a targeted statistic (goals, goals against or performance target), shows the percentage of teams 
        having less favorable outcomes than a chosen number x. 

        Example: 
        In the last 3 (nMatch) games, 85% (result) of the teams have less than 1 (x) Draw (target_outcome). (target_statistic=performance)
        In the last 5 (nMatch) games, 64% (result) of the teams have scored less than 5 (x) goals (target_statistic)

        Arguments:
            x (int): the comparison criteria 
            nMatch (integer): scope of the study (in terms of game number)
            target_outcome (character): only if the performance (win, lose, draw) is evaluated 
            target_statistic (bool): the targeted statistic in [performance, attack, defense]
        
        Returns:
           integer: percentage of teams below the comparison criteria
        """
        result = 0
        for club in self.league_table(1):
            print("Processing with " + club)
            games_data = self.form(club, nMatch, attack, defense, performance)[0]
            print(games_data)

            if target_outcome: #the targeted statistic is the outcome (draw, win or lose) 
                favorable_outcomes = 0
                for outcome in games_data:
                    if outcome == target_outcome:
                        favorable_outcomes += 1
            else : #the targeted statistic is the number of goals or goals against
                favorable_outcomes = sum(games_data)

            if favorable_outcomes <= x:
                result += 1

        return result / self.nClubs


    """Methods that can be used directly from the main file"""


    def league_table(self,matchDay):
        """
        Returns the league table of the considered matchday. 

        Arguments:
            matchDay (integer): the considered matchDay of the season 

        Returns:
            dict{string:integer}: {"club": rank}
        """
        try:
            self.result_day(matchDay)
        except ValueError as x:
            if str(x) == """There is not enough games in a season.""" :
                raise x 
            else: 
                raise ValueError("""Not enough games played yet.""")
        
        #accessing the correct webpage 
        url = "https://www.transfermarkt.com/" + self.id_transfermarkt + "/spieltagtabelle/wettbewerb/" + self.tag + "?saison_id="\
              + str(self.year) + "&spieltag=" + str(matchDay)
        driver.get(url)

        #scraping the club names in the rank order
        RANK = ["//*[@id='yw1']/table/tbody/tr[" + str(i) + "]/td[3]/a" for i in range(1, self.nClubs +1)] #list of Xpaths
        rank = [driver.find_element(By.XPATH, xpath).get_attribute("title") for xpath in RANK] #list of club names
        leaguetable = {rank[i]: i + 1 for i in range(self.nClubs)}

        return leaguetable


    def match_day(self, matchDay):
        """
        Returns all of the bills of the considered matchday. 

        Arguments:
            matchDay (integer): the considered matchDay of the season 

        Returns:
           list[string]: ["home", "away"]
        """
    
        if matchDay > (self.nClubs-2)*2 :
            raise ValueError("""There is not enough games in a season.""")
        
        #accessing the correct webpage 
        url = "https://www.transfermarkt.com/" + self.id_transfermarkt + "/spieltagtabelle/wettbewerb/" + self.tag + "?saison_id=" \
              + str(self.year) + "&spieltag=" + str(matchDay)
        driver.get(url)

        #scraping home and away team (determined with their rank) of every game of the matchday :
        HOME_TEAM = ["//*[@id='main']/main/div[2]/div[1]/div[2]/div[1]/table/tbody/tr[" + str(i) + "]/td[5]/a" for i
                     in range(1, self.nClubs+1)] #list of Xpaths
        AWAY_TEAM = ["//*[@id='main']/main/div[2]/div[1]/div[2]/div[1]/table/tbody/tr[" + str(i) + "]/td[10]/a" for i
                     in range(1, self.nClubs+1)] #list of Xpaths

        TEAMS = []
        for k in range(self.nClubs):
            TEAMS.append([HOME_TEAM[k], AWAY_TEAM[k]]) #list of [Xpath (home), Xpath (away)] with the corresponding game
        
        #Warning: the website is structured in such a way that some Xpaths are not leading to the correct information.
        #As such, a cleaning step is required after parsing every game.  
        games = [[driver.find_elements(By.XPATH,xpath1)[0].get_attribute(("title")), driver.find_elements(By.XPATH, xpath2)[0].get_attribute("title")]
                    if driver.find_elements(By.XPATH, xpath1) and driver.find_elements(By.XPATH, xpath2)
                    else None  for xpath1, xpath2 in TEAMS] #list of ["home", "away"] (corresponding with a game)
        
        #cleaning data
        while None in games: 
                games.remove(None)
        return games
    
    def result_day(self, matchDay):
        """
        Returns the scores of all the games of the considered matchday. 

        Arguments:
            matchDay (integer): the considered matchDay of the season 

        Returns:
           list[string]: ["home", "x:y", "away"]
        """

        if matchDay > (self.nClubs-2)*2 :
            raise ValueError("""There is not enough games in a season.""")
        
        games = self.match_day(matchDay)
        
        #scraping the score of each game
        GAMES = driver.find_elements(By.CLASS_NAME, "matchresult.finished") #list of Xpaths
        scores = []
        for game in GAMES:
            scores.append(game.get_attribute('innerHTML')) #list of scores "x:y"

        #associating score with the corresponding game 
        output = []
        for k in range(len(scores)):
            home , away = games[k]
            output.append([home, scores[k], away])

        if not output: 
            raise ValueError("""The match has not been played yet.""")

        return output
    



def match_result(game, name_club):
        """
        Given a club and a game, gives the result from the club's point of view or None if the club is not part of the game.

        Arguments:
            game (list[string]): ["home team", "x:y", "away team"]
            name_club (string): name of the club concerned

        Returns:
            list[string, integer, integer]: ["W/L/D", Gs , GAs]
            None
        """
        #if the club is the home team
        if name_club == game[0] :
            if game[1][0] > game[1][2] :
                return ['W', int(game[1][0]), int(game[1][2])]
            elif game[1][0] < game[1][2] :
                return ['L', int(game[1][0]), int(game[1][2])]
            else:
                return ['D', int(game[1][0]), int(game[1][2])]
            
        #if the club is the away team
        if name_club == game[2] :
            if game[1][0] < game[1][2] :
                return ['W', int(game[1][2]), int(game[1][0])]
            elif game[1][0] > game[1][2] :
                return ['L', int(game[1][2]), int(game[1][0])]
            else:
                return ['D', int(game[1][2]), int(game[1][0])]
        else: 
            return 
    

    


