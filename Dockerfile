FROM python:3.7.4

# Set Environment Variable
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true

WORKDIR /src

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN apt-get update \ 
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

CMD ["/bin/bash", "start.sh"]