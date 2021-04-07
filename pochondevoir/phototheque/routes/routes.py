from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
import os.path

from ..app import app, login, photos, db

from ..constantes import PHOTOS_PAR_PAGES
from ..modeles.donnees import Photo, Authorship
from ..modeles.utilisateurs import User
from sqlalchemy import or_


@app.route("/")
def accueil():
    """Route et fonction qui gèrent l'affichage de la page d'accueil
    :return : retourne le template de la page d'accueil
    :rtype : template html
    """
    # On récupère les id de toutes les photographies en les classant par ordre ascendant
    # et on limite l'affichage à 5 photographies
    photos_affichees = Photo.query.all()
    photos = Photo.query.order_by(Photo.photo_id.asc()).limit(5).all()
    return render_template("pages/accueil.html", nom="monsite", photos=photos, photos_affichees=photos_affichees)

@app.route("/presentation")
def presentation():
    """Route et fonction qui gèrent l'affichage de la page de présentation du projet
    :return: retourne le template de la page de présentation du projet
    :rtype: template html
    """
    photos_affichees = Photo.query.all()
    return render_template("pages/presentation.html", photos_affichees=photos_affichees)

@app.route("/galerie")
def galerie():
    """Route et fonction qui gèrent l'affichage la page de la galerie d'images des
    photographies présentes dans la base
    :return : la galerie de l'ensemble des photographies présentes référencées dans la base de données
    :rtype : template html
    """
    # On récupère les id de toutes les photographies référencées dans la base
    photos_affichees = Photo.query.all()
    # On établit que la page affichée lors de notre arrivée sur la page de la galerie sera la n°1
    page = request.args.get("page", 1)

    # On établit la numérotation des pages
    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    resultats = []
    titre = "Galerie"

    # On établit l'affichage de photos par page selon le nombre total de photographies référencées
    if photos_affichees :
        resultats = Photo.query.paginate(page=page, per_page=PHOTOS_PAR_PAGES)
    return render_template("pages/galerie.html", nom="monsite", photos_affichees=photos_affichees, titre = titre, resultats = resultats)


@app.route("/index")
def index():
    """Route et fonction qui gèrent la page d'indexation par titre de toutes les photographies présentes dans la base
    :return: retourne l'index par titres des photographies référencées dans la base de données
    :rtype: template html
    """
    # On récupère les id de chacune des photographies référencées dans la base
    # pour pouvoir ensuite afficher leur titre respectif sur la page
    liste_photos = Photo.query.all()
    return render_template("pages/index.html", nom="monsite", liste_photos=liste_photos)

@app.route("/photo/<int:photo_id>")
def photo(photo_id):
    """"Route et fonction qui gère l'affichage d'une photo unique avec sa notice
    :param photo_id: id unique renvoyant à une photographie précise
    :type photo_id: int
    :return: retourne la page d'une photographie précise, en affichant à la fois l'image et sa notice la concernant
    :rtype: template html
    """
    # On récupère l'id unique d'une photographie spécifique pour laquelle on veut accéder à sa notice
    unique_photo = Photo.query.get(photo_id)
    return render_template("pages/photo.html", nom="monsite", photo=unique_photo)

@app.route("/recherche")
def recherche ():
    """Route et fonction qui gèrent la recherche plein texte d'un terme, c'est-à-dire indépendemment de la catégorie
    dans laquelle il est mentionné (dans le titre même, dans la description, dans la date, le mot-clé ou l'auteur)
    :return: retourne la page présentant les résultats de la recherche effectuée dans la barre de recherche
    :rtype: template html
    """
    # On définit la variable motclef pour la recherche et la page affichée par défaut
    # lors de notre arrivée sur la page html
    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats = []
    titre = "Recherche d'images"

    # Selon le mot écrit par l'utilisateur dans la barre de recherche, on recherche dans chaque champ cette
    # chaine de caractères.
    if motclef:
        resultats = Photo.query.filter(
            or_(
                Photo.photo_titre.like("%{}%".format(motclef)),
                Photo.photo_description.like("%{}%".format(motclef)),
                Photo.photo_auteur.like("%{}%".format(motclef)),
                Photo.photo_date.like("%{}%".format(motclef)),
                Photo.photo_orientation.like("%{}%".format(motclef)),
                Photo.photo_tag.like("%{}%".format(motclef))
            )
        ).paginate(page=page, per_page=PHOTOS_PAR_PAGES)
        titre= "Résultats pour la recherche '" + motclef + "'"
    return render_template("pages/recherche.html", resultats=resultats, titre=titre, keyword=motclef)



