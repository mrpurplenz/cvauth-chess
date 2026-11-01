from blessed import Terminal

from cvauth_chess.tui.menu import run_menu


def main():
    """RF Chess application entry point."""

    term = Terminal()

    try:
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            run_menu(term)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
