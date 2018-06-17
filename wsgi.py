from flask import Flask
import requests
import json
import flask


HERO_DATA = {}


application = Flask(__name__)


@application.route('/')
def hello_world():
    return 'Hello, World!'


@application.route('/picks/<player_id>')
def get_picks(player_id):
    response = requests.get('https://api.opendota.com/api/players/%s/heroes?limit=50' % player_id)
    input_data = json.loads(response.text)
    played_heroes = (hero for hero in input_data if hero['games'] > 0)
    
    pick_heroes = []
    matches_won = 0
    for hero in played_heroes:
        matches_won += hero['win']
        tmp = {}
        try:
            hd = HERO_DATA[hero['hero_id']]
        except KeyError:
            load_hero_data()
            hd = HERO_DATA[hero['hero_id']]
        tmp['name'] = hd['localized_name']
        tmp['icon'] = get_icon_url(hd)
        tmp['games'] = hero['games']
        tmp['win'] = (hero['win'] / hero['games']) * 100
        pick_heroes.append(tmp)
    win_percentage = (matches_won / 50) * 100
     
    return flask.jsonify([h for h in pick_heroes if h['win'] > win_percentage])


def load_hero_data():
    response = requests.get('https://api.opendota.com/api/heroes')
    input_data = json.loads(response.text)
    for data in input_data:
        HERO_DATA[str(data['id'])] = data


def get_icon_url(data):
    #"npc_dota_hero_antimage"
    hero = data['name'][14:]
    return 'http://cdn.dota2.com/apps/dota2/images/heroes/%s_sb.png' % hero

if __name__ == '__main__':
        application.run()
