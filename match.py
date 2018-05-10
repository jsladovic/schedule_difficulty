from datetime import datetime

class Match:
    def add_match_data(self, tournament, date, home_team, away_team, home_score, away_score):
        self.tournament = tournament
        self.date = date
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score

    def from_dictionary(self, dictionary):
        self.tournament = dictionary['tournament']
        self.date = datetime.strptime(dictionary['date'], '%Y-%m-%dT%H:%M:%S')
        self.home_team = dictionary['home_team']
        self.away_team = dictionary['away_team']
        self.home_score = dictionary['home_score']
        self.away_score = dictionary['away_score']
        
    def to_string(self):
        return self.home_team + ' (' + str(self.home_score) + ':' + str(self.away_score) + ') ' + self.away_team

    # to be used for more detailed printing
    def __str__(self):
        return str(self.date) + ' ' + self.tournament + ' ' + self.home_team + ' (' + str(self.home_score) + ':' + str(self.away_score) + ') ' + self.away_team

    def __eq__(self, other):
        if (self is None) != (other is None):
            return False
        if self.tournament != other.tournament or self.date != other.date:
            return False
        if self.home_team != other.home_team or self.away_team != other.away_team:
            return False
        if self.home_score != other.home_score or self.away_score != other.away_score:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_home_team(self, team):
        if self.home_team == team:
            return True
        return False

    def other_team(self, team):
        if self.home_team == team:
            return self.away_team
        elif self.away_team == team:
            return self.home_team

        raise 'Team ' + team + ' doesn\'t exist in match: ' + str(match)

    def won(self, team):
        if self.home_team == team:
            if self.home_score > self.away_score:
                return True
            return False

        if self.away_score > self.home_score:
            return True
        return False

    def draw(self):
        if self.home_score == self.away_score:
            return True
        return False

    def points_for_team(self, team):
        if self.draw():
            return 1
        if self.won(team):
            return 3
        return 0
