## Crear la imagen

```shell
docker build -t my-python-app .
```

## Ejecutar el contenedor
```shell
docker run -p 8000:8000 -d my-python-app
```

## Descargar imagen de postgres
```shell
docker pull postgres:15
```

## Crear contenedor para postgres en docker
```shell
docker run -d --name postgres_latam -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=latam_71 -p 5435:5432 postgres
```

## Iniciar entorno
```shell
pipenv shell
```

## Instalar dependencias
```shell
pipenv install flask flask-sqlalchemy python-dotenv psycopg2-binary
```

pipenv install flask-migrate flask-cors
flask db init # Crear Carpeta migrations
flask db migrate # Crear version de tablas
flask db upgrade # Subir a BD

python app.py

http://127.0.0.1:5000/