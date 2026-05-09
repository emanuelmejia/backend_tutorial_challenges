import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# class MediaType(enum.Enum):
#     IMAGE = "image"
#     AUDIO = "audio"
#     VIDEO = "video"

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    lastname: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    posts: Mapped[list["Post"]] = relationship(back_populates="author")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")
    following: Mapped[list["Follower"]] = relationship(
        back_populates="user_from")
    followers: Mapped[list["Follower"]] = relationship(
        back_populates="user_to")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
    media: Mapped[list["Media"]] = relationship(back_populates="post")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(
        String(500), unique=True, nullable=False)
    # type: Mapped[MediaType] = mapped_column(Enum(MediaType))
    url: Mapped[str] = mapped_column(
        String(500), unique=True, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="media")


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(
        String(1000), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="comments")
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, deferred=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_from: Mapped["User"] = relationship(back_populates="following")
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to: Mapped["User"] = relationship(back_populates="followers")
