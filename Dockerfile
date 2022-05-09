FROM python:3.8.2

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

ADD ./requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code/

RUN python manage.py migrate

RUN python manage.py initial_user

CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]