import requests
import json
from perspectives import QuantityPerspective, WinratePerspective, DiffPerspective
from hero import Hero


class StatsController(object):
    def __init__(self, player_id, sample, mode, allies):
        if sample:
            attributes = '?limit=%s&' % sample
        else:
            attributes = '?'
        if mode == 'turbo':
            attributes += 'significant=0&game_mode=23'
        elif mode == 'ranked':
            attributes += 'lobby_type=7'
        elif mode == 'unranked':
            attributes += 'lobby_type=0'
        if allies:
            attributes += '&included_account_id=%s' % allies
        self.request_string = 'https://api.opendota.com/api/players/%s/heroes%s' % (player_id, attributes)

    def get_suggestions(self, sort_order):
        response = requests.get(self.request_string)
        input_data = json.loads(response.text)
        return self._parse_suggestions(input_data, sort_order)

    def _parse_suggestions(self, input_data, sort_order):
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
        win_percentage = (wins / int(games)) * 100
        picks = [h for h in picks if h.winrate > win_percentage]
        if sort_order == 'winrate':
            perspective = WinratePerspective()
        elif sort_order == 'quantity':
            perspective = QuantityPerspective()
        else:
            sort_order = 'diff'
            perspective = DiffPerspective()
        picks = sorted(picks, key=perspective.sort_picks, reverse=True)
        bans = perspective.filter_bans(bans, win_percentage)
        bans = sorted(bans, key=perspective.sort_bans, reverse=True)
        return {'avg_win': win_percentage, 'sample': games, 'picks': picks, 'bans': bans}

    def get_counter(self, hero_id, sort_order):
        response = requests.get(self.request_string + '&against_hero_id=%s' % hero_id)
        input_data = json.loads(response.text)
        return self._parse_suggestions(input_data, sort_order)
