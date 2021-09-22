import abc
from typing import List

from virgil.core.models import Requirement


class BaseParser:
    """Base parser class. Add new parsers by inheriting this class and adding
    them to parser map for use.
    """

    @staticmethod
    @abc.abstractmethod
    def parse_requirements_file(filepath: str) -> List[Requirement]:
        """Parse requirements file and return a collection of requirements"""
        raise NotImplementedError()

    @staticmethod
    @abc.abstractmethod
    def save_lock_file(requirements: List[Requirement], filepath: str) -> None:
        """Save locked requirements to a lock file"""
        raise NotImplementedError()
