import importlib.resources as pkg_resources
from configparser import ConfigParser
from os import getenv
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from dotenv import load_dotenv
from pydantic import BaseSettings, Field, validator
from pydantic.env_settings import SettingsSourceCallable

from isar.config.configuration_error import ConfigurationError
from isar.models.map.map_config import MapConfig
from isar.services.readers.init_map_reader import InitMapConfigReader


class Config(object):
    def __init__(self):
        load_dotenv()

        self.parser = ConfigParser()

        with pkg_resources.path("isar.config", "default.ini") as filepath:
            found_default: bool = self.parser.read(filepath)

        if not found_default:
            raise ConfigurationError(
                f"Failed to import configuration, default: {found_default}"
            )

        robot_package: str = getenv("ROBOT_PACKAGE")
        if robot_package:
            self.parser.set("DEFAULT", "robot_package", robot_package)

    def get(self, section, option):
        return self.parser.get(section, option)

    def getint(self, section, option):
        return self.parser.getint(section, option)

    def getfloat(self, section, option):
        return self.parser.getfloat(section, option)

    def getbool(self, section, option):
        return self.parser.getboolean(section, option)

    def sections(self):
        return self.parser.sections()


# config = Config().parser


def ini_config_settings(settings: BaseSettings) -> Dict[str, Any]:
    with pkg_resources.path("isar.config", "default.ini") as filepath:
        print(f"FILE: {filepath}")
        cnf = ConfigParser()

        cnf.read(filepath)

        # sections, sections_dict = cnf.sections(), {}
        # defaults, default_dict = cnf.defaults(), {}

        sections, defaults = cnf.sections(), cnf.defaults()
        config_dict: Dict = {}

        print(f"DEFFFFF:\n{sections}")

        # config_dict = defaults |

        for name, value in defaults.items():
            # default_dict[name] = value
            config_dict[name] = value

        # sections_dict["DEFAULT"] = default_dict

        for section in sections:
            options, items_dict = cnf.items(section), {}

            for name, value in options:
                # if name not in sections_dict["DEFAULT"]:
                #     items_dict[name] = value

                if name not in defaults.keys():
                    config_dict[name] = value

            # sections_dict[section] = items_dict

        # print(f"sections dict:\n{sections_dict}")
        print(f"sections dict:\n{config_dict}")

        return config_dict  # sections_dict


class IsarConfig(BaseSettings):
    """Global configuration class."""

    local_storage_path: str = "ad"
    robot_package: str = "isar_robot"

    ini_config: ConfigParser

    class Config:
        env_prefix = "isar_"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return init_settings  # , ini_config_settings, env_settings)


class GlobalConfig(BaseSettings):
    config: ConfigParser = ConfigParser()

    maap: Optional[MapConfig] = None
    # InitMapConfigReader(
    #    map_config_path=Path("maps/default_map.json")
    # ).read_map_config()

    @validator("config")
    def load_deafult_ini(cls, config):
        try:
            with pkg_resources.path("isar.config", "default.ini") as filepath:
                config.read(filepath)
        except FileNotFoundError as e:
            raise AssertionError(f"Failed to import default configuration: {e}")

        return config

    @validator("maap")
    def load_map_config(cls, maap):
        try:
            maap = InitMapConfigReader(
                map_config_path=Path("src/isar/config/maps/default_map.json")
            )
        except FileNotFoundError as e:
            raise AssertionError(f"Failed to import map config: {e}")

        return maap


global_config = GlobalConfig()

# global_config.read_ini_config()
config = global_config.config


if __name__ == "__main__":
    # a = ini_config_settings(settings=None)

    # a = IsarConfig()
    # print(a)

    """
    b = GlobalConfig()
    print(b)

    with pkg_resources.path("isar.config", "default.ini") as filepath:
        b.config.read(filepath)

    c = b.config

    d = c.getint("DEFAULT", "request_timeout")
    print(d)
    """

    a = GlobalConfig()
    print(a)

    b = a.config
    print(b)

    c = b.getint("DEFAULT", "request_timeout")
    print(c)
