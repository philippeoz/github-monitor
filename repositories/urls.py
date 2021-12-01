from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import RepositoryViewSet, CommitViewSet

app_name = 'repositories'

router = DefaultRouter()
router.register('repositories', RepositoryViewSet)
router.register('commits', CommitViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]
