from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from .constantes import SECRET_KEY
from flask_uploads import IMAGES, configure_uploads, UploadSet

# stockage du chemin vers le fichier courant
chemin_actuel = os.path.dirname(os.path.abspath(__file__))
# stockage du chemin vers le dossier templates
templates = os.path.join(chemin_actuel, "templates")
# stockage du chemin vers le dossier static
statics = os.path.join(chemin_actuel, "static")

# on instancie l'application dans la variable app et on définit les dossiers templates et statics
# en fonction des chemins ci-dessus
app = Flask("monsite",
    template_folder = templates,
    static_folder = statics
)



# On configure le secret
app.config['SECRET_KEY'] = SECRET_KEY
# On configure la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db_histoireObjet'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# On configure grâce à la librairie UploadSet le dossier dans lequel seront stockées les photos téléchargées
photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "phototheque/static/img"
configure_uploads(app, photos)

# On stocke la base de données dans l'objet db qu'on appellera ensuite
db = SQLAlchemy(app)


# On met en place la gestion d'utilisateur-rice-s
login = LoginManager(app)

from .routes import routes

