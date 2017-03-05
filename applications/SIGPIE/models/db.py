# -*- coding: utf-8 -*-


# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL('sqlite://storage.sqlite')
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager, Mail
import datetime
import os

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, hmac_key = Auth.get_or_create_key(), controller = "default", function = "user")
auth.settings.login_next = URL('index')

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------



# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
#raise HTTP(404)

db.define_table('estudiante',
                Field('carnet','string',unique=True),
                Field('nombre','string', requires= IS_NOT_EMPTY()),
                Field('apellido','string',requires= IS_NOT_EMPTY()),
                Field('telefono_habitacion',requires = IS_MATCH('^[212]+[0-9]{7}$',
         error_message='No es un telefono de habitacion')),
                Field('telefono_celular',requires = IS_MATCH('^[414|424|412|416|426]+[0-9]{7}$',
         error_message='No es un telefono celular')),
                Field('cedula',requires = IS_MATCH('^[0-9]{8}$',
         error_message='No es una cedula'),unique=True),
                Field('Correo',requires = IS_MATCH('[^@]+@[^@]+\.[^@]+',
         error_message='No es un correo valido')))

db.define_table('decanato',
                Field('nombre','string',requires=IS_NOT_EMPTY()))

db.define_table('coordinacion',
                Field('nombre', 'string', requires=IS_NOT_EMPTY()),
                Field('decanato', db.decanato, IS_IN_DB(db, db.decanato.id, 'integer')))

db.define_table('carrera',
               Field('codigo',requires= IS_MATCH('^[0-9]{4}'),unique=True),
               Field('nombre','string',requires = IS_NOT_EMPTY()),
               Field('coordinacion', db.coordinacion, IS_IN_DB(db, db.coordinacion.id, 'integer') ) )

db.define_table('maneja_idioma',
               Field('idioma','string',requires = IS_NOT_EMPTY()),
               Field('Nivel','string', requires = IS_NOT_EMPTY()),
               Field('carnet', db.estudiante , IS_IN_DB(db, db.estudiante.id, 'string')))

db.define_table('universidad',
              Field('pais','string',requires= IS_NOT_EMPTY()),
              Field('nombre','string',requires =IS_NOT_EMPTY()))

db.define_table('convenio',
               Field('nombre','string',requires = IS_NOT_EMPTY()))

db.define_table('universidad_convenio',
               Field('universidad', db.universidad,IS_IN_DB(db, db.universidad.id, 'integer' )),
               Field('convenio', db.convenio ,IS_IN_DB(db, db.convenio.id, 'integer' )),
               Field('cupos', 'integer',default=0))

db.define_table('recaudos',
               Field('informe_academico','upload',requires =IS_NOT_EMPTY()),
               Field('carta_motivacion','upload',requires =IS_NOT_EMPTY()),
               Field('curriculum_vitae','upload',requires =IS_NOT_EMPTY()),
               Field('comprobante','upload',requires =IS_NOT_EMPTY()),
               Field('constancias_cv','upload',requires =IS_NOT_EMPTY()),
               Field('flujograma','upload',requires =IS_NOT_EMPTY()),
               Field('programas_de_estudio','upload',requires =IS_NOT_EMPTY()),
               Field('foto','upload',requires =IS_NOT_EMPTY()),
               Field('carnet','upload',requires =IS_NOT_EMPTY()),
               Field('cedula','upload',requires = IS_NOT_EMPTY()),
               Field('estudiante',db.estudiante,IS_IN_DB(db,db.estudiante.id,'integer')))

db.define_table('formulario',
               Field('estudiante',db.estudiante,IS_IN_DB(db,db.estudiante.id,'integer')),
               Field('genero', 'string', requires=IS_NOT_EMPTY() ),
               Field('nacionalidad', 'string', requires=IS_NOT_EMPTY()),
               Field('pasaporte', 'string',requires=IS_NOT_EMPTY()),
               Field('domicilio', 'string', requires=IS_NOT_EMPTY()),
               Field('persona_contacto', 'string', requires=IS_NOT_EMPTY()),
               Field('rel_persona_contacto', 'string', requires=IS_NOT_EMPTY()),
               Field('dir_persona_contacto', 'string', requires=IS_NOT_EMPTY()),
               Field('tlf_persona_contacto', 'string', requires=IS_NOT_EMPTY()),
               Field('email_persona_contacto', 'string', requires=IS_NOT_EMPTY()),
               Field('univ1', db.universidad, IS_IN_DB(db, db.universidad.id, 'integer' )),
               Field('univ2', db.universidad, IS_IN_DB(db, db.universidad.id, 'integer' )),
               Field('carrera', db.carrera, IS_IN_DB(db, db.carrera.id, 'integer')),
               Field('mencion', 'string', requires=IS_NOT_EMPTY()),
               Field('creditos_aprob', 'string', requires=IS_NOT_EMPTY()),
               Field('indice', 'float', requires=IS_NOT_EMPTY()),
               Field('indice_normalizado', 'float', requires=IS_NOT_EMPTY()),
               Field('fecha', 'date', requires=IS_NOT_EMPTY()),
               Field('opinion_coord', 'string', requires=IS_NOT_EMPTY()),
               Field('observaciones_coord', 'string', requires=IS_NOT_EMPTY())
               )

db.define_table('Actividades_complementarias',
              Field('preparador','boolean',default=False),
              Field('becado','boolean',default=False),
              Field('actividad','text'),
              Field('centro_estudiantes','boolean',default=False),
              Field('carnet',db.estudiante, IS_IN_DB(db, db.estudiante.id, 'string')))