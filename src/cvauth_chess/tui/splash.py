BANNER = [
    r"        ________            _________                                  ",
    r"        \______ \_______   /   _____/__ _______ ___  __ ____   ______  ",
    r"         |    |  \_  __ \  \_____  \|  |  \__  \\  \/ // __ \ /  ___/  ",
    r"         |    `   \  | \/  /        \  |  // __ \\   /\  ___/ \___ \   ",
    r"        /_______  /__|    /_______  /____/(____  /\_/  \___  >____  >  ",
    r"                \/                \/           \/          \/     \/   ",
    r"       _____________   ____     _____          __  .__                 ",
    r"       \_   ___ \   \ /   /    /  _  \  __ ___/  |_|  |__              ",
    r"       /    \  \/\   Y   /    /  /_\  \|  |  \   __\  |  \             ",
    r"       \     \____\     /    /    |    \  |  /|  | |   Y  \            ",
    r"        \______  / \___/     \____|__  /____/ |__| |___|  /            ",
    r"               \/                    \/                 \/             ",
    r"      _________ .__                                                    ",
    r"      \_   ___ \|  |__   ____   ______ ______  _____  ______ ______    ",
    r"      /    \  \/|  |  \_/ __ \ /  ___//  ___/  \__  \ \____ \\____ \   ",
    r"      \     \___|   Y  \  ___/ \___ \ \___ \    / __ \|  |_> >  |_> >  ",
    r"       \______  /___|  /\___  >____  >____  >  (____  /   __/|   __/   ",
    r"              \/     \/     \/     \/     \/        \/|__|   |__|      "]


def draw_splash(term, start_y):
    """Draw the ASCII banner using calculated terminal coordinates."""

    height = len(BANNER)
    width = max(len(line) for line in BANNER)

    start_x = max(0, (term.width - width) // 2)

    for i, line in enumerate(BANNER):
        print(
            term.move_yx(start_y + i, start_x)
            + term.bold
            + line
            + term.normal
        )

    return start_y + height
