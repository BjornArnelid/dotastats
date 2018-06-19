import requests
import json


class StatsController(object):
    def __init__(self):
        self.hero_data = load_hero_data()

    def get_suggestions(self, player_id):
        response = requests.get('https://api.opendota.com/api/players/%s/heroes?limit=50' % player_id)
        input_data = json.loads(response.text)
        wins = 0
        picks = []
        bans = []
        for hero in input_data:
            if hero['win'] > 0:
                wins += hero['win']
                picks.append(self.get_hero(hero))
            if hero['against_games'] > 0:
                bans.append(self.get_opponent(hero)) 
        win_percentage = (wins / 50) * 100
        picks = [h for h in picks if h['win'] > win_percentage]
        bans = [h for h in bans if h['against_win'] < win_percentage]
        bans = sorted(bans, key=lambda against: against['games'], reverse=True)
        return {'picks': picks, 'bans': bans}

    def get_hero(self, hero):
        tmp = {}
        try:
            hd = self.hero_data[hero['hero_id']]
        except KeyError:
            self.hero_data = load_hero_data()
            hd =  self.hero_data[hero['hero_id']]
        tmp['name'] = hd['localized_name']
        tmp['icon'] = get_icon_url(hd)
        tmp['games'] = hero['games']
        tmp['win'] = (hero['win'] / hero['games']) * 100
        return tmp

    def get_opponent(self, hero):
        tmp = {}
        try:
            hd = self.hero_data[hero['hero_id']]
        except KeyError:
            self.hero_data = load_hero_data()
            hd =  self.hero_data[hero['hero_id']]
        tmp['name'] = hd['localized_name']
        tmp['icon'] = get_icon_url(hd)
        tmp['games'] = hero['against_games']
        tmp['against_win'] = (hero['against_win'] / hero['against_games']) * 100
        return tmp


def load_hero_data():
    response = requests.get('https://api.opendota.com/api/heroes')
    input_data = json.loads(response.text)
    tmp_data = {}
    for data in input_data:
        tmp_data[str(data['id'])] = data
    return tmp_data

def get_icon_url(data):
    #"npc_dota_hero_antimage"
    hero = data['name'][14:]
    return 'http://cdn.dota2.com/apps/dota2/images/heroes/%s_sb.png' % hero
