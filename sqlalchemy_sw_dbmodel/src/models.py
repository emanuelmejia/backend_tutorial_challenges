import enum
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
    birthday: Mapped[Date] = mapped_column(
        Date(), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped["Planet"] = relationship(back_populates="residents")
    posts: Mapped[list["Post"]] = relationship(back_populates="author")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")
    favorites: Mapped[list["Favorites"]] = relationship(
        back_populates="user")
    followers: Mapped[list["Favorites"]] = relationship(
        back_populates="fav_character")

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=False)
    size: Mapped[float] = mapped_column(Float, nullable=False)
    residents: Mapped[list["User"]] = relationship(back_populates="planet")
    followers: Mapped[list["Favorites"]] = relationship(
        back_populates="fav_planet")


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    post_text: Mapped[str] = mapped_column(
        String(1000))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
    media: Mapped[list["Media"]] = relationship(back_populates="post")
    likes: Mapped[int] = mapped_column(Integer, default=0)
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False)
    url: Mapped[str] = mapped_column(
        String(500), unique=True, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="media")


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(
        String(1000), nullable=False)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="comments")
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")


class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, deferred=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favorites")
    fav_character_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    fav_character: Mapped["User"] = relationship(back_populates="followers")
    fav_planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    fav_planet: Mapped["Planet"] = relationship(back_populates="followers")
    
