import logging
import pathlib
import re
from typing import Tuple
from unicodedata import normalize

from markdown_it import MarkdownIt
from mdit_py_plugins import footnote
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

# Set up logger
logger = logging.getLogger(__name__)


def highlight_code(code, name, attrs):
    """Highlight a block of code"""

    if attrs:
        logger.info(f"Ignoring highlight attrs: {attrs}")

    try:
        lexer = get_lexer_by_name(name)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)
    except ClassNotFound as e:
        logger.error(f"No lexer found for {name}\n{e}")


# Set up markdown parser
MD_OPTIONS = {
    "highlight": highlight_code,
    "linkify": True,
    "html": True,
    "typographer": True,
}
MD = MarkdownIt(config="gfm-like", options_update=MD_OPTIONS).use(
    footnote.footnote_plugin
)


def sub_template_tag(tag: str, repl: str, string: str) -> str:
    pattern = f"{{{{\s?{tag}\s?}}}}"
    return re.sub(pattern=pattern, repl=f"{repl}", string=f"{string}")


# Re Patterns
md_split_pattern = re.compile("\A---(.|\n)*?---")

meta_patterns = {
    "title": re.compile(
        "(?:^title:\s?)(?P<title>.+)(?:$)", re.MULTILINE | re.IGNORECASE
    ),
    "date": re.compile(
        "(?:^date:\s?)(?P<date>\d{4}-\d{2}-\d{2})(?:$)", re.MULTILINE | re.IGNORECASE
    ),
    "tags": re.compile("(?:^tags:\s?)(?P<tags>.+)(?:$)", re.MULTILINE | re.IGNORECASE),
    "summary": re.compile(
        "(?:^summary:\s?)(?P<summary>.+)(?:$)", re.MULTILINE | re.IGNORECASE
    ),
}


def split_md(md_path: pathlib.Path) -> Tuple[str, str]:
    """
    Opens the markdown file and split the frontmatter with meta data and content
    into md_frontmatter and md_content attributes.

    Arguments:
        md_path -- pathlib.Path() to a markdown file

    Returns:
        Tuple containing the frontmatter and content after the md file was split.
    """
    with open(md_path, "r") as f:
        file_text = f.read()
        frontmatter = md_split_pattern.search(string=file_text).group(0)
        content = md_split_pattern.sub(repl="", string=file_text, count=1)

    return frontmatter.strip(), content.strip()


def render_md(text: str) -> str:
    """Renders markdown text into html text

    :param text: Markdown formatted text
    :type text: str
    :return: HTML text rendered from markdown
    :rtype: str
    """
    return MD.render(text)


def write_file(path: pathlib.Path, text: str):
    # Create parent directory if it doesn't exist:
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=False)

    # Write text to file
    with open(path, "w") as f:
        f.write(text)


def slugify(value):
    """
    copied from Django (django.utils.text)

    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    value = normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")
