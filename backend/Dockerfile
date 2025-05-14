FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    LOG_LEVEL=info

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    unzip \
	nano \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
 && pip install -r requirements.txt
 
COPY . /app
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]
