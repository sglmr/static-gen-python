from pathlib import Path

import pytest

from sglmr.config import Config

from .conftest import config_attrs


def test_default_config_base_dir():
    c = Config()
    assert c.BASE_DIR == Path.cwd()

@pytest.mark.parametrize("a", config_attrs())
def test_default_config_attrs(default_config, a):
    assert hasattr(default_config, a), f"Default config missing attr {a}"


def test_test_config_base_dir(config):
    assert "/tests" in f"{config.BASE_DIR}"