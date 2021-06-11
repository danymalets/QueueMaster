FROM python:3.8
ENV PYTHONUNBUFFERED=1
ENV TZ Europe/Minsk
WORKDIR /code
COPY requirements.txt /code/

RUN pip install -r requirements.txt
COPY . /code/