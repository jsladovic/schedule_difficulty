
from __future__ import division
from datetime import datetime

class Analyzer:
    def __init__(self, matches, competition):
        self.matches_by_team = matches
        self.competition = competition
        self.point_averages = self.calculate_average_points()

    def matches_in_competition(self, team):
        return [match for match in self.matches_by_team[team] if match.tournament == self.competition]

    def calculate_schedule_difficulty(self):
        self.calculate_expected_points_for_matches()
        self.calculte_average_points_around_matches(2, 2, True)
        for team in self.matches_by_team:
            print '\n' + team
            sum_avg = 0
            for match in self.matches_by_team[team]:
                if match.tournament != self.competition:
                    continue
                print str(match) + ' -> ' + str(round(match.points_average_around_match, 2))
                sum_avg += match.points_average_around_match
            print sum_avg

    def calculate_average_points(self):
        teams = {}
        for team in self.matches_by_team:
            matches_in_competition = self.matches_in_competition(team)
            points_sum = 0
            for match in matches_in_competition:
                points_sum += match.points_for_team(team)

            teams[team] = points_sum/len(matches_in_competition)
        return teams

    def calculte_average_points_around_matches(self, past_matches, future_matches, relative = False):
        for team in self.matches_by_team:
            matches_in_competition = self.matches_in_competition(team)
            for i in range(0, len(matches_in_competition)):
                sum_for_match = 0
                count = 0
                for j in range(i - past_matches, i + future_matches + 1):
                    if j < 0 or j >= len(matches_in_competition):
                        continue
                    if relative:
                        sum_for_match += matches_in_competition[j].points_for_team(team) - matches_in_competition[j].expected_points
                    else:
                        sum_for_match += matches_in_competition[j].points_for_team(team)
                    count += 1
                if relative:
                    matches_in_competition[i].points_average_around_match = sum_for_match
                else:
                    matches_in_competition[i].points_average_around_match = sum_for_match/count

    def calculate_expected_points_for_matches(self):
        for team in self.matches_by_team:
            for match in self.matches_in_competition(team):
                match.expected_points = self.calculate_expected_points_for_match(match, team)

    def calculate_expected_points_for_match(self, match, team):
        team_average_points = self.point_averages[team]
        other_team_average_points = self.point_averages[match.other_team(team)]
        if match.is_home_team(team):
            return 3 * 2 * team_average_points / (2 * team_average_points + other_team_average_points)
        return 3 * team_average_points / (team_average_points + 2 * other_team_average_points)

    def calculate_time_between_matches(self):
        teams_rest_difference = []
        for team in self.matches_by_team:
            total_rest = 0
            opposition_total_rest = 0
            count = 0
            
            matches = self.matches_by_team[team]
            matches_in_competition = self.matches_in_competition(team)

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
