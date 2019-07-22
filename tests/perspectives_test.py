from perspectives import QuantityPerspective, WinratePerspective, DiffPerspective
from hero import Hero


sample_1 = Hero({"hero_id":"30","last_played":1532238030,"games":5,"win":2,"with_games":4,"with_win":2,"against_games":5,"against_win":4})
sample_2 = Hero({"hero_id":"21","last_played":1527111232,"games":4,"win":1,"with_games":4,"with_win":2,"against_games":11,"against_win":9})
sample_3 = Hero({"hero_id":"5","last_played":1563310176,"games":6,"win":6,"with_games":2,"with_win":1,"against_games":7,"against_win":1})


def test_pick_by_quantity():
    perspective = QuantityPerspective()
    assert perspective.sort_picks(sample_1) == (5, 40, 5, 20)


def test_ban_by_quantity():
    perspective = QuantityPerspective()
    assert perspective.sort_bans(sample_1) == (5, 20, -4, 50)


def test_filter_by_quantity():
    perspective = QuantityPerspective()
    bans = perspective.filter_bans([sample_1, sample_2], 100)
    assert len(list(bans)) == 1


def test_pick_by_winrate():
    perspective = WinratePerspective()
    assert perspective.sort_picks(sample_1) == (40, 5, 20, 5)


def test_ban_by_winrate():
    perspective = WinratePerspective()
    assert perspective.sort_bans(sample_1) == (20, 5, 50, -4)


def test_filter_by_winrate():
    perspective = WinratePerspective()
    bans = perspective.filter_bans([sample_1, sample_2], 100)
    assert len(list(bans)) == 2


def test_pick_by_diff():
    perspective = DiffPerspective()
    assert perspective.sort_picks(sample_1) == (-1, 5, -3, 5)


def test_ban_by_diff():
    perspective = DiffPerspective()
    assert perspective.sort_bans(sample_1) == (-3, 5, 0, -4)


def test_filter_by_diff():
    perspective = DiffPerspective()
    bans = perspective.filter_bans([sample_1, sample_2, sample_3], 100)
    assert not list(bans)