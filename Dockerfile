FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

ARG PROJECT=linecms
ARG PROJECT_DIR=/opt/${PROJECT}

ARG PROJECT_SERVER_DIR=${PROJECT_DIR}/server
ARG PROJECT_STATIC_DIR=${PROJECT_DIR}/static

# Prepare storage, app.

RUN addgroup -g 82 -S www-data \
  && adduser -u 82 -D -S -G www-data www-data \
  && mkdir -p ${PROJECT_SERVER_DIR} ${PROJECT_STATIC_DIR} \
  && chown -R www-data:www-data ${PROJECT_DIR}

COPY --chown=www-data:www-data . ${PROJECT_SERVER_DIR}

# Installations

WORKDIR ${PROJECT_SERVER_DIR}

RUN pip install --no-cache-dir -r requirements.txt && \
  pip install --no-cache-dir whitenoise gunicorn djongo

EXPOSE 8000

# Preparations

ENV STATIC_ROOT ${PROJECT_STATIC_DIR}
ENV USE_WHITENOISE 1

USER www-data

RUN python manage.py collectstatic --no-input

CMD [ "sh", "-c", "python manage.py migrate --no-input && gunicorn -b 0.0.0.0:8000 linecms_web.wsgi" ]
