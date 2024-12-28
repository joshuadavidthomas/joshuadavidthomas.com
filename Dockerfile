# syntax=docker/dockerfile:1.9
ARG PYTHON_VERSION=3.12
ARG NODE_VERSION=20
ARG UID=1000
ARG GID=1000


FROM python:${PYTHON_VERSION}-slim AS base

SHELL ["/bin/sh", "-exc"]
ARG NODE_VERSION
ENV DEBIAN_FRONTEND=noninteractive \
  UV_LINK_MODE=copy \
  UV_COMPILE_BYTECODE=1 \
  UV_PYTHON_DOWNLOADS=never \
  UV_PYTHON=python${PYTHON_VERSION} \
  UV_PROJECT_ENVIRONMENT=/app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  <<EOT
apt-get update -qy
apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    build-essential \
    ca-certificates \
    curl \
    git \
    jq
curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash -
apt-get update -qy
apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    nodejs
npm install -g npm@latest
apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
EOT


FROM base AS python-deps

COPY pyproject.toml uv.lock /_lock/
RUN --mount=type=cache,target=/root/.cache <<EOT
cd /_lock
uv sync \
    --locked \
    --no-dev \
    --no-install-project
EOT

COPY . /src
RUN --mount=type=cache,target=/root/.cache \
  uv pip install \
  --python=$UV_PROJECT_ENVIRONMENT \
  --no-deps \
  /src


FROM python-deps AS python-dev

WORKDIR /src
RUN --mount=type=cache,target=/root/.cache <<EOT
uv sync \
    --locked \
    --dev
EOT


FROM python-deps AS node-deps

ARG UID
ARG GID
ARG BUILDARCH
ARG BUILDVARIANT

WORKDIR /src
RUN --mount=type=cache,target=/root/.npm <<EOT
npm install

case ${BUILDARCH} in
    arm64)
        case ${BUILDVARIANT} in
            v7) TAILWINDCSS_ARCH=armv7 ;;
            *)  TAILWINDCSS_ARCH=arm64 ;;
        esac ;;
    *) TAILWINDCSS_ARCH=x64 ;;
esac
TAILWINDCSS_VERSION=$(jq -r '.dependencies.tailwindcss // .devDependencies.tailwindcss' package.json | sed 's/^[^0-9]*//')
curl -fsSL "https://github.com/tailwindlabs/tailwindcss/releases/download/v${TAILWINDCSS_VERSION}/tailwindcss-linux-${TAILWINDCSS_ARCH}" \
    -o "/usr/local/bin/tailwindcss-linux-${TAILWINDCSS_ARCH}-${TAILWINDCSS_VERSION}"
chmod 755 "/usr/local/bin/tailwindcss-linux-${TAILWINDCSS_ARCH}-${TAILWINDCSS_VERSION}"
chown ${UID}:${GID} "/usr/local/bin/tailwindcss-linux-${TAILWINDCSS_ARCH}-${TAILWINDCSS_VERSION}"
EOT


FROM node-deps AS static

WORKDIR /src
RUN <<EOT
uv run manage.py tailwind --skip-checks build
uv run manage.py collectstatic --noinput --clear --skip-checks --no-default-ignore
EOT


FROM python:${PYTHON_VERSION}-slim AS final

SHELL ["/bin/sh", "-exc"]
ARG DJANGO_PORT
ARG UID
ARG GID
ENV PATH=/app/bin:$PATH \
  PYTHONPATH=/app \
  PYTHONUNBUFFERED=1
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  <<EOT
apt-get update -qy
apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    fuse3 \
    gosu \
    sqlite3
apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

groupadd -g "${GID}" --system django
useradd -l -u "${UID}" -g "${GID}" -d /app --system django
mkdir -p /app
chown ${UID}:${GID} /app
EOT

COPY --from=python-deps --chown=${UID}:${GID} /app /app
COPY --from=static --chown=${UID}:${GID} /src/staticfiles /app/staticfiles
COPY --chown=${UID}:${GID} . /app/
COPY --from=flyio/litefs:0.5 /usr/local/bin/litefs /usr/local/bin/litefs
USER django
WORKDIR /app

RUN <<EOT
python -V
python -Im site
EOT

STOPSIGNAL SIGINT
EXPOSE ${DJANGO_PORT}
ENTRYPOINT ["litefs", "mount"]
