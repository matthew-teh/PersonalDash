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

COPY . .
RUN uv sync 

EXPOSE 3000

CMD ["uv", "run", "reflex", "run", "--env", "prod", "--frontend-port", "65510", "--loglevel", "debug"]

# docker build -t flexdash:latest . 