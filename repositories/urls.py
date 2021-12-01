from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommitViewSet, RepositoryViewSet

app_name = 'repositories'

router = DefaultRouter()
router.register('repositories', RepositoryViewSet)
router.register('commits', CommitViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]
