FROM python:3.9-slim-buster

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r ./requirements.txt

EXPOSE 80
EXPOSE 443

CMD ["python", "main.py"]
