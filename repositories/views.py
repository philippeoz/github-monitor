from django_filters import rest_framework as rest_filters
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Commit, Repository
from .serializers import CommitSerializer, RepositorySerializer


class RepositoryViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """
    Repository viewset, provides the create and list actions
    """
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    permission_classes = [IsAuthenticated]


class CommitViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Commit viewset, provides list action
    """
    queryset = Commit.objects.all()
    serializer_class = CommitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (rest_filters.DjangoFilterBackend,)
    filterset_fields = ('repository__name', 'author')
