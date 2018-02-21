FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt
RUN python3 manage.py migrate
CMD python3 manage.py runserver 0.0.0.0:8000
