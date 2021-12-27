from pathlib import Path

from isar.models.map.map_config import MapConfig
from isar.services.readers.base_reader import BaseReader
from robot_interface.models.geometry.frame import Frame


class InitMapConfigReader(BaseReader):
    def __init__(self, map_config_path: Path):
        self.map_config_path: Path = map_config_path

    def read_map_config(self) -> MapConfig:
        map_config_dict: dict = self.read_json(self.map_config_path)

        map_config: MapConfig = self.dict_to_dataclass(
            dataclass_dict=map_config_dict,
            target_dataclass=MapConfig,
            cast_config=[Frame],
        )

        return map_config
