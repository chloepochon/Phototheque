from warnings import warn

# On configure le nombre de photographies souhaitées par page
PHOTOS_PAR_PAGES = 2

# On configure les formats de photographies autorisées au téléchargement
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tiff'}

SECRET_KEY = "JE SUIS UN SECRET !"
API_ROUTE = "/api"

if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)
