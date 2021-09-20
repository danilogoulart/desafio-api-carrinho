# Desafio API Carrinho

## Getting Started

### Development environment - Requires Docker and Docker Compose

1. Run this on the project directory:
```
docker build -t api-carrinho .

docker-compose up -d
```

2. Still in the project directory, run:
```
docker-compose run django python3 manage.py makemigrations

docker-compose run django python3 manage.py migrate
```