FROM python:3.12-slim-bookworm as mysqlclient-build
RUN curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | bash 
RUN apt-get update
RUN apt-get install -y mariadb-client libmariadb-dev-compat libmariadb-dev
RUN pip wheel -w /deps mysqlclient

FROM python:3.12-slim-bookworm
COPY --from=mysqlclient-build /deps/*.whl /deps
RUN pip install /deps/*.whl && rm -rf /deps

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000
ENV FLASK_APP=main.py
CMD ["flask", "run", "--host", "0.0.0.0"]
