import pytest
from my_multitool.config import ConfigManager
from my_multitool.globals import config
import pathlib


@pytest.fixture
def config_object(tmp_path: pathlib.Path) -> ConfigManager:
    config.configure(f'{tmp_path}/.my_multitool_config.yaml')
    config.set_default_config()
    config.save()
    return config