@app.route("/recherche/tags")
def recherche_tags():
    """Route et fonction qui gèrent la recherche par mot-clés (tags) selon une liste fermée
    :return: retourne la page avec les résultats de la recherche effectuée par mots-clés selon une liste fermée
    :rtype: template html
    """
    resultats=[]
    # On définit la recherche par tags
    tags=request.args.get("tags", None)
    # s'il y a des tags on filtre selon le tag recherché parmi tous les tags référencés dans le champ photo_tag
    if tags:
        resultats=Photo.query.filter(or_(Photo.photo_tag == tags)).all()
    return augmented_render_template("pages/recherche_tags.html", nom="Recherche par mots-clés", resultats=resultats, tags=tags)

def augmented_render_template(template, **kwargs):
    """Fonction qui permet la récupération des données référencées en tant que "tags" et permettant ainsi
     avec la fonction recherche_tags la recherche par mot-clés selon une liste fermée
     :param template: template associé à la fonction recherche_tags
     :type template : template html
     :param kwargs : permets de transmettre une liste d'arguments de longueur variable avec des mots-clés
     :type kwargs : keyword arguments
     :return : retourne le template associé à la fonction recherche_tags
     :rtype : template
     """
    # On récupère toutes les photos
    photos= Photo.query.all()
    # On crée une liste vide qui va contenir les tags
    tags=[]
    # Pour chaque photo on ajoute le mot-clé qui lui est rattaché dans la liste
    for photo in photos :
        tags.append(photo.photo_tag)
    tags=sorted(list(set(tags)))
    return render_template(template, liste_tag=tags, **kwargs)


@app.route("/register", methods=["GET", "POST"])
def inscription():
    """ Route et fonction qui gèrent les inscriptions des nouveaux utilisateur-ices
    :return: retourne la page html permettant l'inscription d'un nouveau utilisateur
    :rtype: template html
    """
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        # On va chercher par chaque champ de la table User les données renseignées par l'utilisateur-ice
        # sur la page html dédiée lors de son inscription
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )

        # Si les champs sont bien renseignés l'inscription est validée et enregistrée puis
        # l'utilisateur-ice est redigé-e vers la page d'accueil de l'application
        if statut is True:
            logout_user()
            flash("Votre inscription a bien été effectuée. Vous pouvez à présent vous identifier.", "success")
            return redirect("/")
        # Sinon un message d'erreur s'affiche et l'inscription n'est pas enregistrée
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")


