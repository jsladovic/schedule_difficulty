
from __future__ import division
from datetime import datetime

class Analyzer:
    def __init__(self, matches):
        self.matches_by_team = matches

    def calculte_point_averages(self, competition, past_matches, future_matches):
        for team in self.matches_by_team:
            matches_in_competition = [match for match in self.matches_by_team[team] if match.tournament == competition]
            points_sum = 0
            for match in matches_in_competition:
                points_sum += match.points_for_team(team)

            print team + ' ' + str(points_sum/len(matches_in_competition))

    def calculate_time_between_matches(self, competition):
        teams_rest_difference = []
        for team in self.matches_by_team:
            total_rest = 0
            opposition_total_rest = 0
            count = 0
            
            matches = self.matches_by_team[team]
            matches_in_competition = [match for match in matches if match.tournament == competition]

            for match in matches:
                if match not in matches_in_competition:
                    continue

                rest_before_match = self.calculate_time_before_match_for_team(match, team)
                opposition_rest_before_match = self.calculate_time_before_match_for_team(match, match.other_team(team))
                if rest_before_match == None or opposition_rest_before_match == None:
                    continue

                if rest_before_match > 10 and opposition_rest_before_match > 10:
                    continue

                total_rest += rest_before_match
                opposition_total_rest += opposition_rest_before_match
                count += 1

            team_average_rest = total_rest/count
            opposition_average_rest = opposition_total_rest/count
            teams_rest_difference.append((team, team_average_rest - opposition_average_rest))

        teams_rest_difference = self.sort(teams_rest_difference)
        for i in range(0, len(teams_rest_difference)):
            print str(i + 1) + '. ' + teams_rest_difference[i][0] + ' rest average: ' + str(round(teams_rest_difference[i][1], 2))            

    def calculate_time_before_match_for_team(self, match, team):
        for i in range(0, len(self.matches_by_team[team])):
            if self.matches_by_team[team][i] != match:
                continue

            if i == 0:
                return None

            return (match.date.date() - self.matches_by_team[team][i - 1].date.date()).days - 1
            
    def sort(self, array):
        return sorted(array, key = lambda x: x[1])
