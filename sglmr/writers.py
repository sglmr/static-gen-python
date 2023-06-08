import logging
from abc import ABC
from datetime import datetime
from pathlib import Path
from shutil import copytree, rmtree
from typing import List

import feedgenerator
from config import Config
from readers import Theme
from utils import meta_patterns, render_md, split_md, sub_template_tag, write_file

# Set up logger
logger = logging.getLogger(__name__)


def copy_static(content: Path, output: Path):
    """Copy static folder from content to output"""

    logger.debug("Copying static files")
    copytree(content / "static", output / "static")


def copy_images(content: Path, output: Path):
    """Copy images folder from content to output"""

    logger.debug("Copying image files")
    copytree(content / "images", output / "images")


def copy_robots_txt(output: Path, template: str):
    logger.debug("Copying robots.txt file")
    write_file(path=output / "robots.txt", text=template)


def delete_output_directory(output: Path):
    """Delete output directory"""

    logger.debug(f"Deleting '{output}'")
    if output.exists():
        rmtree(output)


def write_404_page(config: Config, theme: Theme):
    output_path = config.OUTPUT_DIR / "404.html"
    html_page = theme.four_o_four
    html_page = sub_template_tag("title", "Not Found (404)", html_page)
    write_file(path=output_path, text=html_page)


def _sitemap_url(url: str, theme: Theme) -> str:
    return sub_template_tag("url", url, theme.sitemap_url)


def write_sitemap(config: Config, theme: Theme, posts: list, pages: list):
    # Set up location for sitemap file
    output_path = config.OUTPUT_DIR / "sitemap.xml"

    # Generate all the sitemap urls
    urls_xml = _sitemap_url(url=config.SITEURL, theme=theme)
    for entry in pages:
        urls_xml += _sitemap_url(url=config.SITEURL + entry.url, theme=theme)
    for entry in posts:
        urls_xml += _sitemap_url(url=config.SITEURL + entry.url, theme=theme)

    sitemap_xml = sub_template_tag("child_template", urls_xml, theme.sitemap)
    write_file(path=output_path, text=sitemap_xml)


def write_index_page(config: Config, theme: Theme, posts: list):
    # Set up location for index file
    output_path = config.OUTPUT_DIR / "index.html"

    # Start creating the html page and fill in the title
    html_page = theme.index
    html_page = sub_template_tag("title", "Home", html_page)

    # Fill in posts list
    post_rows = str()
    for idx, post in enumerate(posts, start=-len(posts)):
        row = theme.post_row
        row = sub_template_tag("idx", -idx, row)
        row = sub_template_tag("url", post.url, row)
        row = sub_template_tag("title", post.title, row)
        row = sub_template_tag("summary", post.summary, row)
        row = sub_template_tag("pretty_date", post.pretty_date, row)
        row = sub_template_tag("post_tags_list", post.post_tags_list, row)

        post_rows += f"\n{row}"

    # Insert post rows into index page
    html_page = sub_template_tag("child_template", post_rows, html_page)

    write_file(path=output_path, text=html_page)


class BaseContent(ABC):
    def __init__(self, md_path: Path, config: Config, theme: Theme, *args, **kwargs):
        self.md_path = md_path
        self.config = config
        self.theme = theme

        self.rel_url = ""

        # Split out frontmatter from content in markdown file
        self.md_meta, self.md_content = split_md(self.md_path)

    def init_attrs(self, rel_url: str = ""):
        """
        Sets the following attributes for the class:
            rel_url, content, url, output_path

        Arguments:
            rel_url -- relative url path without surrounding slashes
        """
        self.rel_url = rel_url
        self.content = render_md(self.md_content)
        self.url = f"/{self.rel_url}/"
        self.output_path = self.config.OUTPUT_DIR / self.rel_url / "index.html"


class Post(BaseContent):
    """Class for keeping track of a post."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        logger.debug(f"Writing post {self.md_path.stem}")

        # Set up rel url
        self.init_attrs(rel_url=f"posts/{self.md_path.stem}")

        # Parse out metadata for file
        self.parse_meta_data()

        # Initialize content as the template
        self.html_page = self.theme.post

        # Replace template tags with their data from this obects attributes
        self.substitute_tags()

        # Write out markdown file to html output file
        write_file(self.output_path, self.html_page)

    @property
    def pretty_date(self):
        if hasattr(self, "date"):
            return datetime.strftime(self.date, "%m %b %Y")
        else:
            return ""

    @property
    def post_tags_list(self):
        return ", ".join([t for t in self.tags])

    def substitute_tags(self):
        for n in self.config.POST_META_FIELDS:
            v = getattr(self, n)
            self.html_page = f"{sub_template_tag(n, v, self.html_page)}"

    def parse_meta_data(self):
        s = meta_patterns["title"].search(self.md_meta)
        self.title = s.group("title").strip()
        if len(self.title) > 60:
            logger.warning(f"{self.md_path.name} title longer than 60 characters")

        s = meta_patterns["date"].search(self.md_meta)
        self.date = s.group("date").strip()
        self.date = datetime.strptime(f"{self.date}", "%Y-%m-%d")

        s = meta_patterns["tags"].search(self.md_meta)
        self.tags = [x.strip() for x in s.group("tags").split(",")]

        s = meta_patterns["summary"].search(self.md_meta)
        self.summary = s.group("summary").strip()


class Page(BaseContent):
    """Class for keeping track of a page."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        logger.debug(f"Writing page {self.md_path.stem}")

        # Set up rel url
        self.init_attrs(rel_url=f"{self.md_path.stem}")

        # Parse out metadata for file
        self.parse_meta_data()

        # Initialize content as the template
        self.html_page = self.theme.page

        # Replace template tags with their data from this obects attributes
        self.substitute_tags()

        # Write out markdown file to html output file
        write_file(self.output_path, self.html_page)

    def substitute_tags(self):
        for n in self.config.PAGE_META_FIELDS:
            v = getattr(self, n)
            self.html_page = f"{sub_template_tag(n, v, self.html_page)}"

    def parse_meta_data(self):
        s = meta_patterns["title"].search(self.md_meta)
        self.title = s.group("title").strip()
        if len(self.title) > 60:
            logger.warning(f"{self.md_path.name} title longer than 60 characters")


def write_atom_feed(config: Config, posts: List[Post]):
    # The timezone "stuff" could be significantly improved in python v3.9+
    # with the zoneinfo.ZoneInfo object

    feed = feedgenerator.Atom1Feed(
        title=config.SITENAME,
        link=config.SITEURL,
        description=config.SITE_DESCRIPTION,
        language="en",
        feed_url=f"{config.SITEURL}/atom.xml",
        author_name=config.AUTHOR,
    )

    # Add entries to the feed for each post
    for post in posts:
        post_full_url = f"{config.SITEURL}{post.url}"
        feed.add_item(
            title=post.title,
            link=post_full_url,
            description=post.summary,
            content=post.content,
            unique_id=post_full_url,
            pubdate=post.date,
        )

    with open(config.OUTPUT_DIR / "atom.xml", "w") as f:
        feed.write(f, "utf-8")
