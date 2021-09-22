import json
import os
from collections import OrderedDict
from configparser import ConfigParser
from copy import deepcopy
from typing import Any, List


class Config:
    PARENT_DIR = os.path.abspath(os.getcwd())
    CONFIG_FILE = os.path.join(PARENT_DIR, "setup.cfg")

    SECTION = "virgil"

    DEFAULT_PARSER = "pip"
    DEFAULT_ANY_VERSION = "Any"
    DEFAULT_CHECKS: List[str] = []
    DEFAULT_IGNORE_LIST = [
        "virgil",
        "pip",
        "setuptools",
        "wheel",
    ]

    DEFAULT_REQUIREMENTS_FILE_PATH = "requirements.txt"
    DEFAULT_LOCK_FILE_PATH = "requirements.lock"

    DEFAULT_REQUIREMENTS_FILES = ["requirements.txt"]
    DEFAULT_LOCK_FILES = ["requirements.lock"]

    parser = DEFAULT_PARSER
    any_version = DEFAULT_ANY_VERSION
    checks = DEFAULT_CHECKS
    ignore_list = DEFAULT_IGNORE_LIST
    requirements_files = DEFAULT_REQUIREMENTS_FILES
    lock_files = DEFAULT_LOCK_FILES
    lock_file_path = DEFAULT_LOCK_FILE_PATH

    def __getattribute__(self, item: Any) -> Any:
        """Return a copy of the attribute if that attribute is a list or a dict
        :param item: Requested attribute
        :return: Attribute or copy of that attribute
        """
        if isinstance(item, list) or isinstance(item, dict):
            return deepcopy(item)

        return item

    @staticmethod
    def absolute_path(file_path: str) -> str:
        """Get absolute path for a file
        :param file_path: Relative filepath
        :return: Absolute path string
        """
        return os.path.join(Config.PARENT_DIR, file_path)

    @classmethod
    def initialize(cls) -> None:
        """Read and set configuration from file
        :return: None
        """
        if not os.path.exists(cls.CONFIG_FILE):
            # If config file does not exist use default config
            return

        parser = ConfigParser()
        parser.read(cls.CONFIG_FILE)

        if parser.has_section(cls.SECTION):
            cls.any_version = cls.get_option(parser, cls.SECTION, "any_version", cls.any_version)
            cls.checks = cls.get_list(parser, cls.SECTION, "checks", cls.checks)
            cls.ignore_list = cls.get_list(parser, cls.SECTION, "ignore_list", cls.ignore_list)
            cls.lock_file_path = cls.get_option(
                parser, cls.SECTION, "lock_file_path", cls.lock_file_path
            )
            cls.requirements_files = [
                cls.absolute_path(file_)
                for file_ in cls.get_list(
                    parser, cls.SECTION, "requirements_files", cls.requirements_files
                )
            ]
            cls.lock_files = [
                cls.absolute_path(file_)
                for file_ in cls.get_list(parser, cls.SECTION, "lock_files", cls.lock_files)
            ]

    @staticmethod
    def get_option(parser: ConfigParser, section: str, option: str, default: Any) -> Any:
        """Get option from parser
        :param parser: Option parser
        :param section: Option section in config file
        :param option: Option name
        :param default: Default value for option
        :return: Option value
        """
        return parser.get(section, option) if parser.has_option(section, option) else default

    @staticmethod
    def get_list(parser: ConfigParser, section: str, option: str, default: Any) -> Any:
        """Get option from parser in list format
        :param parser: Option parser
        :param section: Option section in config file
        :param option: Option name
        :param default: Default value for option
        :return: Option value
        """
        result = Config.get_option(parser, section, option, default)
        try:
            if isinstance(result, str):
                return [item for item in result.split("\n") if item]
            if isinstance(result, list):
                return result
            return default
        except ValueError:
            return default

    @classmethod
    def to_json(cls) -> str:
        """Return options in json format
        :return: json string with options as keys
        """
        return json.dumps(
            OrderedDict(
                (
                    (
                        "virgil",
                        OrderedDict(
                            (
                                ("any_version", cls.any_version),
                                ("checks", cls.checks),
                                ("ignore_list", cls.ignore_list),
                                ("lock_file_path", cls.lock_file_path),
                                ("requirements_files", cls.requirements_files),
                                ("lock_files", cls.lock_files),
                            )
                        ),
                    ),
                )
            ),
            indent=4,
        )
