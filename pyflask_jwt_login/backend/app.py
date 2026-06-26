import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

# Importamos la instancia de la base de datos y el modelo desde models.py
from models import db, User

app = Flask(__name__)

# Configuración
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'super-secret-key' # Cambia esto en producción
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Vinculamos la base de datos a la aplicación
db.init_app(app)
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade
CORS(app) # Configuración de Cors
jwt = JWTManager(app)

@app.route('/')
def main():
    return jsonify({ "status": "API Flask con PostgreSQL corriendo"}), 200

# --- RUTAS ---

@app.route('/signup', methods=['POST'])
def signup():
    # Obtener datos del frontend
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    # Validar que vengan los datos
    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    # Verificar que el usuario no exista previamente en la BD
    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        return jsonify({"msg": "Email already exists"}), 400

    # Encriptar la contraseña por seguridad
    hashed_password = generate_password_hash(password)
    
    # 4. Preparar el nuevo usuario
    new_user = User(email=email, password=hashed_password)
    
    # 5. Agregar a la sesión y hacer COMMIT hacia la base de datos
    db.session.add(new_user)
    db.session.commit() # <--- Aquí se guardan los datos físicamente

    return jsonify({"msg": "User created successfully"}), 201


@app.route('/token', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    # Buscar el usuario en la BD
    user = User.query.filter_by(email=email).first()

    # Validar usuario y contraseña desencriptada
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Bad email or password"}), 401

    # Generar el token
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200


# 6. Crear la base de datos automáticamente si no existe
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()