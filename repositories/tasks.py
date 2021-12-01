from django.utils import timezone

from common.integrations import github
from githubmonitor.celery import app
from repositories.models import Commit, Repository


@app.task(
    autoretry_for=(github.GitHubError,),
    retry_kwargs={'max_retries': 5, 'countdown': 5})
def load_repository_commits(repository_pk, username, **kwargs):
    """
    Recursive load commits task.
    While a next page exists, this task will schedule another request.

    Args:
        repository_pk (int): Repository pk
        username (str): github username

    Returns:
        str: just "Done!"
    """

    page = kwargs.get("page", 1)
    per_page = kwargs.get("per_page", 100)
    since = kwargs.get(
        "since", (
            timezone.datetime.now() - timezone.timedelta(days=30)
        ).isoformat()
    )

    repository_instance = Repository.objects.get(pk=repository_pk)

    page_data = github.GitHub.repository_commits(
        username, repository_instance.name,
        since=since, page=page, per_page=per_page
    )

    def parse_avatar_url(data, name):
        default_url = f"https://ui-avatars.com/api/?name={name}"
        return data.get("avatar_url") if data else default_url

    repository_instance.commit_set.bulk_create(
        [
            Commit(
                repository=repository_instance,
                message=commit.get("commit").get("message"),
                sha=commit.get("sha"),
                author=commit.get("commit").get("author").get("name"),
                url=commit.get("url"),
                date=timezone.make_aware(
                    timezone.datetime.fromisoformat(
                        commit.get("commit").get("author").get("date")[:19]
                    )
                ),
                avatar=parse_avatar_url(
                    commit.get("author"),
                    commit.get("commit").get("author").get("name")
                )
            ) for commit in page_data.get("results")
        ]
    )

    if "next" not in page_data.get("pagination").keys():
        return 'Done!'

    return load_repository_commits.delay(
        repository_pk, username, page=page + 1, since=since, per_page=per_page
    )
