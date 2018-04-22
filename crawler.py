from datetime import datetime
from match import Match

class Crawler:
    def __init__(self):
        self.url = 'http://www.soccerbase.com/teams/team.sd?teamTabs=results&team_id='
        self.matches_xpath = '//*[@id="tgc"]'

    def parse(self, browser, id):
        browser.get_page(self.url + str(id))
        nodes = browser.find_by_xpath(self.matches_xpath)[0].find_elements_by_tag_name('tbody')
        matches = []
        for node in nodes:
            match = self.parse_match(node)
            if match != None:
                matches.append(match)
            
        return matches
        
    def parse_match(self, node):
        nodes = node.find_elements_by_class_name('finished')
        if len(nodes) == 0:
            # match hasn't been played yet
            return None

        tournament = node.find_elements_by_class_name('tournament')[0].find_elements_by_tag_name('a')[0].get_attribute('textContent')
        date = self.parse_date(node.find_elements_by_class_name('dateTime')[0].find_elements_by_class_name('hide')[0].get_attribute('textContent'))
        home_team = node.find_elements_by_class_name('homeTeam')[0].text
        away_team = node.find_elements_by_class_name('awayTeam')[0].text
        result = node.find_elements_by_class_name('score')[0].text.split('-')
        home_score = int(result[0])
        away_score = int(result[1])

        match = Match()
        match.add_match_data(tournament, date, home_team, away_team, home_score, away_score)
        return match

    def parse_date(self, date_string):
        return datetime.strptime(date_string, '%Y-%m-%d %H:%M')

