FROM python:3.9.6-slim-buster

WORKDIR /usr/src

COPY ./requirements.txt /usr/src/requirements.txt

RUN pip install -r ./requirements.txt --no-cache-dir

COPY main.py /usr/src/main.py
COPY models.py /usr/src/models.py
COPY database.py /usr/src/database.py
COPY crud.py /usr/src/crud.py
COPY templates /usr/src/templates

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
