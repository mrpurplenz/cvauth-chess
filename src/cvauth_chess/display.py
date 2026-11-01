
"""Display themes and persistent colour preferences for RF Chess."""

import json
import re
from copy import deepcopy
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "cvauth-chess"
CONFIG_FILE = CONFIG_DIR / "config.json"

COLOUR_FIELDS = {
    "light_square": "Light squares",
    "dark_square": "Dark squares",
    "white_piece": "White pieces",
    "black_piece": "Black pieces",
    "selected_square": "Selected square",
    "legal_move": "Legal move",
    "cursor": "Cursor",
}

THEMES = {
    "walnut": {
        "light_square": "#A58B70",
        "dark_square": "#65503F",
        "white_piece": "#FFF5DD",
        "black_piece": "#17120F",
        "selected_square": "#E5B94F",
        "legal_move": "#668B55",
        "cursor": "#E87535",
    },
    "slate": {
        "light_square": "#9BAAB8",
        "dark_square": "#526575",
        "white_piece": "#FFFFFF",
        "black_piece": "#171D26",
        "selected_square": "#E5C45B",
        "legal_move": "#668F75",
        "cursor": "#E58A45",
    },
    "forest": {
        "light_square": "#A7B895",
        "dark_square": "#52664A",
        "white_piece": "#FFF6DC",
        "black_piece": "#182018",
        "selected_square": "#D8B957",
        "legal_move": "#789B65",
        "cursor": "#E58A45",
    },
    "monochrome": {
        "light_square": "#A6A6A6",
        "dark_square": "#555555",
        "white_piece": "#FFFFFF",
        "black_piece": "#111111",
        "selected_square": "#D6D6D6",
        "legal_move": "#777777",
        "cursor": "#BBBBBB",
    },
}

DEFAULT_THEME = "walnut"


def default_config():
    """Return a fresh copy of the default display configuration."""

    return {
        "theme": DEFAULT_THEME,
        "colours": deepcopy(THEMES[DEFAULT_THEME]),
    }


def valid_hex_colour(value):
    """Check whether a colour is a six-digit hexadecimal RGB value."""

    return isinstance(value, str) and bool(
        re.fullmatch(r"#[0-9a-fA-F]{6}", value)
    )


def load_display_config():
    """Load display preferences, falling back safely to defaults."""

    config = default_config()

    try:
        with CONFIG_FILE.open(encoding="utf-8") as file:
            saved = json.load(file)
            if not isinstance(saved, dict):
                return config
    except (OSError, json.JSONDecodeError):
        return config

    theme = saved.get("theme")
    if theme in THEMES:
        config["theme"] = theme
        config["colours"] = deepcopy(THEMES[theme])
    elif theme == "custom":
        config["theme"] = "custom"

    saved_colours = saved.get("colours", {})
    if isinstance(saved_colours, dict):
        for name in COLOUR_FIELDS:
            value = saved_colours.get(name)
            if valid_hex_colour(value):
                config["colours"][name] = value.upper()

    return config


def save_display_config(config):
    """Save display preferences, creating the configuration directory."""

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    temporary_file = CONFIG_FILE.with_suffix(".tmp")

    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)
        file.write("\n")

    temporary_file.replace(CONFIG_FILE)


def select_theme(config, theme_name):
    """Apply a built-in theme, replacing any previous custom colours."""

    if theme_name not in THEMES:
        raise ValueError(f"Unknown display theme: {theme_name}")

    config["theme"] = theme_name
    config["colours"] = deepcopy(THEMES[theme_name])


def set_custom_colour(config, name, value):
    """Set one custom colour after validating its name and value."""

    if name not in COLOUR_FIELDS:
        raise ValueError(f"Unknown display colour: {name}")

    if not valid_hex_colour(value):
        raise ValueError("Colour must be in #RRGGBB format.")

    config["colours"][name] = value.upper()
    config["theme"] = "custom"


def hex_to_rgb(value):
    """Convert #RRGGBB to an RGB tuple."""

    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def _xterm_palette():
    """Build the standard 256-colour xterm palette."""

    colours = [
        (0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0),
        (0, 0, 128), (128, 0, 128), (0, 128, 128), (192, 192, 192),
        (128, 128, 128), (255, 0, 0), (0, 255, 0), (255, 255, 0),
        (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255),
    ]

    levels = (0, 95, 135, 175, 215, 255)

    for red in levels:
        for green in levels:
            for blue in levels:
                colours.append((red, green, blue))

    for value in range(8, 239, 10):
        colours.append((value, value, value))

    return colours


XTERM_PALETTE = _xterm_palette()


def hex_to_terminal_colour(value):
    """Map an RGB colour to the nearest xterm 256-colour index."""

    red, green, blue = hex_to_rgb(value)

    return min(
        range(256),
        key=lambda index: (
            (XTERM_PALETTE[index][0] - red) ** 2
            + (XTERM_PALETTE[index][1] - green) ** 2
            + (XTERM_PALETTE[index][2] - blue) ** 2
        ),
    )


def terminal_colours(config):
    """Return the configured colours as terminal 256-colour indices."""

    return {
        name: hex_to_terminal_colour(value)
        for name, value in config["colours"].items()
    }
