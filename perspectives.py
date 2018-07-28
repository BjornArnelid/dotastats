class QuantityPerspective(object):
    def filter_bans(self, bans, avg_win):
        for ban in bans:
            if ban.against_games > ban.games and ban.against_winrate < avg_win:
                yield ban

    def sort_picks(self, hero):
        return (hero.games, hero.winrate, hero.against_games, 100-hero.against_winrate)
    
    def sort_bans(self, hero):
        return (hero.against_games, 100-hero.against_winrate, -1*hero.with_games, 100-hero.with_winrate)


class WinratePerspective(object):
    def filter_bans(self, bans, avg_win):
        for ban in bans:
            if ban.against_winrate > ban.winrate and ban.against_winrate < avg_win:
                yield ban

    def sort_picks(self, hero):
        return (hero.winrate, hero.games, 100-hero.against_winrate, hero.against_games)
    
    def sort_bans(self, hero):
        return (100-hero.against_winrate, hero.against_games, 100-hero.with_winrate, -1*hero.with_games)


class DiffPerspective(object):
    def filter_bans(self, bans, avg_win):
        for ban in bans:
            if self.diff_is_worse(ban) and ban.against_winrate < avg_win:
                yield ban

    def sort_picks(self, hero):
        return (hero.diff, hero.games,-1*hero.against_diff, hero.against_games)
    
    def sort_bans(self, hero):
        return (-1*hero.against_diff, hero.against_games, -1*hero.with_diff, -1*hero.with_games)

    def diff_is_worse(self, ban):
        return (not ban.games) or ban.against_diff >= ban.diff