import logging
from pathlib import Path

from config import Config
from utils import sub_template_tag

# Set up logger
logger = logging.getLogger(__name__)


def read_post_paths(posts_content: Path) -> list:
    logger.debug("Reading posts")

    post_paths = list()

    # Iterate over every post in the file
    for md_file in posts_content.glob("*.md"):
        post_paths.append(md_file)

    return post_paths


def read_page_paths(pages_content: Path) -> list:
    logger.debug("Reading pages")

    page_paths = list()

    # Iterate over every post in the file
    for md_file in pages_content.glob("*.md"):
        page_paths.append(md_file)

    return page_paths


# Templates
class Theme:
    def __init__(self, config: Config):
        self.dir = config.THEME_DIR
        self.site_url = config.SITEURL

        self.base = self.dir.joinpath("base.html").read_text()
        self.post = sub_template_tag(
            "child_template",
            self.dir.joinpath("post.html").read_text(),
            self.base,
        )

        self.page = sub_template_tag(
            "child_template",
            self.dir.joinpath("page.html").read_text(),
            self.base,
        )

        self.index = sub_template_tag(
            "child_template",
            self.dir.joinpath("index.html").read_text(),
            self.base,
        )

        self.four_o_four = sub_template_tag(
            "child_template",
            self.dir.joinpath("404.html").read_text(),
            self.base,
        )

        self.post_row = self.dir.joinpath("post_entry.html").read_text()

        self.sitemap = self.dir.joinpath("sitemap.xml").read_text()
        self.sitemap_url = self.dir.joinpath("sitemap_url.xml").read_text()

        self.robots = sub_template_tag(
            "SITEURL",
            self.site_url,
            self.dir.joinpath("robots.txt").read_text(),
        )
