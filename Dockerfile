FROM python:3.11-slim as base
ENV PYTHONPATH /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG False
RUN mkdir -p /app
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    fuse3 \
    gosu \
    sqlite3 \
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*
COPY --from=flyio/litefs:0.5 /usr/local/bin/litefs /usr/local/bin/litefs
WORKDIR /app


FROM base as py
COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
  && python -m pip install -r requirements.txt


FROM base as app
COPY litefs.yml manage.py redirects.json /app/
COPY blog /app/blog
COPY config /app/config
COPY core /app/core
COPY flyio /app/flyio
COPY templates /app/templates
COPY users /app/users


FROM nikolaik/python-nodejs:python3.11-nodejs20 as static
WORKDIR /app
COPY --from=py /usr/local /usr/local
COPY --from=app /app /app
COPY package.json package-lock.json tailwind.config.cjs /app/
COPY static /app/static
ENV DATABASE_URL sqlite:///db.sqlite3
RUN npm install \
  && python manage.py tailwind build \
  && python manage.py collectstatic --noinput --clear


FROM base as final
COPY --from=py /usr/local /usr/local
COPY --from=app /app /app
COPY --from=static /app/staticfiles /app/staticfiles
RUN addgroup --system django \
  && adduser --system --ingroup django django \
  && chown -R django:django /app
EXPOSE 8000
ENTRYPOINT litefs mount
