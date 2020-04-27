FROM ubuntu AS builder
RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server
RUN apt-get install -y libmysqlclient-dev
RUN apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get -y install nodejs
RUN npm install -g newman
COPY ./requirements.txt /api/requirements.txt
WORKDIR /api
RUN pip3 install -r requirements.txt
COPY . /api
