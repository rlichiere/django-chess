FROM python:2.7.13

MAINTAINER panda <pandareum@aim.com>

RUN apt-get update && apt-get install -y wget \
                  vim \
                  gettext \
                  mysql-client libmysqlclient-dev \
                  sqlite3 \
       --no-install-recommends && rm -rf /var/lib/apt/lists/*

ENV APPDIR=/usr/src/app

RUN mkdir -p $APPDIR

WORKDIR $APPDIR

COPY requirements.txt $APPDIR
RUN pip install -r requirements.txt

COPY . $APPDIR

ENV DB_NAME='db' \
    DB_HOST='host' \
    DB_PORT='3306' \
    DB_USER='login' \
    DB_PASS='pass'

COPY app-start.sh /app-start.sh
RUN chmod +x /app-start.sh

EXPOSE 8000

CMD ["sh", "app-start.sh"]
