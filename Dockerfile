FROM python:3.13-slim AS base

LABEL key="blockstak-news-api"


ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update -y
RUN apt-get -y install --no-install-recommends \
    libpq-dev gcc curl wkhtmltopdf \
    python3-dev default-libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && ln -fs /usr/share/zoneinfo/UTC /etc/localtime

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

FROM base AS final

COPY . /app

RUN echo '#!/bin/bash\naerich upgrade\nfastapi run --host 0.0.0.0 main.py' > /app/start.sh && \
    chmod +x /app/start.sh

CMD ["/app/start.sh"]
