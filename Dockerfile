FROM python:3.12-slim

WORKDIR /srv

ARG VERSION=dev
ENV APP_VERSION=${VERSION}

COPY app ./app

USER nobody
EXPOSE 8080
CMD ["python", "-m", "app.server"]
