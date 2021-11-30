from unittest.mock import patch
from urllib.parse import urljoin

import pytest
import requests

from common.integrations import github


@pytest.fixture(name="github_session")
def github_session_instance_fixture():
    """Create a instance of GitHub Session as a fixture

    Returns:
        Session: Github Session instance
    """
    return github.GitHub()


@patch('requests.Session.request')
def test_github_session_request(mock_request, github_session):
    """Test GiHub Session overridden request method

    Args:
        mock_request (Mock): Session.request mocked method
        github_session (GitHub): GitHub instance fixture
    """
    path = "myuser/myrepo/commits"
    github_session.get(path)

    method, url = mock_request.call_args.args

    assert mock_request.called
    assert method == 'GET'
    assert url == urljoin(github.GitHub.BASE_URL, path)


def test_github_repository_not_found(monkeypatch, github_session):
    """Test with mocked "not found" repository request

    Args:
        monkeypatch (MonkeyPatch): pytext monkeypatch fixture
        github_session (GitHub): GitHub instance fixture
    """

    def mock_error_response(*args, **kwargs):
        response = requests.Response()
        response.status_code = requests.status_codes.codes.get('not_found')
        setattr(
            response, "_content", requests.compat.json.dumps(
                {"message": "Not Found", "foo": "bar"}
            ).encode()
        )
        return response

    monkeypatch.setattr(requests.Session, "get", mock_error_response)

    with pytest.raises(github.RepositoryNotFoundException):
        github_session.repository("foo", "bar")


@pytest.mark.parametrize(
    'status, exception', [
        ('not_found', github.RepositoryNotFoundException),
        ('bad', github.GitHubError),
        ('service_unavailable', github.GitHubError),
    ]
)
def test_github_repository_error(status, exception, monkeypatch, github_session):
    """Test repository request with some mocked errors

    Args:
        status (str): status_code names (requests.status_codes.codes pattern)
        exception (Exception): exception to test the error handler
        monkeypatch (MonkeyPatch): pytext monkeypatch fixture
        github_session (GitHub): GitHub instance fixture
    """

    def mock_error_response(*args, **kwargs):
        response = requests.Response()
        response.status_code = requests.status_codes.codes.get(status)
        setattr(
            response, "_content", requests.compat.json.dumps(
                {"message": "Not Found", "foo": "bar"}
            ).encode()
        )
        return response

    monkeypatch.setattr(requests.Session, "get", mock_error_response)

    with pytest.raises(exception):
        github_session.repository("foo", "bar")


def test_github_repository_success(monkeypatch, github_session):
    """Test repository request with some mocked errors

    Args:
        monkeypatch (MonkeyPatch): pytext monkeypatch fixture
        github_session (GitHub): GitHub instance fixture
    """
    expected_data = {"name": "repo_name", "author": "someone"}

    def mock_error_response(*args, **kwargs):
        response = requests.Response()
        response.status_code = requests.status_codes.codes.get('ok')
        setattr(
            response, "_content", requests.compat.json.dumps(
                expected_data
            ).encode()
        )
        return response

    monkeypatch.setattr(requests.Session, "get", mock_error_response)
    assert github_session.repository("foo", "bar") == expected_data
