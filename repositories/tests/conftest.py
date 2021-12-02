import pytest
from rest_framework.test import APIClient


@pytest.fixture
def celeryapp(celery_app):
    """
    CeleryApp test fixture to run celery_worker without a broker

    Args:
        celery_app (fixture): pytest-celery fixture

    Returns:
        fixture: celery app instance with some test settings
    """
    celery_app.conf.task_always_eager = True
    celery_app.conf.task_store_eager_result = True
    celery_app.conf.task_ignore_result = False
    return celery_app


@pytest.fixture
def api_client():
    """DRF client"""
    return APIClient()
