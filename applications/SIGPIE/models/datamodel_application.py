# Definir objetos de app (auth, mail, service)
from gluon.tools import Auth, Mail

auth = Auth(db, hmac_key = Auth.get_or_create_key(), controller = "home", function = "user")
auth.settings.login_next = URL('about')



#auth.settings.login_onaccept=URL('/welcome')

#auth.settings.registration_requires_verification = False
#auth.settings.registration_requires_approval1 = False
#auth.settings.reset_password_requires_verification = True

mail = Mail()
mail.settings.sender = config.mail.sender
mail.settings.server = config.mail.server
mail.settings.login = config.mail.login

auth.settings.mailer = mail

auth.define_tables()
