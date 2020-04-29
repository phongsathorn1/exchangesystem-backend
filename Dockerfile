FROM python:3.7.4

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update \ 
&& apt-get install dos2unix -y \
&& pip install --upgrade pip \
&& apt-get install libmariadb-dev -y \ 
&& pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +X start.sh

RUN apt-get update && apt-get install -y wget

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN dos2unix start.sh
CMD ["/bin/bash", "dos2unix", "start.sh"]