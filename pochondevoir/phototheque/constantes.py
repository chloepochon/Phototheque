from warnings import warn

# On configure le nombre de photographies souhaitées par page
PHOTOS_PAR_PAGES = 2

# On configure les formats de photographies autorisés au téléchargement
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tiff'}

# On configure le secret
SECRET_KEY = "JE SUIS UN SECRET !"

if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)

