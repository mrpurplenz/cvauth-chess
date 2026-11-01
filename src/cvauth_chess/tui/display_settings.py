
from ..display import (
    COLOUR_FIELDS,
    THEMES,
    load_display_config,
    save_display_config,
    select_theme,
    set_custom_colour,
    terminal_colours,
    valid_hex_colour,
)


def _read_hex_colour(term):
    """Read a six-digit hexadecimal colour from the keyboard."""

    value = ""

    while True:
        print(term.move_yx(term.height - 2, 2) + term.clear_eol)
        print(
            term.move_yx(term.height - 2, 2)
            + f"Enter RGB colour (#RRGGBB): #{value}"
        )

        key = term.inkey()
        key_name = key.name
        char = str(key)

        if key_name == "KEY_ESCAPE" or char == "\x1b":
            return None

        if key_name in ("KEY_ENTER", "KEY_KP_ENTER") or char in ("\n", "\r"):
            colour = "#" + value
            return colour if valid_hex_colour(colour) else None

        if key_name in ("KEY_BACKSPACE", "KEY_DELETE") or char in ("\x08", "\x7f"):
            value = value[:-1]

        #elif char.lower() in "0123456789abcdef" and len(value) < 6:
        elif len(char) == 1 and char.lower() in "0123456789abcdef" and len(value) < 6:
            value += char.upper()


def run_display_settings(term):
    """Display and edit the player's board colour preferences."""

    config = load_display_config()
    fields = list(COLOUR_FIELDS)
    selected_field = 0
    message = "Choose a theme (1-4), or select a colour and press Enter."

    theme_names = list(THEMES)

    while True:
        print(term.clear)

        title = "RF CHESS - DISPLAY SETTINGS"
        print(
            term.move_yx(1, max(0, (term.width - len(title)) // 2))
            + term.bold_cyan(title)
        )

        print(term.move_yx(3, 4) + term.bold("BOARD THEMES"))

        for index, theme in enumerate(theme_names):
            marker = "*" if config["theme"] == theme else " "
            print(
                term.move_yx(4 + index, 4)
                + f"{index + 1}. [{marker}] {theme.title()}"
            )

        if config["theme"] == "custom":
            print(term.move_yx(4 + len(theme_names), 4) + "* Custom colours")

        print(term.move_yx(10, 4) + term.bold("COLOUR SETTINGS"))

        colours = terminal_colours(config)

        for index, (name, label) in enumerate(COLOUR_FIELDS.items()):
            y = 11 + index
            marker = ">" if index == selected_field else " "

            swatch = (
                term.on_color(colours[name])
                + "      "
                + term.normal
            )

            print(
                term.move_yx(y, 4)
                + f"{marker} {label:<20} {config['colours'][name]} "
                + swatch
            )

        print(term.move_yx(20, 4) + term.dim(message))
        print(
            term.move_yx(22, 4)
            + "1-4: Theme   UP/DOWN: Select colour   ENTER: Edit colour"
        )
        print(
            term.move_yx(23, 4)
            + "S: Save   ESC: Save and return"
        )

        key = term.inkey()
        key_name = key.name
        key_char = str(key).lower()

        if key_name == "KEY_ESCAPE" or key_char == "\x1b":
            save_display_config(config)
            return

        elif key_char == "s":
            save_display_config(config)
            message = "Display preferences saved."

        elif key_char in ("1", "2", "3", "4"):
            index = int(key_char) - 1
            if index < len(theme_names):
                select_theme(config, theme_names[index])
                message = f"{theme_names[index].title()} theme selected."

        elif key_name == "KEY_UP":
            selected_field = max(0, selected_field - 1)

        elif key_name == "KEY_DOWN":
            selected_field = min(len(fields) - 1, selected_field + 1)

        elif key_name in ("KEY_ENTER", "KEY_KP_ENTER") or key_char in ("\n", "\r"):
            name = fields[selected_field]
            new_colour = _read_hex_colour(term)

            if new_colour is not None:
                set_custom_colour(config, name, new_colour)
                message = f"{COLOUR_FIELDS[name]} updated."
            else:
                message = "Invalid colour or editing cancelled."
