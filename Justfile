set dotenv-load := true

@_default:
    just --list

##################
#  DEPENDENCIES  #
##################

pip-compile *ARGS:
    pip-compile --resolver=backtracking {{ ARGS }} --strip-extras --generate-hashes requirements.in

install:
    python -m pip install --upgrade -r requirements.txt

pup:
    python -m pip install --upgrade pip pip-tools

update:
    @just pup
    @just pip-compile --upgrade
    @just install

venv:
    #!/usr/bin/env python
    from __future__ import annotations

    import os
    import subprocess
    from pathlib import Path

    home = Path.home()
    pyenv_version = home / ".pyenv" / "version"
    PY_VERSION = pyenv_version.read_text().rstrip('\n')
    name = f"jt.dev-{PY_VERSION}"
    pyenv_virtualenv_dir = home / ".pyenv" / "versions" / name

    if not pyenv_virtualenv_dir.exists():
        subprocess.run(["pyenv", "virtualenv", PY_VERSION, name], check=True)

    (python_version_file := Path(".python-version")).write_text(name)

##################
#     DJANGO     #
##################

manage *COMMAND:
    python -m manage {{ COMMAND }}

dev DJANGO_PORT="8000":
    honcho start -f Procfile.dev

prod:
    python -m gunicorn config.wsgi:application --config python:config.gunicorn

alias mm := makemigrations

makemigrations *APPS:
    @just manage makemigrations {{ APPS }}

migrate *ARGS:
    @just manage migrate {{ ARGS }}

shell:
    @just manage shell_plus

createsuperuser USERNAME="admin" EMAIL="" PASSWORD="admin":
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('{{ USERNAME }}', '{{ EMAIL }}', '{{ PASSWORD }}') if not User.objects.filter(username='{{ USERNAME }}').exists() else None" | python manage.py shell

##################
#     DOCKER     #
##################

enter CONTAINER="jt.dev[-_]devcontainer[-_]app" SHELL="zsh" WORKDIR="/workspace" USER="vscode":
    #!/usr/bin/env sh
    if [ -f "/.dockerenv" ]; then
        echo "command cannot be run from within a Docker container"
    else
        case {{ SHELL }} in
            "zsh" )
                shell_path="/usr/bin/zsh" ;;
            "bash" )
                shell_path="/bin/bash" ;;
            "sh" )
                shell_path="/bin/sh" ;;
            * )
                shell_path="/usr/bin/zsh" ;;
        esac

        container=$(docker ps --filter "name={{ CONTAINER }}" --format "{{{{.Names}}")

        docker exec -it -u {{ USER }} -w {{ WORKDIR }} $container $shell_path
    fi

testbuild:
    docker build -t jt.dev:latest .

testrun:
    docker run -it --rm -p 8000:8000 jt.dev:latest

createdb CONTAINER_NAME="jtdev_postgres" VERSION="15.3":
    #!/usr/bin/env python
    from __future__ import annotations

    import os
    import re
    import shutil
    import socket
    import subprocess
    import time
    from pathlib import Path

    CONTAINER_NAME = "{{ CONTAINER_NAME }}"
    VERSION = "{{ VERSION }}"


    def is_port_open(port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("127.0.0.1", port)) != 0


    def main():
        if not shutil.which("docker"):
            print("Docker is not installed")
            return

        if subprocess.getoutput(f"docker ps -q -f name={CONTAINER_NAME}"):
            print(f"Postgres container {CONTAINER_NAME} is already running")
        else:
            if subprocess.getoutput(
                f"docker ps -aq -f status=exited -f name={CONTAINER_NAME}"
            ):
                print(f"Starting postgres container {CONTAINER_NAME}")
                subprocess.run(["docker", "start", CONTAINER_NAME], check=True)
            else:
                print(f"Creating postgres container {CONTAINER_NAME}")
                port = 5432
                while not is_port_open(port):
                    print(f"Port {port} is already in use")
                    print("Incrementing port number by 1")
                    port += 1
                subprocess.run(
                    [
                        "docker",
                        "run",
                        "--name",
                        CONTAINER_NAME,
                        "-e",
                        "POSTGRES_USER=postgres",
                        "-e",
                        "POSTGRES_PASSWORD=postgres",
                        "-e",
                        "POSTGRES_DB=postgres",
                        "-p",
                        f"{port}:5432",
                        "-d",
                        f"postgres:{VERSION}",
                    ],
                    check=True,
                )

        port_output = subprocess.getoutput(f"docker port {CONTAINER_NAME} 5432")
        port = port_output.split(":")[1]
        DATABASE_URL = f"postgres://postgres:postgres@localhost:{port}/postgres"
        os.environ["DATABASE_URL"] = DATABASE_URL

        env_file = Path(".env")
        if env_file.exists():
            print("Updating DATABASE_URL in .env file")
            content = env_file.read_text()
            content = re.sub(r"DATABASE_URL=.*", f"DATABASE_URL={DATABASE_URL}", content)

            if "DATABASE_URL=" not in content:
                content += f"\nDATABASE_URL={DATABASE_URL}\n"

            env_file.write_text(content)
            print("env_file", env_file.read_text())
        else:
            print("Creating .env file")
            env_file.write_text(f"DATABASE_URL={DATABASE_URL}\n")

        while True:
            ready = (
                subprocess.run(
                    [
                        "docker",
                        "exec",
                        "-it",
                        CONTAINER_NAME,
                        "pg_isready",
                        "-U",
                        "postgres",
                        "-q",
                    ]
                ).returncode
                == 0
            )
            if ready:
                break
            print("Waiting for postgres to start")
            time.sleep(1)

        subprocess.run(["just", "manage", "migrate"], check=True)
        subprocess.run(["just", "createsuperuser"], check=True)


    raise SystemExit(main())

##################
#     UTILS      #
##################

# format justfile
@_fmt:
    just --fmt --unstable

# run pre-commit on all files
lint:
    pre-commit run --all-files

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
