FROM python:3.11-slim-buster as base
ENV PYTHONPATH /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG False
RUN mkdir -p /app
WORKDIR /app


FROM base as py
COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
  && python -m pip install -r requirements.txt


FROM base as app
COPY manage.py /app
COPY blog /app/blog
COPY config /app/config
COPY core /app/core
COPY templates /app/templates
COPY users /app/users


FROM nikolaik/python-nodejs:python3.11-nodejs18-bullseye as static
WORKDIR /app
COPY --from=py /usr/local /usr/local
COPY --from=app /app /app
COPY package.json tailwind.config.cjs yarn.lock /app/
COPY static /app/static
ENV DATABASE_URL sqlite:///db.sqlite3
RUN yarn install \
  && python manage.py tailwind build \
  && python manage.py collectstatic --noinput --clear


FROM base as final
COPY --from=py /usr/local /usr/local
COPY --from=app /app /app
COPY --from=static /app/staticfiles /app/staticfiles
RUN addgroup --system django \
  && adduser --system --ingroup django django \
  && chown -R django:django /app
USER django
EXPOSE 8000
CMD ["python", "-m", "gunicorn", "config.wsgi:application", "--config", "python:config.gunicorn"]
