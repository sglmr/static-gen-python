import logging
import time

from config import Config
from readers import Theme, read_page_paths, read_post_paths
from writers import (
    Page,
    Post,
    copy_images,
    copy_robots_txt,
    copy_static,
    delete_output_directory,
    write_404_page,
    write_atom_feed,
    write_index_page,
    write_sitemap,
)

# Set up logger
logger = logging.getLogger(__name__)
logging.getLogger("markdown_it").setLevel(logging.INFO)


def build(config=Config()):
    start_time = time.time()
    logger.info("Building static output")

    # Read templates
    theme = Theme(config)

    # Delete output directory
    delete_output_directory(config.OUTPUT_DIR)

    # Copy Static Files
    copy_images(config.CONTENT_DIR, config.OUTPUT_DIR)
    copy_static(config.CONTENT_DIR, config.OUTPUT_DIR)
    copy_robots_txt(config.OUTPUT_DIR, theme.robots)

    # Get lists of all the posts and pages
    post_paths = read_post_paths(config.POSTS_DIR)
    page_paths = read_page_paths(config.PAGES_DIR)

    # log counts of posts and pages
    logger.debug(f"Discovered {len(post_paths)} post files")
    logger.debug(f"Discovered {len(page_paths)} page files")


    """
    from concurrent.futures import ThreadPoolExecutor as ConcurrentExecutor
    with ConcurrentExecutor(2) as executor:
        posts = set(executor.map(Post, post_paths, repeat(config), repeat(theme)))
        pages = set(executor.map(Page, page_paths, repeat(config), repeat(theme)))

    """
    # Build posts
    posts = list()
    for p in post_paths:
        posts.append(Post(md_path=p, theme=theme, config=config))
    posts = sorted(posts, key=lambda x: x.date, reverse=True)  # sort posts
    

    # Build pages
    pages = list()
    for p in page_paths:
        pages.append(Page(md_path=p, theme=theme, config=config))

    # Build static template pages
    write_index_page(posts=posts, config=config, theme=theme)
    write_404_page(config, theme)
    write_sitemap(config=config, theme=theme, posts=posts, pages=pages)
    write_atom_feed(config=config, posts=posts)

    

    logger.info(f"Wrote {len(posts)} posts and {len(pages)} pages.")
    logger.info(f"Completed in {(time.time()-start_time):.3f} seconds.")
