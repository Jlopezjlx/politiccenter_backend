FROM ubuntu

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server

RUN apt-get install -y libmysqlclient-dev

COPY ./requirements.txt /api/requirements.txt

WORKDIR /api

RUN pip3 install -r requirements.txt

COPY . /api

ENTRYPOINT [ "python3" ]
ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]