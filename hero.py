import json
import requests


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        encoded = {}
        for attr in dir(obj):
            if not attr.startswith("_"):
                encoded[attr] = getattr(obj,attr)
        return encoded


with open('heroes.json') as f:
    HERO_INFORMATION = json.load(f)


DEFAULT = {'localized_name': 'Unknown', 'name': 'unknown'}


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
            return (self.against_win / self.against_games) * 100
        except ZeroDivisionError:
            return 0

    @property
    def with_winrate(self):
        try:
            return (self.with_win / self.with_games) * 100
        except ZeroDivisionError:
            return 0

    @property
    def diff(self):
        return self.win * 2 - self.games

    @property
    def against_diff(self):
        return self.against_win * 2 - self.against_games 

    @property
    def with_diff(self):
        return self.with_win * 2 - self.with_games

    @property
    def name(self):
        hi = get_hero_from_id(self.hero_id)
        return hi['localized_name']
    
    @property
    def icon(self):
        return get_icon_url(get_hero_from_id(self.hero_id))


def get_icon_url(data):
    hero = data['name'][14:]
    return 'http://cdn.dota2.com/apps/dota2/images/heroes/%s_sb.png' % hero


def get_hero_from_id(hero_id):
    if not hero_id in HERO_INFORMATION:
        reload_hero_information()
    hi = HERO_INFORMATION.get(hero_id)
    if not hi:
        hi = DEFAULT
    return hi 


def reload_hero_information():
    response = requests.get('https://api.opendota.com/api/heroes')
    input_data = json.loads(response.text)
    for data in input_data:
        HERO_INFORMATION[str(data['id'])] = data
    with open('heroes.json',  'w') as f:
        json.dump(HERO_INFORMATION, f, cls=CustomEncoder)
