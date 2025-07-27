from carioca.game import Game


def test_game_save_load(tmp_path) -> None:
    save = tmp_path / "save.json"
    game = Game(players=2, save_path=save)
    # simulate a couple of turns
    game.play_round()  # this will also save state
    # load into a new object
    other = Game(save_path=save)
    other.load()
    assert other.current_round == game.current_round
    assert other.scores == game.scores
