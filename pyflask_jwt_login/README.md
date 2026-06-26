
## Frontend
```shell
cd frontend
npm install
npm install react-router-dom
```

## Backend
```shell
cd backend
pipenv shell
pipenv install flask flask-sqlalchemy python-dotenv psycopg2-binary flask-migrate flask-cors flask-jwt-extended werkzeug
python app.py
```

## Inicializar db (Crear Carpeta migrations)
```shell
flask db init 
```

## Crear nueva version de tablas
```shell
flask db migrate
```

## Subir nueva versión a BD
```shell
flask db upgrade
```

## Puerto para correr
http://localhost:5173/
