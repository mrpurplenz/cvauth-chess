
from dataclasses import dataclass


@dataclass(frozen=True)
class LocalGameSettings:
    """Settings selected for a local chess game."""

    player_colour: str
    difficulty_name: str
    skill_level: int


DIFFICULTIES = [
    ("Beginner", 0),
    ("Easy", 5),
    ("Medium", 10),
    ("Hard", 15),
    ("Expert", 20),
]


def run_local_setup(term):
    """Display local game options and return the selected settings.

    Returns None if the user cancels.
    """

    player_colour = "White"
    difficulty_index = 2  # Medium

    while True:
        difficulty_name, skill_level = DIFFICULTIES[difficulty_index]

        lines = [
            ("RF CHESS", "title"),
            ("LOCAL GAME SETUP", "heading"),
            ("", "normal"),
            (f"Player colour:  {player_colour}", "normal"),
            (f"Difficulty:     {difficulty_name}", "normal"),
            ("", "normal"),
            ("W / B       Select White or Black", "help"),
            ("LEFT / RIGHT Change difficulty", "help"),
            ("ENTER       Continue", "help"),
            ("ESC         Return to main menu", "help"),
        ]

        print(term.clear)

        start_y = max(0, (term.height - len(lines)) // 2)

        for i, (line, style) in enumerate(lines):
            x = max(0, (term.width - len(line)) // 2)

            if style == "title":
                line = term.bold_cyan(line)
            elif style == "heading":
                line = term.bold(line)
            elif style == "help":
                line = term.dim(line)

            print(term.move_yx(start_y + i, x) + line)

        key = term.inkey()
        key_name = key.name
        key_char = str(key).lower()

        if key_name == "KEY_ESCAPE" or key_char == "\x1b":
            return None

        elif key_char == "w":
            player_colour = "White"

        elif key_char == "b":
            player_colour = "Black"

        elif key_name == "KEY_LEFT":
            difficulty_index = max(0, difficulty_index - 1)

        elif key_name == "KEY_RIGHT":
            difficulty_index = min(
                len(DIFFICULTIES) - 1,
                difficulty_index + 1,
            )

        elif key_name in ("KEY_ENTER", "KEY_KP_ENTER") or key_char in ("\n", "\r"):
            return LocalGameSettings(
                player_colour=player_colour,
                difficulty_name=difficulty_name,
                skill_level=skill_level,
            )
