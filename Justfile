set dotenv-load := true

@_default:
    just --list

@fmt:
    just --fmt --unstable

# ----------------------------------------------------------------------
# DEPENDENCIES
# ----------------------------------------------------------------------

# Generate requirements file
lock *ARGS:
    python -m uv pip compile {{ ARGS }} --generate-hashes requirements.in --output-file requirements.txt

# Install dependencies
install *ARGS:
    python -m uv pip install --upgrade -r requirements.txt

# Generate and upgrade dependencies
upgrade:
    @just lock --upgrade
# Install and update dependency tools
pup:
    python -m pip install --upgrade pip uv

# Update local development environment
update:
    @just pup
    @just upgrade
    @just install

# ----------------------------------------------------------------------
# TESTING/TYPES
# ----------------------------------------------------------------------

coverage:
    rm -rf htmlcov
    @just command "python -m coverage run -m pytest && python -m coverage html --skip-covered --skip-empty"

# Run tests using pytest within the 'app' container, with optional arguments
test *ARGS:
    @just command pytest {{ ARGS }}

# Run mypy on project
types:
    @just command python -m mypy .

# ----------------------------------------------------------------------
# DJANGO
# ----------------------------------------------------------------------

# Run a Django management command
manage *COMMAND:
    @just command python -m manage {{ COMMAND }}

# Alias for makemigrations
alias mm := makemigrations

# Generate Django migrations
makemigrations *APPS:
    @just manage makemigrations {{ APPS }}

# Run Django migrations
migrate *ARGS:
    @just manage migrate {{ ARGS }}

# Open a Django shell using django-extensions shell_plus command
shell-plus:
    @just manage shell_plus

# Quickly create a superuser with the provided credentials
createsuperuser USERNAME="admin" EMAIL="" PASSWORD="admin":
    docker compose run --rm --no-deps app /bin/bash -c 'echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('"'"'{{ USERNAME }}'"'"', '"'"'{{ EMAIL }}'"'"', '"'"'{{ PASSWORD }}'"'"') if not User.objects.filter(username='"'"'{{ USERNAME }}'"'"').exists() else None" | python manage.py shell'

# Reset a user's password
resetuserpassword USERNAME="admin" PASSWORD="admin":
    docker compose run --rm --no-deps app /bin/bash -c 'echo "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.get(username='"'"'{{ USERNAME }}'"'"'); user.set_password('"'"'{{ PASSWORD }}'"'"'); user.save()" | python manage.py shell'

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

# Build services using docker compose
build *ARGS:
    docker compose build {{ ARGS }}

# Stop and remove all containers, networks, images, and volumes
clean:
    @just down --volumes --rmi local

# Run a command within the 'app' container
command *ARGS:
    docker compose run --rm --no-deps app /bin/bash -c "{{ ARGS }}"

# Open an interactive shell within the 'app' container opens a console
console:
    docker compose run --rm --no-deps app /bin/bash

# Stop and remove all containers defined in docker compose
down *ARGS:
    docker compose down {{ ARGS }}

# Display the logs for containers, optionally using provided arguments (e.g., --follow)
logs *ARGS:
    docker compose logs {{ ARGS }}

# Display the running containers and their statuses
ps:
    docker compose ps

# Pull the latest versions of all images defined in docker compose
pull:
    docker compose pull

# Restart services, optionally targeting specific ones
restart *ARGS:
    docker compose restart {{ ARGS }}

# Open an interactive shell within a specified container (default: 'app')
shell *ARGS="app":
    docker compose run --rm --no-deps {{ ARGS }} /bin/bash

# Start services using docker compose, defaulting to detached mode
start *ARGS="--detach":
    @just up {{ ARGS }}

# Stop services by calling the 'down' command
stop:
    @just down

# Continuously display the latest logs by using the --follow option, optionally targeting specific containers
tail *ARGS:
    @just logs --follow {{ ARGS }}

# Start services using docker compose, with optional arguments
up *ARGS:
    docker compose up {{ ARGS }}
