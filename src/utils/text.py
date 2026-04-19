import re


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")


def normalize_text_to_tokens(text: str) -> list[str]:
    tokens = TOKEN_PATTERN.findall(text.lower())
    return [token for token in tokens if len(token) >= 2]