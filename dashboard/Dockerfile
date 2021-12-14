FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow

COPY requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["streamlit", "run", "main.py"]