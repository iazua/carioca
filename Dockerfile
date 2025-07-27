FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir poetry && poetry install --no-root
ENTRYPOINT ["poetry", "run", "carioca", "play"]
