import requests
import json
from perspectives import QuantityPerspective, WinratePerspective


with open('heroes.json') as f:
        HERO_INFORMATION = json.load(f)


class StatsController(object):
    def __init__(self):
        with open('heroes.json') as f:
            self.hero_data = json.load(f)

    def get_suggestions(self, player_id, sample, mode, sort_order):
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
        games = 0
        wins = 0
        picks = []
        bans = []
        for hero in input_data:
            games += hero['games']
            if hero['win'] > 0:
                wins += hero['win']
                picks.append(Hero(hero))
            if hero['against_games'] > 0:
                bans.append(Hero(hero)) 
        win_percentage = (wins / int(games)) * 100
        picks = [h for h in picks if h.winrate > win_percentage]
        if sort_order == 'winrate':
            perspective = WinratePerspective()
        else:
            perspective = QuantityPerspective()
        picks = sorted(picks, key=perspective.sort_picks, reverse=True)
        bans = perspective.filter_bans(bans, win_percentage)
        bans = sorted(bans, key=perspective.sort_bans, reverse=True)
        return {'avg_win': win_percentage, 'sample': games, 'picks': picks, 'bans': bans}


class Hero(object):
    def __init__(self, hero_stats):
        for k, v in hero_stats.items():
            setattr(self, k, v)
    
    @property
    def winrate(self):
        try:
            return (self.win / self.games) * 100
        except ZeroDivisionError:
            return 0
    
    @property
    def against_winrate(self):
        try:
            return  (self.against_win / self.against_games) * 100
        except ZeroDivisionError:
            return 0

    @property
    def with_winrate(self):
        try:
            return (self.with_win / self.with_games) * 100
        except ZeroDivisionError:
            return 0

    @property
    def name(self):
        hi = HERO_INFORMATION[self.hero_id]
        if not hi:
            reload_hero_information()
            hi = HERO_INFORMATION[self.hero_id]
        return hi['localized_name']
    
    @property
    def icon(self):
        return get_icon_url(HERO_INFORMATION[self.hero_id])


def get_icon_url(data):
    hero = data['name'][14:]
    return 'http://cdn.dota2.com/apps/dota2/images/heroes/%s_sb.png' % hero


def reload_hero_information():
    response = requests.get('https://api.opendota.com/api/heroes')
    input_data = json.loads(response.text)
    for data in input_data:
        HERO_INFORMATION[str(data['id'])] = data
    with open('heroes.json',  'w') as f:
        json.dump(HERO_INFORMATION, f)
