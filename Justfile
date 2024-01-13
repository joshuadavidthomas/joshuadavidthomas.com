set dotenv-load := true

@_default:
    just --list

@fmt:
    just --fmt --unstable

# ----------------------------------------------------------------------
# DEPENDENCIES
# ----------------------------------------------------------------------

_pip-compile *ARGS:
    python -m piptools compile --resolver=backtracking --strip-extras {{ ARGS }}

@pip-compile *ARGS:
    just _pip-compile {{ ARGS }} --generate-hashes requirements.in
    just _pip-compile {{ ARGS }} requirements.nohash.in

_install *ARGS:
    python -m pip install --upgrade {{ ARGS }}

@install:
    just _install -r requirements.txt
    just _install -r requirements.nohash.txt

@upgrade:
    just pip-compile --upgrade

pup:
    python -m pip install --upgrade pip pip-tools

update:
    @just pup
    @just upgrade
    @just install

# ----------------------------------------------------------------------
# DJANGO
# ----------------------------------------------------------------------

@manage *COMMAND:
    just command python -m manage {{ COMMAND }}

alias mm := makemigrations

makemigrations *APPS:
    @just manage makemigrations {{ APPS }}

migrate *ARGS:
    @just manage migrate {{ ARGS }}

shell-plus:
    @just manage shell_plus

createsuperuser USERNAME="admin" EMAIL="" PASSWORD="admin":
    docker compose run --rm --no-deps app /bin/bash -c 'echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('"'"'{{ USERNAME }}'"'"', '"'"'{{ EMAIL }}'"'"', '"'"'{{ PASSWORD }}'"'"') if not User.objects.filter(username='"'"'{{ USERNAME }}'"'"').exists() else None" | python manage.py shell'

# ----------------------------------------------------------------------
# DOCS
# ----------------------------------------------------------------------

@docs-pip-compile *ARGS:
    just _pip-compile {{ ARGS }} --output-file --generate-hashes docs/requirements.txt docs/requirements.in

@docs-upgrade:
    just docs-pip-compile --upgrade

@docs-install:
    python -m pip install -r docs/requirements.txt

@docs-serve:
    #!/usr/bin/env sh
    # just _cog
    if [ -f "/.dockerenv" ]; then
        sphinx-autobuild docs docs/_build/html --host "0.0.0.0"
    else
        sphinx-autobuild docs docs/_build/html --host "localhost"
    fi

@docs-build LOCATION="docs/_build/html":
    # just _cog
    sphinx-build docs {{ LOCATION }}

# DOCS UTILS
# @_cog:
#     cog -r docs/misc/utilities/just.md

# ----------------------------------------------------------------------
# UTILS
# ----------------------------------------------------------------------

envsync:
    #!/usr/bin/env python
    from pathlib import Path

    envfile = Path('.env')
    envfile_example = Path('.env.example')

    if not envfile.exists():
        envfile.write_text(envfile_example.read_text())

    with envfile.open() as f:
        lines = [line for line in f.readlines() if not line.endswith('# envsync: ignore\n')]
        lines = [line.split('=')[0] + '=\n' if line.endswith('# envsync: no-value\n') else line for line in lines]

        lines.sort()
        envfile_example.write_text(''.join(lines))

lint:
    pre-commit run --all-files

# ----------------------------------------------------------------------
# DOCKER
# ----------------------------------------------------------------------

# Build services using docker-compose
@build:
    docker compose build

# Stop and remove all containers, networks, images, and volumes
@clean:
    just down --volumes --rmi local

# Run a command within the 'app' container
@command *ARGS:
    docker compose run --rm --no-deps app /bin/bash -c "{{ ARGS }}"

# Open an interactive shell within the 'app' container opens a console
@console:
    docker compose run --rm --no-deps app /bin/bash

# Stop and remove all containers defined in docker-compose
@down *ARGS:
    docker compose down {{ ARGS }}

# Display the logs for containers, optionally using provided arguments (e.g., --follow)
@logs *ARGS:
    docker compose logs {{ ARGS }}

# Display the running containers and their statuses
@ps:
    docker compose ps

# Pull the latest versions of all images defined in docker-compose
@pull:
    docker compose pull

# Restart services, optionally targeting specific ones
@restart *ARGS:
    docker compose restart {{ ARGS }}

# Open an interactive shell within a specified container (default: 'app')
@shell *ARGS="app":
    docker compose run --rm --no-deps {{ ARGS }} /bin/bash

# Start services using docker-compose, defaulting to detached mode
@start *ARGS="--detach":
    just up {{ ARGS }}

# Stop services by calling the 'down' command
@stop:
    just down

# Continuously display the latest logs by using the --follow option, optionally targeting specific containers
@tail *ARGS:
    just logs '--follow {{ ARGS }}'

# Run tests using pytest within the 'app' container, with optional arguments
@test *ARGS:
    docker compose run --rm --no-deps app pytest {{ ARGS }}

# Start services using docker-compose, with optional arguments
@up *ARGS:
    docker compose up {{ ARGS }}
