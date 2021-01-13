from python:3.6.1

COPY . /application
WORKDIR /application

RUN pip install -r requirements.txt
VOLUME /application/config

ENV PATH=$PATH:/application
ENV PYTHONPATH /application

WORKDIR /application/src

CMD ["python", "app.py"]
