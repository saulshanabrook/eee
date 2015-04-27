FROM python:3.4.2-onbuild

ENV PYTHONUNBUFFERED TRUE

ENV PYTHONASYNCIODEBUG 1

CMD gunicorn -b 0.0.0.0  --timeout 360 eee.dev_server:app
