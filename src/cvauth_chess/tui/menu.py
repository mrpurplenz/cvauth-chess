from .splash import draw_splash, BANNER
from .local_setup import run_local_setup
from .board import run_board
from .display_settings import run_display_settings

def show_message(term, title, message):
    """Display a temporary screen and wait for a keypress."""
    print(term.clear)
    print(term.center(term.bold_cyan(title)))
    print()
    print(term.center(message))
    print()
    print(term.center("Press any key to return to the main menu."))

    term.inkey()

def start_local_game(term):
    """Configure and launch a local chess game."""

    settings = run_local_setup(term)

    if settings is None:
        return

    run_board(term, settings)


def start_radio_game(term):
    show_message(
        term,
        "RADIO GAME",
        "Authenticated AX.25 chess coming soon.",
    )


def start_online_game(term):
    show_message(
        term,
        "ONLINE GAME",
        "Internet chess connectivity coming soon.",
    )


def load_saved_game(term):
    show_message(
        term,
        "LOAD SAVED GAME",
        "Saved game management coming soon.",
    )


def show_settings(term):
    """Open application display settings."""

    run_display_settings(term)


def run_menu(term):
    """Display the main menu and handle user selections."""

    while True:
        print(term.clear)

        # Calculate the complete screen layout.
        menu_lines = [
            "",
            "RF CHESS",
            "Authenticated Radio Chess",
            "",
            "MAIN MENU",
            "",
            "1. Local Game",
            "2. Radio Game",
            "3. Online Game",
            "4. Load Saved Game",
            "5. Settings",
            "",
            "Q. Quit",
            "",
            "Select an option: ",
        ]

        total_height = len(BANNER) + len(menu_lines)
        start_y = max(0, (term.height - total_height) // 2)

        # Draw the banner.
        #from .splash import draw_splash, BANNER

        y = draw_splash(term, start_y)

        # Draw the menu beneath the banner.
        for line in menu_lines:
            if line == "RF CHESS":
                line = term.bold_cyan(line)
            elif line == "MAIN MENU":
                line = term.bold(line)

            x = max(0, (term.width - len(line)) // 2)

            print(term.move_yx(y, x) + line)
            y += 1

        # Read the menu selection.
        choice = str(term.inkey()).lower()

        if choice == "1":
            start_local_game(term)
        elif choice == "2":
            start_radio_game(term)
        elif choice == "3":
            start_online_game(term)
        elif choice == "4":
            load_saved_game(term)
        elif choice == "5":
            show_settings(term)
        elif choice == "q":
            break
