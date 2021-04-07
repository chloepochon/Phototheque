from flask import url_for
import datetime

from .. app import db

# On configure le modèle de la table photo
class Photo(db.Model):
    __tablename__ = "photo"
    photo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo_titre = db.Column(db.Text)
    photo_description = db.Column(db.Text)
    photo_auteur = db.Column(db.Text)
    photo_date = db.Column(db.Text)
    photo_tag = db.Column(db.Text)
    photo_orientation = db.Column(db.String(8))
    photo_fichier = db.Column(db.String(64), index=True, unique=True)
    authorships = db.relationship("Authorship", back_populates="photo", cascade="all, delete")



# On configure le modèle de la table Authorship
class Authorship(db.Model):
    __tablename__ = "authorship"
    authorship_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_photo_id = db.Column(db.Integer, db.ForeignKey('photo.photo_id'))
    authorship_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user = db.relationship("User", back_populates="authorships")
    photo = db.relationship("Photo", back_populates="authorships")



