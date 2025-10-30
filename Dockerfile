FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
  
RUN useradd -m -u 1000 myuser
USER myuser
WORKDIR /app/myuser

COPY --chown=myuser:myuser requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

ENV PATH="/app/myuser/.local/bin:${PATH}"

COPY --chown=myuser:myuser . .

CMD ["python3", "src/app.py"]
