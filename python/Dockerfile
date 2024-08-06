FROM python:3.11.6-slim-bullseye

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "llm_chat.py"]