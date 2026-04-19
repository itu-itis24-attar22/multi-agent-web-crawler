import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from src.core.config import DEFAULT_FETCH_TIMEOUT_SECONDS


USER_AGENT = "LocalCrawler/1.0"


def fetch_html(url: str, timeout: int = DEFAULT_FETCH_TIMEOUT_SECONDS) -> tuple[int | None, str | None, str | None]:
    """
    Returns:
        (http_status, content_type, html_text)

    If fetch fails or content is not HTML, html_text will be None.
    """
    request = Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urlopen(request, timeout=timeout) as response:
            status = getattr(response, "status", None)
            content_type = response.headers.get("Content-Type", "")

            if "text/html" not in content_type.lower():
                return status, content_type, None

            charset = response.headers.get_content_charset() or "utf-8"
            raw_bytes = response.read()
            html_text = raw_bytes.decode(charset, errors="replace")

            return status, content_type, html_text

    except HTTPError as e:
        return e.code, None, None
    except URLError as e:
        sys.stderr.write(f"[fetch] URLError {url}: {e.reason}\n")
        return None, None, None
    except Exception as e:
        sys.stderr.write(f"[fetch] {type(e).__name__} {url}: {e}\n")
        return None, None, None