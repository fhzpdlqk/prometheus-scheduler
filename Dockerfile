FROM python:3.10.5

RUN python -m pip install --upgrade pip

WORKDIR /prometheus_flask

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /prometheus_flask/

ENV PYTHONPATH=/prometheus_flask

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]