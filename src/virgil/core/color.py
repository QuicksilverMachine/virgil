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


def color_code(color: int) -> str:
    csi = "\033["
    return f"{csi}{color}m"


DEFAULT_ERROR = color_code(Color.RED)
DEFAULT_SUCCESS = color_code(Color.GREEN)
DEFAULT_WARNING = color_code(Color.YELLOW)
DEFAULT_FOREGROUND = color_code(Color.RESET)

DEFAULT_PACKAGE = color_code(Color.CYAN)
DEFAULT_REQUIREMENT = color_code(Color.MAGENTA)


def set_color(message: str, message_color: str, foreground_color: str) -> str:
    """Set color characters around a message
    :param message: Message string
    :param message_color: Message color
    :param foreground_color: Color that the output will be reset to
    :return: Message wrapped in color characters
    """
    return f"{message_color}{message}{foreground_color}"
