from typing import Any, Dict, List, Type

from virgil.config import Config
from virgil.core.models import Requirement
from virgil.parsers.base import BaseParser
from virgil.parsers.pip import PipParser


class Parser:
    """Class used to call set parser's methods"""

    # New parsers should be added here under configurable keys
    _parser_map: Dict[str, Type[BaseParser]] = {
        "pip": PipParser,
    }

    @staticmethod
    def parse_requirements_file(filepath: str) -> Any:
        """Run set parser's requirements file parse method"""
        parser = (
            Parser._parser_map.get(Config.parser, PipParser)
            if Config.parser is not None
            else PipParser
        )
        return parser.parse_requirements_file(filepath=filepath)

    @staticmethod
    def save_lock_file(requirements: List[Requirement], filepath: str) -> None:
        """Run set parser's lock file save method"""
        parser = (
            Parser._parser_map.get(Config.parser, PipParser)
            if Config.parser is not None
            else PipParser
        )
        parser.save_lock_file(requirements=requirements, filepath=filepath)
