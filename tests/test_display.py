
from cvauth_chess import display


def test_default_theme_is_walnut():
    config = display.default_config()

    assert config["theme"] == "walnut"
    assert config["colours"] == display.THEMES["walnut"]


def test_select_theme():
    config = display.default_config()

    display.select_theme(config, "slate")

    assert config["theme"] == "slate"
    assert config["colours"] == display.THEMES["slate"]


def test_custom_colour():
    config = display.default_config()

    display.set_custom_colour(config, "light_square", "#123456")

    assert config["theme"] == "custom"
    assert config["colours"]["light_square"] == "#123456"


def test_invalid_custom_colour():
    config = display.default_config()

    try:
        display.set_custom_colour(config, "light_square", "not-a-colour")
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_terminal_colour_conversion():
    result = display.hex_to_terminal_colour("#FFFFFF")

    assert result == 15


def test_save_and_load_custom_preferences(tmp_path, monkeypatch):
    monkeypatch.setattr(display, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(display, "CONFIG_FILE", tmp_path / "config.json")

    config = display.default_config()
    display.set_custom_colour(config, "light_square", "#123456")
    display.save_display_config(config)

    loaded = display.load_display_config()

    assert loaded["theme"] == "custom"
    assert loaded["colours"]["light_square"] == "#123456"
