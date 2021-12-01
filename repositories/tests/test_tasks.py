from unittest.mock import patch

import pytest
from django.utils import timezone
from model_bakery import baker

from common.integrations import github
from repositories.models import Repository
from repositories.tasks import load_repository_commits


@pytest.fixture(name="mock_commit")
def commit_body_mock():
    """Mocking commit body

    Returns:
        dict: commit simple body
    """
    return {
        "sha": "str", "url": "http://my.commit/url",
        "commit": {
            "message": "message",
            "author": {
                "name": "author name", "date": timezone.now().isoformat()
            }
        }
    }


@pytest.mark.django_db
def test_load_repository_commits_repo_not_exists():
    """Test task error when repo doen't exists"""
    with pytest.raises(Repository.DoesNotExist):
        load_repository_commits(10, "foo")


@pytest.mark.django_db
@patch('requests.Session.request')
def test_load_repository_commits_default_params(request_mock):
    """Test load with default params

    Args:
        request_mock (Mock): Session.request mock
    """
    repository = baker.make(Repository)
    username = "foo"

    with pytest.raises(github.GitHubError):
        load_repository_commits(repository.pk, username)

    request_mock.assert_called()
    method, url = request_mock.call_args.args
    params = request_mock.call_args.kwargs.get("params")

    assert method == 'GET'
    assert url == f"{github.GitHub.BASE_URL}/repos/{username}/{repository.name}/commits"
    assert params.get("page") == 1
    assert params.get("per_page") == 100
    assert (
        timezone.datetime.now() - timezone.datetime.fromisoformat(params.get("since"))
    ).days == 30


@pytest.mark.django_db
def test_load_repository_commits_bulk_create(monkeypatch, mock_commit):
    """Test Commit model bulk_create

    Args:
        monkeypatch (fixture): pytest monkeypatch fixture
        mock_commit (dict): commit body
    """
    repository = baker.make(Repository)
    username = "foo"

    def commits_response(*args, **kwargs):
        return {"pagination": {}, "results": [mock_commit for _ in range(10)]}

    monkeypatch.setattr(github.GitHub, 'repository_commits', commits_response)

    assert load_repository_commits(repository.pk, username) == "Done!"
    assert repository.commit_set.count() == 10


@pytest.mark.django_db
def test_load_repository_commits_pagination(monkeypatch, mock_commit, celeryapp):
    """Test celery task call with pagination

    Args:
        monkeypatch (fixture): pytest monkeypatch fixture
        mock_commit (dict): commit body
        celeryapp (Celery): celery test app
    """
    repository = baker.make(Repository)
    username = "foo"

    def commits_response(*args, **kwargs):
        pagination = {"next": True} if kwargs.get("page") < 5 else {}
        return {"pagination": pagination, "results": [mock_commit for _ in range(10)]}

    monkeypatch.setattr(github.GitHub, 'repository_commits', commits_response)

    task = celeryapp.register_task(load_repository_commits)

    pipeline = task.delay(repository.pk, username).get()
    while pipeline != "Done!":
        pipeline = pipeline.get()

    assert repository.commit_set.count() == 50
