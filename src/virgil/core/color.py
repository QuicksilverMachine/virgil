CSI = "\033["
OSC = "\033]"
BEL = "\a"


class Color:
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39

    @staticmethod
    def code(color: str) -> str:
        return f"{CSI}{color}m"


DEFAULT_ERROR = Color.RED
DEFAULT_SUCCESS = Color.GREEN
DEFAULT_WARNING = Color.YELLOW
DEFAULT_FOREGROUND = Color.RESET

DEFAULT_PACKAGE = Color.CYAN
DEFAULT_REQUIREMENT = Color.MAGENTA


def set_color(message: str, message_color: str, foreground_color: str) -> str:
    """Set color characters around a message
    :param message: Message string
    :param message_color: Message color
    :param foreground_color: Color that the output will be reset to
    :return: Message wrapped in color characters
    """
    return f"{Color.code(message_color)}{message}{Color.code(foreground_color)}"
