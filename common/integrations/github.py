from urllib.parse import urljoin

import requests


class GitHubError(Exception):
    """Base class for exceptions in this module."""


class RepositoryNotFoundException(GitHubError):
    """Exception raised for not found on github requests"""
    def __init__(self, **kwargs):
        super().__init__(kwargs)


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
    def error_handler(response):
        """GitHub error handler method

        Args:
            response (Response): response instance

        Raises:
            GitHubError: Exception with some response description
        """
        raise GitHubError(
            f"status: {response.status_code} - content: {response.content}"
        )

    @classmethod
    def repository(cls, username, repository_name):
        """Get repository data

        Args:
            username (str): github username
            repository_name (str): github repository name

        Raises:
            RepositoryNotFoundException: when repo not found (404)
            GitHubError: With some reponse data if status os not 200 or 404

        Returns:
            dict: repository data
        """
        session = cls()
        response = session.get(f"repos/{username}/{repository_name}")

        if response.status_code == 200:
            return response.json()
        if response.status_code == 404:
            raise RepositoryNotFoundException(**response.json())

        return cls.error_handler(response)
