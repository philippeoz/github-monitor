from rest_framework import serializers

from common.integrations import github

from .models import Commit, Repository


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ('name',)

    def validate(self, attrs):
        request = self.context.get("request")

        try:
            github.GitHub.repository(request.user.username, attrs.get("name"))
        except github.RepositoryNotFoundException as error:
            raise serializers.ValidationError("Repository not found!") from error

        return super().validate(attrs)


class CommitSerializer(serializers.ModelSerializer):
    repository = serializers.StringRelatedField(many=False)

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
