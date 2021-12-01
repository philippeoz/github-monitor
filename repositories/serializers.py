from rest_framework import serializers

from common.integrations import github
from repositories.tasks import load_repository_commits

from .models import Commit, Repository


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ('name',)

    def validate(self, attrs):
        """Override validate method to check if repository exists

        Args:
            attrs (dict): serializer data

        Raises:
            serializers.ValidationError: if repo not found
        """
        request = self.context.get("request")

        try:
            github.GitHub.repository(request.user.username, attrs.get("name"))
        except github.RepositoryNotFoundException as error:
            raise serializers.ValidationError("Repository not found!") from error

        return super().validate(attrs)

    def save(self, **kwargs):
        """
        Override save methdo and check if is a create then run load_commits task

        """
        create = self.instance is None
        instance = super().save(**kwargs)
        if create:
            request = self.context.get("request")
            username = request.user.username
            load_repository_commits.delay(instance.pk, username)


class CommitSerializer(serializers.ModelSerializer):
    repository = serializers.CharField(source='repository.name')

    class Meta:
        model = Commit
        fields = (
            'message',
            'sha',
            'author',
            'url',
            'avatar',
            'date',
            'repository',
        )
