
from analyzer import Analyzer
from browser import Browser
from crawler import Crawler
from match import Match

from datetime import datetime
import json

def get_teams():
    return {'Arsenal' : 142, 'Bournemouth' : 359, 'Brighton' : 381, 'Burnley' : 435, 'C Palace' : 646,
            'Chelsea' : 536, 'Everton' : 942, 'Huddersfield' : 1309, 'Leicester' : 1527, 'Liverpool' : 1563,
            'Man City' : 1718, 'Man Utd' : 1724, 'Newcastle' : 1823, 'Southampton' : 2471, 'Stoke' : 2477,
            'Swansea' : 2513, 'Tottenham' : 2590, 'Watford' : 2741, 'West Brom' : 2744, 'West Ham' : 2802}

def serialize_json(obj):
    if isinstance(obj, (datetime)):
        return obj.isoformat()
    raise TypeError ('Type %s not serializable' % type(obj))

def get_cache_filename(cache_path, team_id):
    return cache_path + str(team_id) + '.json'

def cache_matches(team_id, matches, cache_path):
    matches_json = json.dumps([ob.__dict__ for ob in matches], default=serialize_json)
    with open(get_cache_filename(cache_path, team_id), 'w') as f:
        f.write(matches_json)
        f.close

def deserialize_matches(text):
    dictionary = json.loads(text)
    matches = []
    for element in dictionary:
        match = Match()
        match.from_dictionary(element)
        matches.append(match)
    return matches

def get_cached_data(cache_path, teams):
    dictionary = {}
    for team in teams:
        f = open(get_cache_filename(cache_path, teams[team]), 'r')
        text = f.read()
        dictionary[team] = deserialize_matches(text)
        
    return dictionary

need_stats = False
cache_path = 'cache/premiership/2017-2018/'
teams = get_teams()

if need_stats:
    browser = Browser()
    crawler = Crawler()
    try:
        for team in teams:
            team_id = teams[team]
            matches = crawler.parse(browser, team_id)
            print team + ' played ' + str(len(matches)) + ' matches'
            cache_matches(team_id, matches, cache_path)
                                
    except Exception as ex:
        browser.close_browser()
        raise ex

    browser.close_browser()

competition = 'Premier League'
matches_by_team = get_cached_data(cache_path, teams)
analyzer = Analyzer(matches_by_team, competition)
#analyzer.calculate_time_between_matches(competition)
#analyzer.calculte_average_points_around_matches(2, 2)
#analyzer.calculate_expected_points_for_matches()
analyzer.calculate_schedule_difficulty()

