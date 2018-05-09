
from analyzer import Analyzer
from browser import Browser
from crawler import Crawler
from match import Match

from datetime import datetime
import json

# Premiership
def get_teams_premier_league():
    return 'Premier League', {'Arsenal' : 142, 'Bournemouth' : 359, 'Brighton' : 381, 'Burnley' : 435,
                           'C Palace' : 646, 'Chelsea' : 536, 'Everton' : 942, 'Huddersfield' : 1309,
                           'Leicester' : 1527, 'Liverpool' : 1563, 'Man City' : 1718, 'Man Utd' : 1724,
                           'Newcastle' : 1823, 'Southampton' : 2471, 'Stoke' : 2477, 'Swansea' : 2513,
                           'Tottenham' : 2590, 'Watford' : 2741, 'West Brom' : 2744, 'West Ham' : 2802}

# Spanish La Liga
def get_teams_la_liga():
    return 'Spanish La Liga', {'Alaves' : 2975, 'Ath Bilbao' : 207, 'Atl Madrid' : 163, 'Barcelona' : 224,
                               'Celta Vigo' : 690, 'Deportivo' : 776, 'Eibar' : 889, 'Espanyol' : 927,
                               'Getafe' : 3480, 'Girona' : 4309, 'Las Palmas' : 1615, 'Leganes' : 3411,
                               'Levante' : 3251, 'Malaga' : 3069, 'Real Betis' : 2159, 'Real Madrid' : 2165,
                               'Sevilla' : 2292, 'Sociedad' : 2192, 'Valencia' : 2697, 'Villarreal' : 3123}

# Italian Serie A
def get_teams_serie_a():
    return 'Italian Serie A', {'Atalanta' : 17, 'Benevento' : 4612, 'Bologna' : 268, 'Cagliari' : 525,
                               'Chievo' : 3462, 'Crotone' : 4195, 'Fiorentina' : 999, 'Genoa' : 1082,
                               'Inter' : 1370, 'Juventus' : 1408, 'Lazio' : 1501, 'Milan' : 41, 'Napoli' : 1801,
                               'Roma' : 2163, 'Sampdoria' : 2388, 'Sassuolo' : 4692, 'Spal' : 6042,
                               'Torino' : 2584, 'Udinese' : 2634, 'Verona' : 2681}

# German Bundesliga
def get_teams_bundesliga():
    return 'German Bundesliga', {'Augsburg' : 4796, 'B Dortmund' : 398, 'B Leverkusen' : 468, 'B Munich' : 469,
                                 'Cologne' : 970, 'E Frankfurt' : 884, 'Freiburg' : 1054, 'Hamburg' : 2503,
                                 'Hannover' : 1320, 'Hertha Berlin' : 1284, 'Hoffenheim' : 3937, 'Mainz' : 3050,
                                 'Mgladbach' : 403, 'RB Leipzig' : 5709, 'Schalke' : 2260, 'Stuttgart' : 2682,
                                 'W Bremen' : 2854, 'Wolfsburg' : 2967}

# French Ligue 1
def get_teams_ligue_1():
    return 'French Ligue 1', {'Amiens' : 3149, 'Angers' : 68, 'Bordeaux' : 246, 'Caen' : 2961, 'Dijon' : 4197,
                              'Guingamp' : 1090, 'Lille' : 1576, 'Lyon' : 1645, 'Marseille' : 1748,
                              'Metz' : 1772, 'Monaco' : 1674, 'Montpellier' : 1767, 'Nantes' : 1800,
                              'Nice' : 1832, 'Paris St-G.' : 2068, 'Rennes' : 2173, 'St-Etienne' : 935,
                              'Strasbourg' : 2248, 'Toulouse' : 2591, 'Troyes' : 3051}
    
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
competition, teams = get_teams_ligue_1()
cache_path = 'cache/' + competition.replace(' ', '_') + '/2017-2018/'

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

matches_by_team = get_cached_data(cache_path, teams)
analyzer = Analyzer(matches_by_team, competition)
#analyzer.calculate_time_between_matches(competition)
#analyzer.calculte_average_points_around_matches(2, 2)
#analyzer.calculate_expected_points_for_matches()
analyzer.calculate_schedule_difficulty()

