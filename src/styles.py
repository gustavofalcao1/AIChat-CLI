import emoji

class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    
class Format:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    SPACE = '\033[2m'

class Style:
    USER = '\033[1;96m'
    BOT = '\033[1;92m'
    WARNING = '\033[1;93m'
    ERROR = '\033[1;91m'

class Emoji:
    USER = emoji.emojize(':bust_in_silhouette:')
    BOT = emoji.emojize(':robot:')
    WARNING = emoji.emojize(':warning:')
    ERROR = emoji.emojize(':alien_monster:')