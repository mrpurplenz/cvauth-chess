
import chess


class ChessGame:
    """Manage a chess game using the python-chess library."""

    def __init__(self, fen=None):
        """Create a new game, optionally from a FEN position."""

        self.board = chess.Board(fen) if fen else chess.Board()

    def legal_moves_from(self, square):
        """Return legal moves originating from a square."""

        square_index = chess.parse_square(square)
        return [
            move
            for move in self.board.legal_moves
            if move.from_square == square_index
        ]

    def make_move(self, from_square, to_square, promotion=None):
        """Make a legal move and return its SAN notation.

        Promotion should be one of: q, r, b, n.
        Raises ValueError if the move is illegal.
        """

        move = chess.Move(
            chess.parse_square(from_square),
            chess.parse_square(to_square),
            promotion=(
                chess.Piece.from_symbol(promotion).piece_type
                if promotion else None
            ),
        )

        if move not in self.board.legal_moves:
            raise ValueError(f"Illegal move: {move.uci()}")

        notation = self.board.san(move)
        self.board.push(move)

        return notation

    def undo(self):
        """Undo the previous move. Return False if there is nothing to undo."""

        if not self.board.move_stack:
            return False

        self.board.pop()
        return True

    def restart(self):
        """Restore the standard starting position."""

        self.board.reset()

    def is_game_over(self):
        """Return True if the game has ended."""

        return self.board.is_game_over(claim_draw=True)

    def game_status(self):
        """Return a human-readable description of the current position."""

        outcome = self.board.outcome(claim_draw=True)

        if outcome:
            if outcome.winner is None:
                return "Draw"
            return "White wins" if outcome.winner else "Black wins"

        if self.board.is_check():
            return (
                "White to move — Check"
                if self.board.turn == chess.WHITE
                else "Black to move — Check"
            )

        return (
            "White to move"
            if self.board.turn == chess.WHITE
            else "Black to move"
        )
