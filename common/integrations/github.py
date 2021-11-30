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
    def response_handler(response):
        """GitHub error handler method

        Args:
            response (Response): response instance

        Raises:
            RepositoryNotFoundException: when repo not found (404)
            GitHubError: With some reponse data if status os not 200 or 404
        """
        if response.status_code == 200:
            return response
        if response.status_code == 404:
            raise RepositoryNotFoundException(**response.json())
        raise GitHubError(
            f"status: {response.status_code} - content: {response.content}"
        )

    @classmethod
    def repository(cls, username, repository_name):
        """Get repository data

        Args:
            username (str): github username
            repository_name (str): github repository name

        Returns:
            dict: repository data
        """
        response = cls().get(f"repos/{username}/{repository_name}")
        return cls.response_handler(response).json()

    @classmethod
    def repository_commits(cls, username, repository_name, **query_params):
        """
        Get repository commits list/data
        Extra args will be parsed to request url query string

        Args:
            username (str): github username
            repository_name (str): github repository name

        Returns:
            dict: repository commits list and pagination data
        """
        response = cls().get(
            f"repos/{username}/{repository_name}/commits", params=query_params
        )
        response_checked = cls.response_handler(response)
        return {
            "results": response_checked.json(),
            "pagination": response.links
        }
