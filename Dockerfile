FROM python:3.7.5-slim-buster

ENV INSTALL_PATH /backend_top_rated_app
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH
RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev --no-install-recommends
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "app:app"
