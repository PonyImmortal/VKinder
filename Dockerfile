FROM python:3.11.4-slim-bullseye

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y postgresql

COPY bot.py .

CMD [ "python", "/app/bot.py" ]
