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
    'method, status, exception', [
        ('repository', 'not_found', github.RepositoryNotFoundException),
        ('repository', 'bad', github.GitHubError),
        ('repository', 'service_unavailable', github.GitHubError),
        ('repository_commits', 'not_found', github.RepositoryNotFoundException),
        ('repository_commits', 'bad', github.GitHubError),
        ('repository_commits', 'service_unavailable', github.GitHubError),
    ]
)
def test_github_repository_methods_errors(method, status, exception, monkeypatch, github_session):
    """Test repository request with some mocked errors

    Args:
        method (str): GitHub method to call
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
        getattr(github_session, method)("foo", "bar")


def test_github_repository_success(monkeypatch, github_session):
    """Test repository request with mocked success response

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


def test_github_repository_commits_success(monkeypatch, github_session):
    """Test repository_commits request mocked success response

    Args:
        monkeypatch (MonkeyPatch): pytext monkeypatch fixture
        github_session (GitHub): GitHub instance fixture
    """
    expected_data = [{"author": "niceguy"}, {"author": "someone"}]

    link = "http://awesome/url"
    mock_links = f"<{link}>; rel=\"next\", <{link}>; rel=\"last\""

    expected_pagination = {
        "next": {"url": "http://awesome/url", "rel": "next"},
        "last": {"url": "http://awesome/url", "rel": "last"}
    }

    def mock_error_response(*args, **kwargs):
        response = requests.Response()
        response.status_code = requests.status_codes.codes.get('ok')
        response.headers.update({"link": mock_links})
        setattr(
            response, "_content", requests.compat.json.dumps(
                expected_data
            ).encode()
        )
        return response

    monkeypatch.setattr(requests.Session, "get", mock_error_response)
    response_data = github_session.repository_commits("foo", "bar")
    assert response_data.get("results") == expected_data
    assert response_data.get("pagination") == expected_pagination
