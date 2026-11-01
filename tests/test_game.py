
import chess
import pytest

from cvauth_chess.chess.game import ChessGame


def test_new_game_starts_in_standard_position():
    game = ChessGame()

    assert game.board.fen() == chess.Board().fen()
    assert game.board.turn == chess.WHITE


def test_legal_moves_from_starting_position():
    game = ChessGame()

    moves = game.legal_moves_from("e2")

    assert len(moves) == 2
    assert {move.uci() for move in moves} == {"e2e3", "e2e4"}


def test_make_legal_move():
    game = ChessGame()

    notation = game.make_move("e2", "e4")

    assert notation == "e4"
    assert game.board.piece_at(chess.E4) == chess.Piece(
        chess.PAWN, chess.WHITE
    )
    assert game.board.turn == chess.BLACK


def test_illegal_move_is_rejected():
    game = ChessGame()

    with pytest.raises(ValueError):
        game.make_move("e2", "e5")


def test_undo_move():
    game = ChessGame()
    original_fen = game.board.fen()

    game.make_move("e2", "e4")

    assert game.undo()
    assert game.board.fen() == original_fen


def test_undo_empty_game():
    game = ChessGame()

    assert not game.undo()


def test_restart():
    game = ChessGame()
    game.make_move("e2", "e4")
    game.restart()

    assert game.board.fen() == chess.Board().fen()


def test_check_detection():
    game = ChessGame("4k3/8/8/8/8/8/4R3/4K3 b - - 0 1")

    assert "Check" in game.game_status()
