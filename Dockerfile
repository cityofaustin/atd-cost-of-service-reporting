FROM ghcr.io/oracle/oraclelinux8-instantclient:19

WORKDIR /app
COPY . /app

RUN dnf update && dnf install -y python3 python3-pip vim
RUN pip3 install -r requirements.txt
