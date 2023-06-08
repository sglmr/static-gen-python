import re

import pytest
import requests

sitemap_url = "https://sglmr.com/sitemap.xml"

def _get_sitemap(url:str=sitemap_url) -> requests.Response:
    return requests.get(url=url)

def _get_sitemap_links() -> list:
    _p = re.compile("(?:<loc>)(\S+)(?:<\/loc>)")
    return [p for p in _p.findall(_get_sitemap().text)]

sitemap_links = _get_sitemap_links()

@pytest.fixture
def sitemap():
    yield _get_sitemap()

# ============================================================================
#   TESTS
# ============================================================================
def test_sitemap_status_code_200(sitemap:requests.Response):
    assert sitemap.status_code == 200

@pytest.mark.skip(reason="skip longer test")
@pytest.mark.parametrize("url", sitemap_links)
def test_sitemap_links_200(url):
    r = requests.get(url=url)
    assert r.status_code == 200