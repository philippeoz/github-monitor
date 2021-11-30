FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN groupadd user && useradd -m -g user user
USER user
ENV PATH="/home/user/.local/bin:${PATH}"

WORKDIR /app

ADD pyproject.toml /app/pyproject.toml
ADD poetry.lock /app/poetry.lock

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --user poetry==1.0.3 && \
    poetry export --without-hashes -f requirements.txt -n | \
    xargs -n 1 pip install --no-cache-dir --user && \
    pip uninstall --yes poetry

COPY --chown=user:user . /app

CMD python manage.py runserver 0.0.0.0:8000
