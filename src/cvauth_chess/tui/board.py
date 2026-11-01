
import chess

from ..chess.game import ChessGame
from ..display import load_display_config, terminal_colours


# Use solid chess glyphs for both sides.
PIECES = {
    "K": "♚",
    "Q": "♛",
    "R": "♜",
    "B": "♝",
    "N": "♞",
    "P": "♟",
    "k": "♚",
    "q": "♛",
    "r": "♜",
    "b": "♝",
    "n": "♞",
    "p": "♟",
}

DIFFICULTIES = {
    "q": "Queen",
    "r": "Rook",
    "b": "Bishop",
    "n": "Knight",
}


def run_board(term, settings):
    """Run a local chess game in the terminal."""

    game = ChessGame()

    # The board orientation follows the player's selected colour.
    white_at_bottom = settings.player_colour == "White"

    cursor = chess.E2 if white_at_bottom else chess.E7
    selected = None
    promotion_moves = []

    # Load the player's display preferences.
    display_config = load_display_config()
    colours = terminal_colours(display_config)

    light_square = term.on_color(colours["light_square"])
    dark_square = term.on_color(colours["dark_square"])
    selected_square = term.on_color(colours["selected_square"])
    target_square = term.on_color(colours["legal_move"])
    cursor_square = term.on_color(colours["cursor"])

    white_piece_colour = term.color(colours["white_piece"])
    black_piece_colour = term.color(colours["black_piece"])

    while True:
        print(term.clear)

        board = game.board
        legal_targets = []

        if selected is not None:
            legal_targets = [
                move.to_square
                for move in game.legal_moves_from(
                    chess.square_name(selected)
                )
            ]

        # Draw the heading.
        heading = "RF CHESS  -  LOCAL GAME"
        print(term.move_yx(1, max(0, (term.width - len(heading)) // 2))
              + term.bold_cyan(heading))

        info = (
            f"You: {settings.player_colour}    "
            f"Difficulty: {settings.difficulty_name}"
        )
        print(term.move_yx(3, max(0, (term.width - len(info)) // 2))
              + info)

        # Calculate board placement.
        board_width = 36
        start_x = max(0, (term.width - board_width) // 2)
        start_y = max(5, (term.height - 15) // 2)

        # File labels above the board.
        files = "    "
        for col in range(8):
            file_index = col if white_at_bottom else 7 - col
            files += f" {chr(ord('a') + file_index)}  "

        print(term.move_yx(start_y, start_x) + term.dim(files))

        # Draw all eight ranks.
        for row in range(8):
            rank = 7 - row if white_at_bottom else row

            line = f" {rank + 1}  "

            for col in range(8):
                file_index = col if white_at_bottom else 7 - col
                square = chess.square(file_index, rank)

                piece = board.piece_at(square)
                symbol = PIECES[piece.symbol()] if piece else " "

                # Choose the square background.
                if square == cursor:
                    background = cursor_square
                elif square == selected:
                    background = selected_square
                elif square in legal_targets:
                    background = target_square
                elif (row + col) % 2 == 0:
                    background = light_square
                else:
                    background = dark_square

                # Choose the piece foreground
                if piece:
                    foreground = (
                        term.color(15)
                        if piece.color == chess.WHITE
                        else term.color(0)
                    )
                    piece_style = term.bold + foreground
                else:
                    piece_style = ""

                cell = f" {symbol}  "
                line += background + piece_style + cell + term.normal

            line += f" {rank + 1}"

            print(term.move_yx(start_y + row + 1, start_x) + line)

        # File labels below the board.
        print(term.move_yx(start_y + 9, start_x) + term.dim(files))

        # Display game status and controls.
        status = game.game_status()
        print(term.move_yx(start_y + 11, start_x) + term.bold(status))

        if promotion_moves:
            message = "Promote to: Q Queen | R Rook | B Bishop | N Knight"
        elif selected is not None:
            message = "Select a highlighted destination. Enter/Space to move."
        else:
            message = "Arrow keys: move | Enter/Space: select | U: undo"

        print(term.move_yx(start_y + 12, start_x) + message)
        print(term.move_yx(start_y + 13, start_x)
              + "R: Restart    ESC: Return to main menu")

        # Read keyboard input.
        key = term.inkey()
        key_name = key.name
        key_char = str(key).lower()

        if key_name == "KEY_ESCAPE" or key_char == "\x1b":
            return

        # Handle promotion choices.
        if promotion_moves:
            if key_char in ("q", "r", "b", "n"):
                move = next(
                    (
                        move for move in promotion_moves
                        if move.promotion == {
                            "q": chess.QUEEN,
                            "r": chess.ROOK,
                            "b": chess.BISHOP,
                            "n": chess.KNIGHT,
                        }[key_char]
                    ),
                    None,
                )

                if move:
                    game.make_move(
                        chess.square_name(move.from_square),
                        chess.square_name(move.to_square),
                        promotion=key_char,
                    )
                    selected = None
                    promotion_moves = []

            continue

        # Move the cursor around the board.
        row = 7 - chess.square_rank(cursor) if white_at_bottom else chess.square_rank(cursor)
        col = chess.square_file(cursor) if white_at_bottom else 7 - chess.square_file(cursor)

        if key_name == "KEY_UP":
            row = max(0, row - 1)
        elif key_name == "KEY_DOWN":
            row = min(7, row + 1)
        elif key_name == "KEY_LEFT":
            col = max(0, col - 1)
        elif key_name == "KEY_RIGHT":
            col = min(7, col + 1)

        if key_name in ("KEY_UP", "KEY_DOWN", "KEY_LEFT", "KEY_RIGHT"):
            file_index = col if white_at_bottom else 7 - col
            rank = 7 - row if white_at_bottom else row
            cursor = chess.square(file_index, rank)
            continue

        # Undo the previous move.
        if key_char == "u":
            game.undo()
            selected = None
            continue

        # Restart the game.
        if key_char == "r":
            game.restart()
            selected = None
            promotion_moves = []
            continue

        # Select a piece or make a move.
        if key_name in ("KEY_ENTER", "KEY_KP_ENTER") or key_char == " ":
            if selected is None:
                piece = board.piece_at(cursor)

                if piece and piece.color == board.turn:
                    moves = game.legal_moves_from(
                        chess.square_name(cursor)
                    )

                    if moves:
                        selected = cursor

            else:
                candidates = [
                    move for move in game.legal_moves_from(
                        chess.square_name(selected)
                    )
                    if move.to_square == cursor
                ]

                if candidates:
                    if any(move.promotion for move in candidates):
                        promotion_moves = candidates
                    else:
                        game.make_move(
                            chess.square_name(selected),
                            chess.square_name(cursor),
                        )
                        selected = None

                else:
                    piece = board.piece_at(cursor)

                    if piece and piece.color == board.turn:
                        moves = game.legal_moves_from(
                            chess.square_name(cursor)
                        )
                        selected = cursor if moves else None
                    else:
                        selected = None
