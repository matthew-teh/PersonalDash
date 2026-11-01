FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    nodejs \
    npm \
    unzip \
    && rm -rf /var/lib/apt/lists/*


ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod +x /install.sh && /install.sh && rm /install.sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

RUN uv init
RUN uv add reflex openmeteo-requests requests 

COPY . .

EXPOSE 65502

CMD ["uv", "run", "reflex", "run", "--env", "prod", "--frontend-port", "65503", "--loglevel", "debug"]

# uv run reflex run --env prod --frontend-port 65503 --loglevel debug
# docker build -t reflex-app-v2 .
# docker run -d -p 65503:65503 --name Reflex-PDash-V2 reflex-app-v2
# docker rm Reflex-PDash-V2