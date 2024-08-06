FROM python:3.11.6-alpine3.18

WORKDIR /app

RUN apk add --no-cache \
    build-base \
    gfortran \
    openblas-dev \
    lapack-dev \
    musl-dev \
    python3-dev

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir scikit-learn

COPY . /app

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "llm_chat.py"]