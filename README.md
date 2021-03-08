# Phototheque "Objet de l'Histoire, histoire de l'Objet."

:camera_flash: **Présentation du projet**

Cette application a été développée par Chloé Pochon à l'occasion d'un devoir réalisé dans le cadre de la deuxième année de master "Technologies numériques appliquées à l'histoire" à l'Ecole nationale des chartes.
 
 A la fois photothèque et application de téléchargement de photographies, il s'appuie sur mon projet photographique réalisé en 2016 dans le cadre de mon BTS en photographie intitulé "Objet de l'Histoire, histoire de l'objet".

:gear: **Les fonctionnalités**

* Une page d'accueil présentant les cinq premières photographies référencées. Elle permet d'effectuer une recherche directement dans la barre de recherche ou par mots-clés. Elle permet aussi la création d'un compte d'utilisateur-ice et le cas échéant à ce ou cette dernière de se connecter afin d'accéder à davantage de fonctionnalités.
* Une page de présentation du projet
* Un index recensant par titre la totalité des photographies référencées dans la base de données et permettant à l'utilisateur-ice d'accéder directement à la notice de la photographie.
* Une galerie d'images qui affiche chacune d'entre elles. En cliquant dessus l'utilisateurice accède à la notice photographique individuelle.
* Des notices individuelles pour chacune des photographies comprenant : un titre, une description, l'auteur-e, la date, un mot-clé, une orientation et bien sûr l'image en tant que telle.

  Une fois indentifié-e, il est possible pour l'utilisateur-ice de : 
  - télécharger une nouvelle photographie en remplissant également sa notice. Pour cela il lui faudra indiquer les champs susmentionnés ainsi que le nom du fichier.     L'utilisateu-rice devra aussi compléter le chemin du fichier.
  - modifier la notice d'une photographie.
  - remplacer une photographie par une autre sans pour autant modifier la notice. Ainsi la photographie remplacée sera toujours rattachée à la même notice.
  - supprimer une photographie ainsi que sa notice.
  > NB : Pour les modifications, les remplacements et suppressions de photographies, l'utilisateur-ice peut accéder à ces fonctionnalités soit par le biais de la page dédiée, soit directement via la notice de la photographie concernée.
  
:desktop_computer: **Installation**
 
 * Via son terminal, l'utilisateur-ice doit créer un environement virtuel dans un dossier de son choix : virtualenv env -p python3
 * L'utilisateur-ice devra installer des packages et libraries : 
  1. Pour cela il doit sourcer son environnement virtuel 
    -> dans le dossier choisi faire la commande source env/bin/activate 
  2.  Puis : 
       - Flask : pip install flask
       - Flask-SQLAlchemy : pip install flask_sqlalchemy
       - Flask-Login : pip install flask-login
       - Flask-Uploads : pip install Flask-Uploads
       - Flask-Reuploaded : pip install Flask-Reuploaded
  3. Vérifier que tout est bien installé : pip freeze
  4. Désactiver l'environnement : deactivate
  
 * Il devra aussi installer SQLite : sudo apt-get install sqlite3
 
 * Enfin l'utilisateur-ice devra cloner le dossier : git clone https://github.com/chloepochon/Phototheque
 
 * Il pourra alors lancer l'application : 
    - Activer l'environnement virtuel : source env/bin/activate
    - Lancer l'application : python run.py
    - Aller sur http://127.0.0.1:5000/ 
    - Pour désactiver : ctrl + c
  
  
