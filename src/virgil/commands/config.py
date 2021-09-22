from virgil.config import Config
from virgil.core.printer import Printer


def config_command(_) -> None:
    """Print current configuration
    :return: None
    """
    printer = Printer()
    message = Config.to_json()
    printer.print_message(message=message)
