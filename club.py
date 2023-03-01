class Club :
    def __init__(self,name,league):
        """
        Arguments:
            name (string): name used in the transfermarkt website
            league (class): class corresponding if the related league
        """
        self.league = league 
        self.name = name 


    def game(self, matchDay):
        """
        Given the matchday of the season, returns the bill.

        Arguments:
            matchDay (integer): the considered matchDay of the season

        Returns:
            list[string]: ["home", "away"]
        """
        games = self.league.match_day(matchDay)

        for game in games :
            if self.name in game :
                return game

    def game_form(self, nMatch, attack = False, defense = False, performance = False):
        """
        Returns the last club performance and its opponent performance previous the given matchday.

        Arguments:
            nMatch (integer): the number of previous games considered in order to give the past performance of a club
            attack (bool): if the attack data will be in the output
            defense (bool): if the defense data will be in the output
            performance (bool): if the performance data will be in the output
        
        Returns:
            dict{string: list[list]}: {"home": form(), "away": form()}
        """
        game = self.game(self.league.matchDay)
        home = self.league.form(game[0], nMatch, attack, defense, performance)
        away = self.league.form(game[1], nMatch, attack, defense, performance)
        gameForm = {game[0]: home, game[1]: away}

        return gameForm
    
    def club_form(self, nMatch, attack = False, defense = False, performance = False):
        """
        Returns the last club performance previous the given matchday.

        Arguments:
            nMatch (integer): the number of previous games considered in order to give the past performance of a club
            attack (bool): if the attack data will be in the output
            defense (bool): if the defense data will be in the output
            performance (bool): if the performance data will be in the output
        
        Returns:
            list[list]: form()
        """
        return self.league.form(self.name,nMatch, attack, defense, performance)
    
    def rank(self,matchDay):
        """
        Given the matchday of the season, returns the rank in the league

        Arguments:
            matchDay (integer): the considered matchDay of the season

        Returns:
            integer: rank of the season
        """
        return self.league.league_table(matchDay)[self.name]


    #confrontation between the club and its opponent


    def xstats_confrontation(self,matchDay):
        """
        Returns the xstats of the club and its opponent.
        Arguments: 
            matchDay (integer): the considered matchDay of the season
        
        Returns: 
            list[list[integer]]: [home=[goals, goals against, points], away=[goals, goals against, points]]
        """
        home, away = self.game(matchDay)
        xstats = self.league.xStats_table()
        homeRank = self.league.league_table(self.league.matchDay-1)[home]
        awayRank = self.league.league_table(self.league.matchDay-1)[away]

        return [xstats[homeRank-1],xstats[awayRank-1]]

    def rank_confrontation(self,matchDay):
        """
        Returns the rank of the club and its opponent.
        Arguments: 
            matchDay (integer): the considered matchDay of the season
        
        Returns: 
            list[integer]: [home team rank, away team rank]
        """
        home, away = self.game(matchDay)
        homeRank = self.league.league_table(self.league.matchDay-1)[home]
        awayRank = self.league.league_table(self.league.matchDay-1)[away]

        return [homeRank,awayRank]

    def form_confrontation(self, matchDay, nMatch):
        """
        Returns the form of the club and its opponent.

        Arguments: 
            matchDay (integer): the considered matchDay of the season
            nMatch (integer): the number of previous games considered in order to give the past performance of a club
        
        Returns: 
            list[list[string]]: the latest performance of the club and its opponent ("D","L","W")
        """
        home, away = self.game(matchDay)
        homeForm = self.league.form(home,nMatch)
        awayForm = self.league.form(away,nMatch)

        return [homeForm, awayForm]


    #statistical modelisation 

    #the modelisation is yet to be satisfying, therefore methods are not well detailed afterwards

    def rank_calculations(self,matchDay):

        rank = self.Vs_rank(matchDay)
        return -(rank[0]-rank[1])

    def form_calculations(self,matchDay):

        home, away = self.Vs_form(matchDay)
        homeCount, awayCount = 0 , 0
        if home[0][2] == 'D' :
            homeCount += 0.5
        if home[0][2] == 'W':
            homeCount += 2

        if home[0][1] == 'D' :
            homeCount += 1
        if home[0][1] == 'W':
            homeCount += 2.5

        if home[0][0] == 'D' :
            homeCount += 2
        if home[0][0] == 'W':
            homeCount += 3

        if away[0][2] == 'D':
            awayCount += 0.5
        if away[0][2] == 'W':
            awayCount += 2

        if away[0][1] == 'D':
            awayCount += 1
        if away[0][1] == 'W':
            awayCount += 2.5

        if away[0][0] == 'D':
            awayCount += 2
        if away[0][0] == 'W':
            awayCount += 3

        return [homeCount - awayCount , sum(home[1])-sum(away[1]), -(sum(home[2])-sum(away[2]))]

    def xstats_calculations(self,matchDay):
        homeXstats, awayXstats = self.Vs_xstats(matchDay)
        print(homeXstats,awayXstats)
        goal = float(homeXstats[0]) - float(awayXstats[0])
        goalAgainst= float(homeXstats[1]) - float(awayXstats[1])
        points = float(homeXstats[2]) - float(awayXstats[2])
        return points + goal + goalAgainst

    def result(self,matchDay):
        x = self.xstats_calculations(matchDay)
        y = self.form_calculations(matchDay)
        z = self.rank_calculations(matchDay)
        print(x, y, z)
        if abs(y[0]) <= 1 :
            return x/3 + z
        return x + 2*y[0]