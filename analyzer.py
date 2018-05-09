
from __future__ import division
from datetime import datetime
import operator

class Analyzer:
    def __init__(self, matches, competition):
        self.matches_by_team = matches
        self.competition = competition
        self.point_averages = self.calculate_average_points()
        self.home_point_averages = self.calculate_average_points(True)
        self.away_point_averages = self.calculate_average_points(False)

        print '\nHome point averages:'
        for team in self.sort_dictionary(self.home_point_averages, True):
            print team[0] + ' -> ' + str(round(team[1], 2))

        print '\nAway point averages:'
        for team in self.sort_dictionary(self.away_point_averages, True):
            print team[0] + ' -> ' + str(round(team[1], 2))

    def matches_in_competition(self, team):
        return [match for match in self.matches_by_team[team] if match.tournament == self.competition]

    def calculate_schedule_difficulty(self):
        self.calculate_expected_points_for_matches()
        self.calculte_average_points_around_matches(2, 2, True)
        for team in self.matches_by_team:
            matches = sorted(self.matches_in_competition(team), key = lambda x: x.points_average_around_match)

            biggest_diffs = self.find_biggest_differences(matches)
            difficulty = 0
            for i in range(0, len(matches)):
                if difficulty < 4 and i > biggest_diffs[difficulty][0]:
                    difficulty += 1
                #matches[i].difficulty = difficulty + 1
                matches[i].difficulty = int(5 * (i / len(matches)) + 1)

        difficulties = []
        for team in self.matches_by_team:
            matches = self.matches_in_competition(team)
            difficulty_sum = 0
            for match in matches:
                opposition_match = [m for m in  self.matches_in_competition(match.other_team(team)) if m == match][0]
                difficulty_sum += opposition_match.difficulty
            difficulties.append((team, difficulty_sum / len(matches)))

        difficulties = self.sort_array(difficulties, True)
        for i in range(0, len(difficulties)):
            print str(i + 1) + '. ' + difficulties[i][0] + '\t\t' + str(round(difficulties[i][1], 2))

    def calculate_average_points(self, home = None):
        teams = {}
        for team in self.matches_by_team:
            matches_in_competition = self.matches_in_competition(team)
            points_sum = 0
            count = 0
            for match in matches_in_competition:
                if home == None:
                    points_sum += match.points_for_team(team)
                    count += 1
                elif match.is_home_team(team) == home:
                    points_sum += match.points_for_team(team)
                    count += 1

            teams[team] = points_sum/count
            
        return teams

    def find_biggest_differences(self, matches):
        differences = dict()
        for i in range(0, len(matches) - 1):
            differences[i] = matches[i + 1].points_average_around_match - matches[i].points_average_around_match

        biggest_diffs = sorted(differences.items(), key = operator.itemgetter(1), reverse = True)[:4]
        return sorted(biggest_diffs, key = lambda x : x[0])

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
                match.expected_points = self.calculate_expected_points_for_match_home_away(match, team)

    def calculate_expected_points_for_match(self, match, team):
        team_average_points = self.point_averages[team]
        other_team_average_points = self.point_averages[match.other_team(team)]
        if match.is_home_team(team):
            return 3 * 2 * team_average_points / (2 * team_average_points + other_team_average_points)

        return 3 * team_average_points / (team_average_points + 2 * other_team_average_points)

    def calculate_expected_points_for_match_home_away(self, match, team):
        if match.is_home_team(team):
            team_average_points = self.home_point_averages[team]
        else:
            team_average_points = self.away_point_averages[team]

        other_team = match.other_team(team)
        if match.is_home_team(other_team):
            other_team_average_points = self.home_point_averages[other_team]
        else:
            other_team_average_points = self.away_point_averages[other_team]

        return 3 * team_average_points / (team_average_points + other_team_average_points)

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

        teams_rest_difference = self.sort_array(teams_rest_difference)
        for i in range(0, len(teams_rest_difference)):
            print str(i + 1) + '. ' + teams_rest_difference[i][0] + ' rest average: ' + str(round(teams_rest_difference[i][1], 2))            

    def calculate_time_before_match_for_team(self, match, team):
        for i in range(0, len(self.matches_by_team[team])):
            if self.matches_by_team[team][i] != match:
                continue

            if i == 0:
                return None

            return (match.date.date() - self.matches_by_team[team][i - 1].date.date()).days - 1
            
    def sort_array(self, array, rev = False):
        return sorted(array, key = lambda x: x[1], reverse = rev)

    def sort_dictionary(self, dictionary, rev = False):
        return sorted(dictionary.iteritems(), key = lambda x : x[1], reverse = rev)
