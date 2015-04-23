FROM python:3.4.2-onbuild

ENV PYTHONUNBUFFERED TRUE

CMD gunicorn -b 0.0.0.0  --timeout 360 eee.server:app
