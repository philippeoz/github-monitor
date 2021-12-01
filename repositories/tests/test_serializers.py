from unittest.mock import MagicMock, Mock, patch

import pytest
from rest_framework.serializers import ValidationError

from common.integrations import github
from repositories import serializers


@patch('requests.Session.request')
def test_repository_validate_not_found(github_mock):
    username = "niceguy"
    repository_name = "nicerepo"
    mock_request = MagicMock(user=MagicMock(username=username))
    github_mock.side_effect = github.RepositoryNotFoundException()
    serializer = serializers.RepositorySerializer(
        data={"name": repository_name}, context={"request": mock_request}
    )
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@patch('requests.Session.request')
def test_repository_validate_is_valid(github_mock):
    username = "niceguy"
    repository_name = "nicerepo"
    mock_request = MagicMock(user=MagicMock(username=username))
    github_mock.return_value = MagicMock(
        status_code=200, json=Mock(return_value={"repo": "data"})
    )
    serializer = serializers.RepositorySerializer(
        data={"name": repository_name}, context={"request": mock_request}
    )
    assert serializer.is_valid(raise_exception=True)
