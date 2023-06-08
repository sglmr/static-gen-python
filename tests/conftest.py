from pathlib import Path

import pytest

from sglmr.config import Config


def config_attrs():
    return ["BASE_DIR", "SITEURL", "CONTENT_DIR", "OUTPUT_DIR", "PAGES_DIR","POSTS_DIR","THEME_DIR","POST_META_FIELDS","PAGE_META_FIELDS",]

@pytest.fixture
def default_config() -> Config:
    yield Config()

@pytest.fixture
def config() -> Config:
    c = Config(
        BASE_DIR = Path.cwd() / "tests",
    ) 
    yield c