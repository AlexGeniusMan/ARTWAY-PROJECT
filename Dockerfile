FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/artway

COPY . .
RUN pip install -r requirements.txt
RUN python3 manage.py collectstatic --noinput