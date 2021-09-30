FROM python:3.9.5

WORKDIR /code

COPY . /code

RUN pip install -r requirements.txt

RUN python manage.py collectstatic

CMD gunicorn food.wsgi:application --bind 0.0.0.0:8000
