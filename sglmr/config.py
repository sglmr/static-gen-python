from os import getenv
from pathlib import Path


class Config:
    def __init__(self, **kwargs):
        # SITE URL
        if "SITEURL" in kwargs:
            self.SITEURL = kwargs.pop("SITEURL")
        elif getenv("SITEURL"):
            self.SITEURL = getenv("SITEURL", None)
        elif getenv("CF_PAGES_URL"):
            self.SITEURL = getenv("CF_PAGES_URL", None)
        else:
            self.SITEURL = "sglmr.com"

        self.BASE_DIR = kwargs.pop("BASE_DIR", Path.cwd())
        self.AUTHOR = kwargs.pop("AUTHOR", getenv("AUTHOR", "Stephen Gilmore"))
        self.SITENAME = kwargs.pop("SITENAME", getenv("SITENAME", self.SITEURL))
        self.SITE_DESCRIPTION = kwargs.pop(
            "SITE_DESCRIPTION", getenv("SITE_DESCRIPTION", "")
        )

        # Content & Output
        self.CONTENT_DIR = kwargs.pop("CONTENT_DIR", self.BASE_DIR / "content")
        self.OUTPUT_DIR = kwargs.pop("OUTPUT_DIR", self.BASE_DIR / "output")

        # Sub dirs
        self.PAGES_DIR = kwargs.pop("PAGES_DIR", self.CONTENT_DIR / "pages")
        self.POSTS_DIR = kwargs.pop("POSTS_DIR", self.CONTENT_DIR / "posts")
        self.THEME_DIR = kwargs.pop("THEME_DIR", self.CONTENT_DIR / "theme")

        # Meta fields
        self.PAGE_META_FIELDS = ("title", "content")
        self.POST_META_FIELDS = (
            "title",
            "content",
            "summary",
            "pretty_date",
            "post_tags_list",
        )

        for k, v in kwargs.items():
            if k.upper() == k:
                setattr(self, k, v)
