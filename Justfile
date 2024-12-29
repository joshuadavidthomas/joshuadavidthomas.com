set dotenv-load := true
set unstable := true

mod copier ".just/copier.just"
mod dj ".just/django.just"
mod docker ".just/docker.just"
mod docs ".just/documentation.just"
mod node ".just/node.just"
mod pg ".just/postgres.just"
mod project ".just/project.just"
mod py ".just/python.just"

export DATABASE_URL := env_var_or_default('DATABASE_URL', 'postgres://postgres:postgres@db:5432/postgres')
export VIRTUAL_ENV := env_var_or_default('VIRTUAL_ENV', '.venv')
python_dir := if os_family() == "windows" { VIRTUAL_ENV + "/Scripts" } else { VIRTUAL_ENV + "/bin" }
export python := python_dir + if os_family() == "windows" { "/python.exe" } else { "/python" }
export system_python := if os_family() == "windows" { "py.exe" } else { "python" }

# List all available commands
[private]
default:
    @just --list

# Install and update all dependencies
bootstrap:
    @just docker build
    @just py install
    @just node install

# Clean up local development environment
clean:
    @just project clean
    @just docker clean

# Open a bash console within a specified container (default: 'app')
console CONTAINER="app":
    @just docker run {{ CONTAINER }} "" "/bin/bash"

# Stop local development environment
down:
    @just docker down

# Run the linters on all files in project
lint:
    @just project lint

# Generate lockfiles for all dependencies
lock:
    @just py lock
    @just node lock

# Print out the logs of all Docker containers, optionally specifying a container to focus on
logs *ARGS:
    @just docker logs {{ ARGS }}

# Run Django migrations
migrate *ARGS:
    @just dj migrate {{ ARGS }}

alias mm := makemigrations

# Generate Django migrations
makemigrations *ARGS:
    @just dj makemigrations {{ ARGS }}

# Run a Django management command
manage *COMMAND:
    @just dj manage {{ COMMAND }}

# Refresh local development environment
refresh:
    @just lock
    @just docker stop
    @just bootstrap
    @just docker start

# Setup local development environment
setup:
    @just clean
    @just project setup
    @just bootstrap
    @just docker start
    @just dj migrate
    @just dj createsuperuser
    @just py test
    @just py coverage-report
    @just py types
    @just project lint
    @just docker down

# Open a tool's interative shell within a specified container (default: 'app')
shell CONTAINER="app" COMMAND="":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ {{ CONTAINER }} = 'db' ]; then
        COMMAND="psql -d {{ DATABASE_URL }}"
    elif [ "{{ CONTAINER }}" = "node" ] || [ "{{ CONTAINER }}" = "tailwind" ]; then
        COMMAND="node"
    elif [ "{{ CONTAINER }}" = "app" ] || [ "{{ CONTAINER }}" = "worker" ]; then
        COMMAND="ipython"
    elif [ {{ CONTAINER }} = 'dj' ]; then
        COMMAND="python -m manage shell_plus"
    fi
    [ -n "{{ COMMAND }}" ] && COMMAND="{{ COMMAND }}"
    COMMAND="${COMMAND:-/bin/bash}"
    just docker run {{ CONTAINER }} "" $COMMAND

# Start local development environment in background
start:
    @just docker start

# Stop local development environment
stop:
    @just docker stop

# Follow the logs of all Docker containers, optionally specifying a container to focus on
tail *ARGS:
    @just docker tail {{ ARGS }}

# Run entire test suite, including generating code coverage
test:
    @just py test
    @just py coverage-html

# Start local development environment in foreground
up:
    @just docker up

# Update local development environment
update:
    @just docker pull
    @just lock
    @just bootstrap

# Upgrade all dependencies to their newest versions
upgrade:
    @just py upgrade
    @just node upgrade
