import pytest
from my_multitool.config import ConfigManager, ContextModel
from my_multitool.globals import config
import pathlib


@pytest.fixture
def config_object(tmp_path: pathlib.Path) -> ConfigManager:
    config.configure(f'{tmp_path}/.my_multitool_config.yaml')
    config.set_default_config()
    config.full_config.contexts.extend([
        ContextModel(name='context_01', db_string='sqlite:///:memory:/'),
        ContextModel(name='context_02', db_string='sqlite:///:memory:/'),
        ContextModel(name='context_03', db_string='sqlite:///:memory:/'),
        ContextModel(name='context_04', db_string='sqlite:///:memory:/'),
        ContextModel(name='context_05', db_string='sqlite:///:memory:/')]
    )
    config.save()
    return config
