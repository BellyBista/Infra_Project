FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        netbase \
        build-essential \
        gcc \
        g++ \
        && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

EXPOSE 8501

COPY . .

ENTRYPOINT ["streamlit", "run"]

CMD ["About.py"]