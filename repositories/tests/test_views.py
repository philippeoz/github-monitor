from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework import status

from repositories.models import Commit, Repository


@pytest.mark.parametrize(
    "method, path", [
        ("get", "/api/repositories/"),
        ("post", "/api/repositories/"),
        ("put", "/api/repositories/"),
        ("patch", "/api/repositories/"),
        ("get", "/api/commits/"),
        ("post", "/api/commits/"),
        ("put", "/api/commits/"),
        ("patch", "/api/commits/"),
    ]
)
def test_unauthenticated_requests(method, path, api_client):
    """Test unauthenticated requests

    Args:
        api_client (APIClient): DRF APIClient fixture
    """
    response = getattr(api_client, method)(path, json={"cool": "data"})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize(
    "method, path", [
        ("put", "/api/repositories/"),
        ("patch", "/api/repositories/"),
        ("post", "/api/commits/"),
        ("put", "/api/commits/"),
        ("patch", "/api/commits/"),
    ]
)
def test_mothod_not_allowed(method, path, api_client):
    """Resring not allowed/not implemented paths"""
    user = baker.make(get_user_model())
    api_client.force_authenticate(user=user)
    response = getattr(api_client, method)(path, json={"cool": "data"})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_commit_list_request(api_client):
    """Testing commits list request without filtering"""
    user = baker.make(get_user_model())
    api_client.force_authenticate(user=user)
    commits = baker.make(Commit, _quantity=15)
    response = api_client.get("/api/commits/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get("results")) == 10
    assert response.json().get("count") == 15
    assert not [
        co.get("sha") for co in response.json().get("results") if co.get("sha") not in [
            commit.sha for commit in commits
        ]
    ]


@pytest.mark.django_db
def test_commit_list_request_filter(api_client):
    """Test commits filteting with url querystring"""
    user = baker.make(get_user_model())
    api_client.force_authenticate(user=user)
    baker.make(Commit, _quantity=13, author="niceguy")
    baker.make(Commit, _quantity=5, repository=baker.make(Repository, name="dosdahora"))
    baker.make(
        Commit, _quantity=9,
        repository=baker.make(Repository, name="dosdahora"),
        author="niceguy"
    )
    assert api_client.get(
        "/api/commits/?author=niceguy").json().get("count") == 22
    assert api_client.get(
        "/api/commits/?repository__name=dosdahora").json().get("count") == 14
    assert api_client.get(
        "/api/commits/?repository__name=dosdahora&author=niceguy"
    ).json().get("count") == 9


@pytest.mark.django_db
def test_repository_list_request(api_client):
    """Test repository list request"""
    user = baker.make(get_user_model())
    api_client.force_authenticate(user=user)
    baker.make(Repository, _quantity=16)
    response = api_client.get("/api/repositories/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json().get("results")) == 10
    assert response.json().get("count") == 16


@pytest.mark.django_db
@patch("requests.Session.request")
def test_repository_not_found_error(request_mock, api_client):
    """Testing repository not found error

    Args:
        request_mock (Mock): Mockinf github response
        api_client (APIClient): DRF test client
    """
    user = baker.make(get_user_model())
    api_client.force_authenticate(user=user)
    request_mock.return_value = MagicMock(
        status_code=404,
        json=MagicMock(return_value={"message": "error"})
    )
    response = api_client.post(
        "/api/repositories/",
        {"name": "odahora"}, format="json"
    )
    assert response.status_code == 400
    assert "non_field_errors" in response.json().keys()
    assert response.json()["non_field_errors"] == ["Repository not found!"]


@patch("requests.Session.request")
@patch("repositories.tasks.load_repository_commits.delay")
@pytest.mark.django_db
def test_repository_create_request(mock_load, request_mock, api_client):
    """Testing repository creation endpoint

    Args:
        mock_load (Mock): Mocking celery delay
        request_mock (Mock): Mocking github integration request
        api_client (APIClient): DRF test client
    """
    user = baker.make(get_user_model())
    api_client.force_authenticate(user=user)

    request_mock.return_value = MagicMock(
        status_code=200,
        json=MagicMock(return_value={"repo": "data"})
    )

    repository = baker.prepare(Repository, name="vrau")
    response = api_client.post(
        "/api/repositories/", {"name": repository.name}, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("name") == repository.name

    repository = Repository.objects.get(name="vrau")
    mock_load.assert_called()
    mock_load.assert_called_with(repository.pk, user.username)
