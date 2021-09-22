# Desafio API Carrinho

## Getting Started

### 1. Development environment (Requires Docker and Docker Compose)

1.1 Run this on the project directory:
```
docker build -t api-carrinho .

docker-compose up -d
```

1.2 Still in the project directory, run the migrations:
```
docker-compose run django python3 manage.py makemigrations

docker-compose run django python3 manage.py migrate
```



### 3.1 Tests

2.1 Run tests
```
docker-compose run django python manage.py test api
```

### 4. Docs API Reference

https://app.swaggerhub.com/apis-docs/danilogoulart8/desafioapicarrinho/1.0.0-oas3#/