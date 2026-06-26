import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, User, Planet, Favorites
from sqlalchemy.exc import IntegrityError

load_dotenv()

app = Flask(__name__)

# Configurar nuestra app
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) # vinculamos nuestras entidades a nuestra aplicacion
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade
CORS(app) # Configuración de Cors

@app.route('/')
def main():
    return jsonify({ "status": "API Flask con PostgreSQL corriendo"}), 200

@app.route('/api/register', methods=['POST'])
def user_register():
    
    # Recibimos los datos enviados desde el frontend (Postman, React, etc.)
    data = request.get_json()

    # Creamos una instancia vacía de nuestro modelo User
    user = User()
    
    try:
        # Asignamos los datos obligatorios. 
        # Si falta alguno de estos en el JSON, lanzará un KeyError y caerá en el except de abajo.
        user.username = data['username']
        user.name = data['name']
        user.password = data['password'] # Recordatorio: En producción, esto se debe encriptar.
        user.email = data['email']
        user.planet_id = data['planet_id']

        # Preparamos (add) y confirmamos (commit) la transacción en la base de datos
        db.session.add(user)
        db.session.commit()

        # Si el commit es exitoso, devolvemos un 201 (Código HTTP estándar para "Creado")
        return jsonify({"mensaje": "Usuario registrado con éxito"}), 201
        
    except KeyError as e:
        # Esto ocurre si el frontend olvidó enviar un dato obligatorio (ej. no envió el password)
        return jsonify({"error": f"Falta el campo obligatorio: {str(e)}"}), 400
        
    except IntegrityError:
        # Esto ocurre si el correo o username ya están en la base de datos (valores unique=True)
        # Hacemos rollback para limpiar la sesión de la BD y evitar que se quede "colgada"
        db.session.rollback()
        return jsonify({"error": "El nombre de usuario o correo ya está registrado"}), 400
        
    except Exception as e:
        # Esto atrapa cualquier otro error inesperado que pueda surgir
        db.session.rollback()
        return jsonify({"error": f"Error al intentar registrar un usuario: {str(e)}"}), 500

    
@app.route('/api/user/<int:id>/profile', methods=['GET'])
def user_profile(id):
    
    # Buscar el usuario por el id
    user = db.session.get(User, id) 
    
    # Validar qué pasa si el usuario NO existe
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    # Si existe, usamos método to_dict()
    return jsonify(user.to_dict()), 200  

@app.route('/api/user/<int:id>/close', methods=['DELETE'])
def close_account(id):
    
    # Buscamos al usuario usando la sintaxis moderna de SQLAlchemy 2.0
    # Equivale a: SELECT * FROM user WHERE id = ?;
    user = db.session.get(User, id) 
    
    # Validamos si el usuario realmente existe en la base de datos
    if not user:
        return jsonify({"error": "La cuenta que está intentando cerrar no existe"}), 404
    
    try:
        # Preparamos la eliminación del usuario en la sesión
        # Equivale a: DELETE FROM user WHERE id = ?;
        db.session.delete(user) 
        
        # Confirmamos y aplicamos los cambios en la base de datos real
        db.session.commit() 
        
        # Respondemos con éxito
        return jsonify({"mensaje": "Su cuenta ha sido cerrada correctamente"}), 200
        
    except Exception as e:
        # Si la base de datos rechaza la eliminación (ej. porque el usuario 
        # tiene favoritos vinculados y no configuraste el borrado en cascada), 
        # hacemos rollback para evitar que la sesión de la BD colapse.
        db.session.rollback()
        return jsonify({"error": f"Ocurrió un error al intentar cerrar la cuenta: {str(e)}"}), 500

@app.route('/api/newplanet', methods=['POST'])
def register_planet():
    
    # Recibimos los datos enviados en la petición POST
    data = request.get_json()

    # Creamos una instancia vacía del modelo Planet
    planet = Planet()
    
    try:
        # Asignamos los valores a las columnas correspondientes
        # Si falta alguna de estas claves en el JSON, Python lanzará un KeyError
        planet.name = data['name']
        planet.population = data['population']
        planet.size = data['size']

        # Preparamos el objeto en la sesión y guardamos en la base de datos real
        db.session.add(planet)
        db.session.commit()

        # Usamos el código 201 porque estamos creando un nuevo recurso en la base de datos
        return jsonify({"mensaje": "Planeta registrado con éxito"}), 201
        
    except KeyError as e:
        # Atrapamos el error si el frontend olvidó enviar un dato obligatorio
        return jsonify({"error": f"Falta el campo obligatorio: {str(e)}"}), 400
        
    except IntegrityError:
        # Atrapamos el error si se intenta registrar un planeta con un nombre que ya existe
        # Hacemos rollback para limpiar la sesión de la base de datos
        db.session.rollback()
        return jsonify({"error": "Ya existe un planeta registrado con ese nombre"}), 400
        
    except Exception as e:
        # Atrapamos cualquier otro error inesperado para evitar que el servidor se caiga
        db.session.rollback()
        return jsonify({"error": f"Error al intentar registrar el planeta: {str(e)}"}), 500
    
