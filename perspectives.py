class QuantityPerspective(object):
    def filter_bans(self, bans, avg_win):
        for ban in bans:
            if ban.against_games > ban.games and ban.against_winrate < avg_win:
                yield ban

    def sort_picks(self, hero):
        return (hero.games, hero.winrate, hero.against_games, 100-hero.against_winrate)
    
    def sort_bans(self, hero):
        return (hero.against_games, 100-hero.against_winrate, hero.with_games, hero.with_winrate)


class WinratePerspective(object):
    def filter_bans(self, bans, avg_win):
        for ban in bans:
            if ban.against_winrate > ban.with_winrate and ban.against_winrate < avg_win:
                yield ban

    def sort_picks(self, hero):
        return (hero.winrate, hero.games, 100-hero.against_winrate, hero.against_games)
    
    def sort_bans(self, hero):
        return (100-hero.against_winrate, hero.against_games, hero.with_winrate, hero.with_games)
