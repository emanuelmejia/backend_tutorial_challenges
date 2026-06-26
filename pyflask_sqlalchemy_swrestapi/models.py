from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Boolean, Integer, Float, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(
        String(120), nullable=False)
    password: Mapped[str] = mapped_column(
        String(200), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped["Planet"] = relationship(back_populates="residents")
    favorites: Mapped[List["Favorites"]] = relationship(
        foreign_keys="[Favorites.user_id]", 
        back_populates="user"
    )
    followers: Mapped[List["Favorites"]] = relationship(
        foreign_keys="[Favorites.fav_character_id]", 
        back_populates="fav_character"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "active": self.active,
            "planet_id": self.planet_id,
            # ¡No se incluye el password por seguridad!

            # Convertimos cada favorito de la lista a diccionario para que quede en la lista
            "favorites": [favorito.to_dict() for favorito in self.favorites],
            # Mostrar quiénes tienen a este personaje como favorito
            "followers": [
                {
                    "follower_id": follower.user.id,
                    "follower_username": follower.user.username,
                    "follower_name": follower.user.name
                }
                for follower in self.followers if follower.user
            ]
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=False)
    size: Mapped[float] = mapped_column(Float, nullable=False)
    residents: Mapped[List["User"]] = relationship(back_populates="planet")
    followers: Mapped[List["Favorites"]] = relationship(back_populates="fav_planet")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "size": self.size,
            
            # Recorremos la relación residents para extraer los datos de cada usuario
            "residents": [
                {
                    "user_id": residente.id,
                    "username": residente.username,
                    "name": residente.name,
                    "email": residente.email
                }
                for residente in self.residents
            ]
        }

class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(
        foreign_keys=[user_id], 
        back_populates="favorites"
    )
    fav_character_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    fav_character: Mapped["User"] = relationship(
        foreign_keys=[fav_character_id], 
        back_populates="followers"
    )
    fav_planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    fav_planet: Mapped["Planet"] = relationship(back_populates="followers")

    def to_dict(self):
        # 1. Iniciamos el diccionario solo con los datos fijos obligatorios
        data = {
            "id": self.id
        }

        # 2. Si tiene un personaje favorito, agregamos su ID y su Nombre
        if self.fav_character_id is not None:
            data["fav_character_id"] = self.fav_character_id
            # Validamos que la relación exista por seguridad antes de pedir el name
            if self.fav_character: 
                data["fav_character_name"] = self.fav_character.name

        # 3. Si tiene un planeta favorito, agregamos su ID y su Nombre
        if self.fav_planet_id is not None:
            data["fav_planet_id"] = self.fav_planet_id
            if self.fav_planet:
                data["fav_planet_name"] = self.fav_planet.name

        return data


    