@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Routes et fonction qui gèrent la connexion des utilisateur-rices à leur compte sur l'application
    :return: retourne la page html permettant la connexion des utilisateur-rices à leur compte
    :rtype: template html
    """
    # Si l'utilisateur courant est bien connecté ce message flash s'affiche
    if current_user.is_authenticated is True:
        flash("Connexion effectuée", "info")
        # et est redirigé vers la page d'accueil
        return redirect("/")
    # Si l'utilisateur renseigne bien les champs de connexion, la connexion est effectuée
    if request.method == "POST":
        # Pour cela on requête la table User pour aller chercher et vérifier les données propres à
        # chaque utilisateur-ice
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Le nom d'utilisateur ou le mot de passe sont incorrects.", "error")

    return render_template("pages/connexion.html")
login.login_view = 'connexion'


@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    """Route et fonction qui gèrent la déconnexion des utilisateur-ices de l'application
     :return: une fois la déconnexion effectuée, l'utilisateur-rice est automatiquement redirigé-e vers la page d'accueil
    :rtype: template html"""
    # Si l'utilisateur-ice est connecté-e et veut se déconnecter en cliquant sur le lien, alors la
    # déconnexion est effectuée
    if current_user.is_authenticated is True:
        logout_user()
    flash("Déconnexion effectuée", "info")
    return redirect("/")




@login_required
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    """ Route et fonction qui gèrent à la fois le téléchargement d'une nouvelle image dans le dossier static
    et l'enregistrement de sa notice dans la base de données
    :return: retroune la page de téléchargement d'une nouvelle photographie et de création de sa notice
             et redirige automatiquement vers la notice de la nouvelle photographie téléchargée
    :rtype: template html
        """
    """
    Pour cette fonction et les suivantes propres aux photographies, je me suis aidée principalement de ces ressources : 
    https://pypi.org/project/Flask-Reuploaded/
    https://flask-uploads.readthedocs.io/en/latest/#configuration
    https://pythonhosted.org/Flask-Uploads/
    https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
    https://stackoverflow.com/questions/44926465/upload-image-in-flask
    https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
    """
    errors = []
    # Si on est en méthode POST cela signifie que le formulaire a été envoyé, et si la photographie
    # correspond bien aux formats de fichiers autorisés...
    if request.method == 'POST' and 'photo' in request.files:
        # ... on récupère les informations renseignées par l'utilisateur-ice dans les
        # différents champs de la notice
        titre = request.form.get("titre", None)
        description = request.form.get("description", None)
        auteur = request.form.get("auteur", None)
        date = request.form.get("date", None)
        tag = request.form.get("tag", None)
        orientation = request.form.get("orientation", None)
        fichier = request.form.get("fichier", None)

        # On décide d'appliquer des contraintes d'obligation et de caractères sur les
        # champs de la notice
        if not titre or len(titre) == 0:
            errors.append("Titre obligatoire.")

        if not auteur or len(auteur) <= 1:
            auteur = "Anonyme"

        if not date :
            date = "Date inconnue"

        if not tag :
            errors.append("Choisissez un motclef.")

        if not orientation :
            errors.append("Choisissez une orientation")

        if not description :
            description = "Cette photographie n'a pas encore de description, n'hésitez pas à en proposer une !"

        # On vérifie que le fichier n'existe pas déjà sous un nom identique dans le dossier img de l'application
        # Documentation : https://www.guru99.com/python-check-if-file-exists.html
        if os.path.isfile("phototheque/static/img/"+str(fichier)):
            errors.append("Ce nom de fichier existe déja, veuillez le télécharger sous un autre nom.")

        if not errors:
            # S'il n'y a pas d'erreur : on fait correspondre pour chaque champ de la table Photo
            # les champs renseignés par l'utilisateur-ice sur la page html de téléchargement
            nouvelle_photo = Photo(
                photo_titre=titre,
                photo_description=description,
                photo_auteur=auteur,
                photo_date=date,
                photo_tag=tag,
                photo_orientation=orientation,
                photo_fichier=fichier
            )

            # On sauvegarde la photographie dans le dossier static/img spécialement configuré pour cela
            photos.save(request.files['photo'])
            # On envoie à la base de données la nouvelle notice photographique et on enregistre
            db.session.add(nouvelle_photo)
            db.session.commit()

            # S'il y a une nouvelle photo alors on crée un lien d'autorité
            if nouvelle_photo:
                # On récupère l'id de la dernière photographie référencée dans la base
                photo = Photo.query.order_by(Photo.photo_id.desc()).limit(1).first()
                # On récupère l'id de l'utilisateur courant authentifié
                # Documentation : https://www.programcreek.com/python/example/99634/flask_login.current_user.id
                #                 https://flask-login.readthedocs.io/en/latest/#flask_login.LoginManager.user_loader
                user = User.query.get(current_user.user_id)
                # On crée un lien d'autorité
                a_ecrit = Authorship(user=user, photo=photo)

            # On envoie dans la base et on enregistre
            db.session.add(a_ecrit)
            db.session.commit()

            flash("Votre photographie a bien été enregistrée dans la base. Nous vous en remercions !")

            # On redirige directement après le téléchargement vers la notice de la photographie en question
            return redirect(url_for("photo", photo_id=photo.photo_id))
    return render_template('pages/uploads.html', errors=errors)

@login_required
@app.route("/update")
def update_accueil():
    """Route et fonction qui permettent l'affichage de la page d'accueil pour pouvoir
    choisir directement la photo à modifier lorsque l'utilisateur-ice est connecté-e
    :return: retourne une page type index permettant de choisir directement une photo à modifier, sans avoir
             besoin de passer par sa notice, même si cette possibiloté reste possible.
    :rtype: template html
    """
    photos = Photo.query.all()
    return render_template("pages/update_accueil.html", nom="monsite", photos=photos)

@login_required
@app.route("/update/<int:photo_id>", methods=['GET', 'POST'])
def edit_notice(photo_id):
    """Route et fonction qui gèrent la modification d'une notice photographique choisie par l'utilisateur et selon
    l'identifiant de la photographie à laquelle appartient la notice.
    :param photo_id: id de la photographie faisant l'objet d'une modification
    :type photo_id: int
    :return: retourne la page permettant soit d'accéder à la suppression de la photo, à son remplacement ou
             d'effectuer une modification simple de sa notice.
    :rtype: template html
    """
    # On recupère l'id de la photographie qu'on veut modifier (remplacement, édition de notice ou suppression)
    photo = Photo.query.get_or_404(photo_id)
    errors = []
    # Si on est en méthode POST le formulaire est envoyé
    if request.method == 'POST':
        # On récupère les informations renseignées par l'utilisateur-ice dans les
        # différents champs de la notice
        titre = request.form.get("titre", None)
        description = request.form.get("description", None)
        auteur = request.form.get("auteur", None)
        date = request.form.get("date", None)
        tag = request.form.get("tag", None)
        orientation = request.form.get("orientation", None)
        # Le champ fichier est ici volontairement omis et n'est utilisé qu'en cas
        # de remplacement

        # On décide d'appliquer des contraintes d'obligation et de caractères pour les champs de la notice
        if not titre or len(titre) == 0:
            errors.append("Titre obligatoire.")

        if not auteur or len(auteur) <= 1:
            auteur = "Anonyme"

        if not date :
            date = "Date inconnue"

        if not tag :
            errors.append("Choisissez un motclef.")

        if not orientation :
            errors.append("Choisissez une orientation.")

        if not description :
            description = "Cette photographie n'a pas encore de description, n'hésitez pas à en proposer une !"


        if not errors:
            # S'il n'y a pas d'erreur, alors pour chaque champ dans la table Photo de la photo modifiée
            # correspond les nouvelles données renseignées dans les champs du formulaire par l'utilisateur-ice
            photo.photo_titre=titre
            photo.photo_description=description
            photo.photo_auteur=auteur
            photo.photo_date=date
            photo.photo_tag=tag
            photo.photo_orientation=orientation


            # On envoie ces modifications dans la base de données (table Photo) et on enregistre
            db.session.add(photo)
            db.session.commit()

            flash("Votre photographie a bien été modifiée.")

        # On redirige automatiquement vers la notice de la photographie modifiée
            return redirect(url_for("photo", photo_id=photo.photo_id))

    return render_template("pages/edition.html", photo=photo, errors=errors)

@login_required
@app.route("/update/<int:photo_id>/replace", methods=['GET', 'POST'])
def replace(photo_id):
    """Route et fonction qui gèrent le remplacement d'une photographie par une autre, sans nécessairement devoir
    modifier sa notice
    :param photo_id: id de la photographie faisant l'objet d'un remplacement
    :type photo_id: int
    :return: retourne la page permettant de remplacer la photographie en question par une autre choisie par l'utilisateur-ice
    :rtype: template html
    """
    # On récupère l'id de la photographie qu'on souhaite remplacer
    photo = Photo.query.get_or_404(photo_id)
    # On réutilise cet id pour supprimer la photo qu'on souhaite remplacer afin de ne pas créer de bug
    # si, par la suite, une autre image possédant le même nom de fichier que la photo remplacée devait être ajoutée
    photo_a_supprimer = photo
    # On opère une jointure grâce à l'id récupéré pour récupérer le nom du fichier à supprimer dans le dossier
    fichier_a_supprimer = photo_a_supprimer.photo_fichier

    errors = []
    # Si la méthode est POST alors le formulaire est envoyé
    # et si le format de la photographie correspond à ceux autorisés...
    if request.method == 'POST' and 'photo' in request.files:
        # On récupère le nom du fichier
        fichier = request.form.get("fichier", None)

        # Par sûreté, on vérifie que le nom du fichier n'est pas porté par un autre fichier du dossier img,
        # sinon erreur
        if os.path.isfile("phototheque/static/img/"+str(fichier)):
            errors.append("Ce nom de fichier existe déja, veuillez le télécharger sous un autre nom.")

        # S'il n'y a pas d'erreur...
        if not errors:
            # ... on met à jour les données des champs fichier et chemin
            # par les nouvelles rentrées par l'utilisateur-ice
            photo.photo_fichier = fichier

            # ... on envoie à la base de données et on sauvegarde
            db.session.add(photo)
            db.session.commit()

            # ... et on supprime l'ancien fichier du dossier img pour ne pas créer d'interférence en cas d'ajout
            # ultérieur d'un fichier du même nom que l'ancien
            os.remove("phototheque/static/img/" + str(fichier_a_supprimer))

            # alors pour finir on sauvegarde la photographie dans le dossier configuré au préalable pour cela
            photos.save(request.files['photo'])
            flash("Votre photographie a bien été remplacée.")

            # et on redirige automatiquement vers la notice de la photo
            return redirect(url_for("photo", photo_id=photo.photo_id))
    return render_template("pages/remplacer.html", photo=photo, errors=errors, fichier_a_supprimer=fichier_a_supprimer)

@login_required
@app.route("/update/<int:photo_id>/delete", methods=['GET', 'POST'])
def delete(photo_id):
    """Route et fonction qui gèrent la suppression d'une photographie du dossier img de l'application
    et de sa notice enregistrée dans la base
    :param photo_id: id de la photographie faisant l'objet d'une suppression
    :type photo_id: int
    :return: retourne la page permettant de confirmer la suppression de la photographie et redirige automatiquement
             vers la page d'accueil
    :rtype: template html
    """
    # On récupère l'id de la photographie dont on souhaite supprimer la notice et l'image
    photo_a_supprimer = Photo.query.get_or_404(photo_id)
    # On opère une jointure grace à l'id récupéré pour récupérer le nom du fichier à supprimer dans le dossier
    fichier_a_supprimer = photo_a_supprimer.photo_fichier

    # Si la méthode est POST cela signifie que le formulaire est envoyé
    if request.method == 'POST':
        # On supprime l'enregistrement de la notice souhaitée de la table Photo
        # (Grâce à la méthode ON DELETE CASCADE le lien d'autorité est supprimé automatiquement)
        db.session.delete(photo_a_supprimer)
        # On sauvegarde
        db.session.commit()

        # On supprime la photo en question du dossier img
        os.remove("phototheque/static/img/" + str(fichier_a_supprimer))

        flash("La photographie a bien été supprimée.")

        # On redirige automatiquement vers la page d'accueil
        return redirect(url_for('accueil'))
    return render_template("pages/supprimer.html", photo=photo_a_supprimer, fichier_a_supprimer=fichier_a_supprimer)




