# FROM python:3.9.7 as base
FROM python:3.9.7 as build 
# ENV PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app

# FROM base as poetry
RUN pip install poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry export -o requirements.txt

# FROM base as build
# COPY --from=poetry /app/requirements.txt /tmp/requirements.txt
RUN python -m venv .venv && \
    .venv/bin/pip install 'wheel==0.36.2' && \
    # .venv/bin/pip install -r /tmp/requirements.txt
    .venv/bin/pip install -r /app/requirements.txt

FROM python:3.9.7-slim as runtime
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
ENV PATH=/app/.venv/bin:$PATH

ENV TARGET_USER=""
ENV DOWNLOAD_DIRECTORY=""
ENV TWITTER_BEARER_TOKEN=""

RUN mkdir /data
COPY --from=build /app/.venv /app/.venv
COPY ./pytwitloader /app
ENTRYPOINT ["python", "main.py"]