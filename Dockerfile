FROM python:3.7.5-slim-buster

ENV INSTALL_PATH /backend_top_rated_app
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH
RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev wget --no-install-recommends
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O $INSTALL_PATH/cloud_sql_proxy
RUN chmod +x $INSTALL_PATH/cloud_sql_proxy
RUN mkdir /cloudsql; chmod 777 /cloudsql

COPY . .

CMD $INSTALL_PATH/cloud_sql_proxy -dir=/cloudsql -instances=bluestacks-cloud-beginners:us-central1:backend-top-rated-app-pg-instance -credential_file=./application_default_credentials.json & gunicorn -b 0.0.0.0:$PORT --access-logfile - "app:app"