@app.route('/api/planet/<int:id>', methods=['GET'])
def get_planet_with_residents(id):
    
    # Buscamos el planeta en la base de datos por su ID
    # Equivale a: SELECT * FROM planet WHERE id = ?;
    planet = db.session.get(Planet, id)
    
    # Validamos si el planeta realmente existe
    if not planet:
        return jsonify({"error": "El planeta que buscas no existe"}), 404
        
    try:
        # Si existe, devolvemos el diccionario que incluye la lista de residentes
        return jsonify(planet.to_dict()), 200
        
    except Exception as e:
        # Atrapamos cualquier error inesperado del servidor
        return jsonify({"error": f"Error al procesar la solicitud: {str(e)}"}), 500
    
@app.route('/api/planet/<int:id>/close', methods=['DELETE'])
def close_planet(id):
    
    # Buscamos el planeta usando la sintaxis moderna de SQLAlchemy 2.0
    # Equivale a: SELECT * FROM planet WHERE id = ?;
    planet = db.session.get(Planet, id) 
    
    # Validamos si el planeta realmente existe en la base de datos
    if not planet:
        return jsonify({"error": "El planeta que buscas eliminar no existe"}), 404
    
    try:
        # Preparamos la eliminación del planeta en la sesión
        # Equivale a: DELETE FROM planet WHERE id = ?;
        db.session.delete(planet) 
        
        # Confirmamos y aplicamos los cambios en la base de datos real
        db.session.commit() 
        
        # Respondemos con éxito
        return jsonify({"mensaje": "El planeta ha sido eliminado correctamente"}), 200
        
    except Exception as e:
        # Si la base de datos rechaza la eliminación (ej. porque hay usuarios que viven 
        # en este planeta o alguien lo tiene en favoritos), hacemos rollback 
        # para evitar que la sesión de la base de datos colapse.
        db.session.rollback()
        return jsonify({"error": f"Ocurrió un error al intentar eliminar el planeta: {str(e)}"}), 500



@app.route('/api/newfavorite', methods=['POST'])
def agregar_favorito():
    data = request.get_json()

    # Validar que sepamos de qué usuario se trata
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "Falta el user_id"}), 400

    # Extraer los posibles favoritos del request
    fav_planet_id = data.get('fav_planet_id')
    fav_character_id = data.get('fav_character_id')

    # Validar que al menos envíe un planeta o un personaje
    if not fav_planet_id and not fav_character_id:
         return jsonify({"error": "Debes enviar un fav_planet_id o fav_character_id"}), 400

    # Prevenir favoritos duplicados
    # Buscamos si ya existe ese favorito exacto en la base de datos
    favorito_existente = Favorites.query.filter_by(
        user_id=user_id, 
        fav_planet_id=fav_planet_id, 
        fav_character_id=fav_character_id
    ).first()

    if favorito_existente:
        return jsonify({"error": "Este favorito ya existe"}), 400

    # Crear la nueva instancia de Favorito
    nuevo_favorito = Favorites(user_id=user_id)

    # Asignar el planeta o el personaje según lo que haya llegado en el request
    if fav_planet_id:
        nuevo_favorito.fav_planet_id = fav_planet_id
    
    if fav_character_id:
        nuevo_favorito.fav_character_id = fav_character_id

    # Guardar en la base de datos
    try:
        db.session.add(nuevo_favorito)
        db.session.commit()
        return jsonify({"mensaje": "Favorito agregado con éxito"}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500

@app.route('/api/favorites/<int:fav_id>/close', methods=['DELETE'])
def remove_favorite(fav_id):
    
    # Buscar el favorito en la base de datos por su ID
    fav = db.session.get(Favorites, fav_id)

    # Validar si el favorito realmente existe
    if not fav:
        return jsonify({"error": "El favorito no existe o ya fue eliminado"}), 404

    # Eliminarlo y guardar los cambios
    try:
        db.session.delete(fav)
        db.session.commit()
        
        return jsonify({"mensaje": "Favorito eliminado correctamente"}), 200
        
    except Exception as e:
        # Si algo falla en la base de datos, deshacemos la operación
        db.session.rollback()
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500


if __name__ == '__main__':
    app.run()