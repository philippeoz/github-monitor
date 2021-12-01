import pytest


@pytest.fixture
def celeryapp(celery_app):
    celery_app.conf.task_always_eager = True
    celery_app.conf.task_store_eager_result = True
    celery_app.conf.task_ignore_result = False
    return celery_app
