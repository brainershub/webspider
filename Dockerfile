# As Scrapy runs on Python, I choose the official Python 3 Docker image.
# FROM ubuntu:latest
# FROM python:3

# RUN apt-get update && apt-get upgrade -y
# RUN apt-get -yqq install python3-pip python-dev
# RUN pip3 install psycopg2 && pip3 install psycopg2-binary
# RUN pip3 install --upgrade pip
# RUN pip3 install scrapy --upgrade
# RUN pip3 install scrapy-splash

# COPY . /services/webscrap
# # Set the working directory to /usr/src/app.
# WORKDIR /services/webscrap

# # Copy the file from the local host to the filesystem of the container at the working directory.
# COPY requirements.txt ./
 
# # Install Scrapy specified in requirements.txt.
# RUN pip3 install --no-cache-dir -r requirements.txt
 
# # Copy the project source code from the local host to the filesystem of the container at the working directory.
# EXPOSE 80
# EXPOSE 5432/tcp
 
# # Run the crawler when the container launches.
# CMD [ "python3", "go-spider.py" ]

FROM python:3.9.5-slim-buster

WORKDIR /usr/src/app/scrapy

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/scrapy/requirements.txt
# COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/scrapy/

#ENV DATABASE_URL=postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev
#ENV TABLE_CONTENT=content_table

EXPOSE 80
EXPOSE 5432

RUN cat ./pharma/go-spider.py

# CMD [ "python", "./pharma/go-spider.py" ]
CMD [ "bash" ]
# CMD [ "scrapy", "crawl", "gelbeliste"]
# run entrypoint.sh
#ENTRYPOINT ["/usr/src/app/entrypoint.sh"]