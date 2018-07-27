from statscontroller import pick_by_quantity, Hero, ban_by_quantity, filter_bans


sample_1 = Hero({"hero_id":"30","last_played":1532238030,"games":5,"win":2,"with_games":4,"with_win":2,"against_games":5,"against_win":4})
sample_2 = Hero({"hero_id":"21","last_played":1527111232,"games":4,"win":1,"with_games":4,"with_win":2,"against_games":11,"against_win":9})


def test_pick_by_quantity():
    assert pick_by_quantity(sample_1) == (5, 40, 5, 20)


def test_ban_by_quantity():
    assert ban_by_quantity(sample_1) == (5, 20, 4, 50)


def test_filter_bans():
    bans = filter_bans([sample_1, sample_2], 100)
    assert len(list(bans)) == 1