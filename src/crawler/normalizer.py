from urllib.parse import urljoin, urlparse, urlunparse


def normalize_url(base_url: str, candidate_url: str) -> str | None:
    """
    Resolve candidate_url relative to base_url and normalize it.

    Rules:
    - resolve relative URLs
    - keep only http/https
    - lowercase scheme and host
    - remove fragments
    - remove default ports
    - normalize empty path to '/'
    """
    if not candidate_url:
        return None

    absolute_url = urljoin(base_url, candidate_url)
    parsed = urlparse(absolute_url)

    if parsed.scheme.lower() not in {"http", "https"}:
        return None

    hostname = (parsed.hostname or "").lower()
    if not hostname:
        return None

    scheme = parsed.scheme.lower()

    port = parsed.port
    if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        netloc = hostname
    elif port is not None:
        netloc = f"{hostname}:{port}"
    else:
        netloc = hostname

    path = parsed.path or "/"

    normalized = urlunparse(
        (
            scheme,
            netloc,
            path,
            "",              # params
            parsed.query,    # keep query for now
            "",              # fragment removed
        )
    )

    return normalized