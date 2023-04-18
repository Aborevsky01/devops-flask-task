# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

RUN pip3.8 install flask

ADD app.py /app/

WORKDIR /app

COPY . .

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
