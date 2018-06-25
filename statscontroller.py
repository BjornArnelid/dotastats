import requests
import json


class StatsController(object):
    def __init__(self):
        self.hero_data = load_hero_data()

    def get_suggestions(self, player_id, sample, mode):
        if mode == 'turbo':
            mode = '&significant=0&game_mode=23'
        elif mode == 'ranked':
            mode = '&lobby_type=7'
        elif mode == 'unranked':
            mode = '&lobby_type=0'
        else:
            mode=''
        response = requests.get('https://api.opendota.com/api/players/%s/heroes?limit=%s%s' % (player_id,sample,mode))
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
        win_percentage = (wins / int(sample)) * 100
        picks = [h for h in picks if h['win'] > win_percentage]
        bans = filter_bans(bans, picks, win_percentage)
        bans = sorted(bans, key=lambda against: against['games'], reverse=True)
        return {'avg_win': win_percentage, 'sample': sample, 'picks': picks, 'bans': bans}

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


def filter_bans(bans, picks, win):
    for ban in bans:
        if ban['against_win'] < win:
            if not_in_list(ban, picks):
                yield ban
 
 
def not_in_list(hero, hero_list):
    for other in hero_list:
        if hero['name'] == other['name']:
            return False
    return True


def load_hero_data():
    response = requests.get('https://api.opendota.com/api/heroes')
    input_data = json.loads(response.text)
    tmp_data = {}
    for data in input_data:
        tmp_data[str(data['id'])] = data
    return tmp_data

def get_icon_url(data):
    hero = data['name'][14:]
    return 'http://cdn.dota2.com/apps/dota2/images/heroes/%s_sb.png' % hero
