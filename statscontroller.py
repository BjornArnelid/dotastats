import requests
import json
import flask
from perspectives import QuantityPerspective, WinratePerspective, DiffPerspective
from hero import Hero, get_hero_from_id


class StatsController(object):
    def __init__(self, player_id, args):
        if args.get('sample'):
            attributes = '?limit=%s&' % args.get('sample')
        else:
            attributes = '?'
        if args.get('mode') == 'turbo':
            attributes += 'significant=0&game_mode=23'
        elif args.get('mode') == 'ranked':
            attributes += 'lobby_type=7'
        elif args.get('mode') == 'unranked':
            attributes += 'lobby_type=0'
        if args.get('allies'):
            attributes += '&included_account_id=%s' % args.get('allies')
        self.request_string = 'https://api.opendota.com/api/players/%s/heroes%s' % (player_id, attributes)

    def get_suggestions(self, sort_order):
        response = requests.get(self.request_string)
        if response.status_code is not 200:
            flask.abort(response.status_code)
        input_data = json.loads(response.text)
        result = _parse_input_data(input_data)
        if sort_order == 'winrate':
            perspective = WinratePerspective()
        elif sort_order == 'quantity':
            perspective = QuantityPerspective()
        else:
            # sort_order = 'diff'
            perspective = DiffPerspective()
        picks = [h for h in result['picks'] if h.winrate > result['avg_win']]
        result['picks'] = sorted(picks, key=perspective.sort_picks, reverse=True)
        bans = perspective.filter_bans(result['bans'], result['avg_win'])
        result['bans'] = sorted(bans, key=perspective.sort_bans, reverse=True)
        return result

    def get_counter(self, hero_id, sort_order):
        response = requests.get(self.request_string + '&against_hero_id=%s' % hero_id)
        input_data = json.loads(response.text)
        result = _parse_input_data(input_data)
        if sort_order == 'winrate':
            perspective = WinratePerspective()
        elif sort_order == 'quantity':
            perspective = QuantityPerspective()
        else:
            # sort_order = 'diff'
            perspective = DiffPerspective()
        picks = [h for h in result['picks'] if h.winrate > result['avg_win']]
        return sorted(picks, key=perspective.sort_picks, reverse=True)

    def get_synergy(self, hero_id, sort_order):
        response = requests.get(self.request_string + '&with_hero_id=%s' % hero_id)
        input_data = json.loads(response.text)
        result = _parse_input_data(input_data)
        if sort_order == 'winrate':
            perspective = WinratePerspective()
        elif sort_order == 'quantity':
            perspective = QuantityPerspective()
        else:
            # sort_order = 'diff'
            perspective = DiffPerspective()
        picks = [h for h in result['picks'] if h.winrate > result['avg_win'] and h.hero_id != hero_id]
        return sorted(picks, key=perspective.sort_picks, reverse=True)


def _parse_input_data(input_data):
    games = 0
    wins = 0
    picks = []
    bans = []
    for hero in input_data:
        games += hero['games']
        h = Hero(hero)
        if hero['win'] > 0:
            wins += hero['win']
            picks.append(h)
        if hero['against_games'] > 0:
            bans.append(h)
    if games:
        win_percentage = (wins / games) * 100
    else:
        win_percentage = 0
    return {'avg_win': win_percentage, 'sample': games, 'picks': picks, 'bans': bans}
