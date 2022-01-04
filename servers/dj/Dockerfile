FROM python:3.9

WORKDIR /code
ADD requirements.txt .
RUN pip install -r requirements.txt
RUN chmod 777 /tmp/

ADD . .

EXPOSE 8089
ENV PYTHONPATH /code
CMD ["gunicorn", "-c", "gunicorn_conf.py", "dj.wsgi:application"]
