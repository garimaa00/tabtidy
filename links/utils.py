
import ipaddress
import socket
from html.parser import HTMLParser
from urllib.parse import urlparse

import requests


class PageTitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = []
        self.in_title = False
        self.og_title = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag.lower() == 'title':
            self.in_title = True

        if (
            tag.lower() == 'meta'
            and attrs.get('property', '').lower() == 'og:title'
        ):
            self.og_title = attrs.get('content', '').strip()

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == 'title':
            self.in_title = False

    def get_title(self):
        return self.og_title or ' '.join(
            ' '.join(self.title).split()
        )


def get_website_title(url):
    parsed = urlparse(url)

    if (
        parsed.scheme not in ('http', 'https')
        or not parsed.hostname
        or parsed.username
        or parsed.password
    ):
        return ''

    host = parsed.hostname

    try:
        addresses = socket.getaddrinfo(
            host, parsed.port or (443 if parsed.scheme == 'https' else 80)
        )

        for address in addresses:
            ip = ipaddress.ip_address(address[4][0])

            if not ip.is_global:
                return ''

        response = requests.get(
            url,
            timeout=5,
            allow_redirects=False,
            headers={'User-Agent': 'TabTidy/1.0'},
            stream=True,
        )

        if response.status_code != 200:
            response.close()
            return ''

        content_type = response.headers.get('Content-Type', '')

        if 'text/html' not in content_type.lower():
            response.close()
            return ''

        parser = PageTitleParser()

        try:
            for chunk in response.iter_content(
                chunk_size=2048, decode_unicode=True
            ):
                if not chunk:
                    continue

                if isinstance(chunk, bytes):
                    chunk = chunk.decode('utf-8', errors='ignore')

                parser.feed(chunk)

                if '</title>' in chunk.lower() or parser.og_title:
                    break
        finally:
            response.close()

        return parser.get_title()[:150]

    except (requests.RequestException, ValueError, OSError):
        return ''
