FROM python:3.12-slim-bookworm
WORKDIR /app

RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y libmariadb3 libmariadb-dev

COPY ./requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000
ENV FLASK_APP=main.py
CMD ["flask", "run", "--host", "0.0.0.0"]
