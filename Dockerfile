# syntax=docker/dockerfile:1

FROM quay.io/repository/bitnami/python

WORKDIR /myKart

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
