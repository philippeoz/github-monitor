from unittest.mock import patch
from urllib.parse import urljoin

import pytest

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
    path = "myuser/myrepo/commits"
    github_session.get(path)

    method, url = mock_request.call_args.args

    assert mock_request.called
    assert method == 'GET'
    assert url == urljoin(github.GitHub.BASE_URL, path)
