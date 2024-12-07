import contextlib
import urllib.request

from loguru import logger


@contextlib.contextmanager
def urlopen(url: str, *args, **kwargs):
    try:
        with urllib.request.urlopen(url, *args, **kwargs) as response:
            yield response
    except urllib.error.HTTPError as e:
        if "Location" not in e.headers:
            raise
        redirected_url = e.headers["Location"]
        logger.debug("Redirected from {!r} to {!r}", url, redirected_url)
        with urlopen(redirected_url, *args, **kwargs) as response:
            yield response
