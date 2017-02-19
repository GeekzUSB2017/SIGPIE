#import sys
#sys.path.insert(0, r"/home/gabo/Escritorio/web2py")

# Creacion de objeto Storage (remplazo de un diccionario)
from gluon.storage import Storage


config = Storage(
    db = Storage(),
    mail = Storage(),
    auth = Storage(),
)

# Definir settings para db, auth y mail
config.db.uri = "sqlite://storage.sqlite"
config.db.pool_size = 0
config.db.check_reserved = ["all"]
config.db.migrate_enabled = True

config.mail.sender = "gabo2595@gmail.com"
config.mail.server = "logging"
config.mail.login = "usuario:gabo"


response.title = "DRIC Internacional"
response.description = "DRIC"

response.generic_patterns = ['*']
