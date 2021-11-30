from urllib.parse import urljoin

import requests


class GitHub(requests.Session):
    """GitHub integration"""
    BASE_URL = 'https://api.github.com'

    def __init__(self):
        """Init override to update default_headers"""
        super().__init__()
        self.headers.update({"Accept": "application/vnd.github.v3+json"})

    def request(self, method, path, **kwargs):
        """Override request method to accept the url path"""
        return super().request(
            method, urljoin(GitHub.BASE_URL, path), **kwargs
        )

    @staticmethod
    def repository():
        pass
