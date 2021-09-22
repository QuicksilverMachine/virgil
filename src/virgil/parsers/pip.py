from typing import List

from virgil.config import Config
from virgil.core.models import Requirement
from virgil.parsers.base import BaseParser


class PipParser(BaseParser):
    """Parser for pip's standard requirements files"""

    @staticmethod
    def parse_requirements_file(filepath: str) -> List[Requirement]:
        """Parse requirements file and return a collection of requirements
        :param filepath: Filepath of requirements file
        :return: Collection of requirements
        """
        with open(str(filepath), "r") as requirements_file:
            data = [
                # Remove whitespaces and newlines
                row.replace(" ", "").strip()
                # In every row
                for row in requirements_file.readlines()
                # Ignore comments, references and empty lines
                if not row.startswith("#")
                and not row.startswith("-r ")
                and not row.startswith("-c ")
                and row != "\n"
            ]

        return [Requirement.from_string(row) for row in data]

    @staticmethod
    def save_lock_file(requirements: List[Requirement], filepath: str) -> None:
        """Save locked requirements to a lock file
        :param requirements: Collection of requirements
        :param filepath: Filepath for lock file
        """
        filepath = str(filepath or Config.lock_file_path)
        with open(filepath, "w") as lock_file:
            data = [
                f"{requirement.name}=={requirement.version}\n"
                for requirement in sorted(requirements, key=lambda p: p.name)
            ]
            lock_file.writelines(data)
