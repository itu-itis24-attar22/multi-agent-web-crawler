from html.parser import HTMLParser
from typing import List


class LinkAndTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.text_parts: list[str] = []
        self.title_parts: list[str] = []

        self._in_script = False
        self._in_style = False
        self._in_title = False

    def handle_starttag(self, tag: str, attrs) -> None:
        tag = tag.lower()

        if tag == "script":
            self._in_script = True
        elif tag == "style":
            self._in_style = True
        elif tag == "title":
            self._in_title = True
        elif tag == "a":
            for attr_name, attr_value in attrs:
                if attr_name.lower() == "href" and attr_value:
                    self.links.append(attr_value)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()

        if tag == "script":
            self._in_script = False
        elif tag == "style":
            self._in_style = False
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_script or self._in_style:
            return

        stripped = data.strip()
        if not stripped:
            return

        if self._in_title:
            self.title_parts.append(stripped)

        self.text_parts.append(stripped)


def extract_page_data(html_text: str) -> tuple[str | None, str, List[str]]:
    parser = LinkAndTextExtractor()
    parser.feed(html_text)

    title = " ".join(parser.title_parts).strip() or None
    text = " ".join(parser.text_parts).strip()
    links = parser.links

    return title, text, links