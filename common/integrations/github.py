import requests

from urllib.parse import urljoin


class GitHub(requests.Session):
    """GitHub integration"""
    BASE_URL = 'https://api.github.com'
