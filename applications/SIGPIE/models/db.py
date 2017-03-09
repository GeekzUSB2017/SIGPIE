# -*- coding: utf-8 -*-
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

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
# raise HTTP(404)

db.define_table('contacto_emergencia',
                Field('nombres', 'string', requires=IS_NOT_EMPTY()),
                Field('apellidos', 'string', requires=IS_NOT_EMPTY()),
                Field('direccion', 'string', requires=IS_NOT_EMPTY()),
                Field('relacion', 'string', requires=IS_NOT_EMPTY()),
                Field('telefono_habitacion', requires=IS_MATCH('^[0-9]{11}$',
                                                               error_message='No es un telefono de habitacion')),
                Field('telefono_celular', requires=IS_MATCH('^[0-9]{11}$',
                                                            error_message='No es un telefono celular')),

                Field('Correo', requires=IS_MATCH('[^@]+@[^@]+\.[^@]+',
                                                  error_message='No es un correo valido')),
                )

db.define_table('decanato',
                Field('nombre', 'string', requires=IS_NOT_EMPTY()),
                format = '%(nombre)s'
                )

db.define_table('coordinacion',
                Field('nombre', 'string', requires=IS_NOT_EMPTY()),
                Field('decanato', db.decanato,
                      requires=IS_IN_DB(db, db.decanato.id, '%(nombre)s', zero=T('choose one')))
                )

db.define_table('carrera',
                Field('codigo', requires=IS_MATCH('^[0-9]{4}'), unique=True),
                Field('nombre', 'string', requires=IS_NOT_EMPTY()),
                Field('coordinacion', db.coordinacion,
                      requires=IS_IN_DB(db, db.coordinacion.id, '%(nombre)s', zero=T('choose one')))
                )

db.define_table('idioma',
                Field('nombre', 'string', requires=IS_NOT_EMPTY()),
                format = '%(nombre)s'
                )

db.define_table('maneja_idioma',
                Field('idioma', db.idioma,
                      requires=IS_IN_DB(db, db.idioma.id,'%(nombre)s')),
                Field('oral', 'string', requires=IS_NOT_EMPTY()),
                Field('escrito', 'string', requires=IS_NOT_EMPTY()),
                Field('lectura', 'string', requires=IS_NOT_EMPTY())
                )

db.define_table('actividades_complementarias',
                Field('preparador', 'boolean', default=False),
                Field('becado', 'boolean', default=False),
                Field('actividad', 'text'),
                Field('centro_estudiantes', 'boolean', default=False)
                )

db.define_table('pais',
                Field('nombre', 'string', requires=IS_NOT_EMPTY()),
                format = '%(nombre)s'
                )

db.define_table('convenio',
                Field('nombre', 'string', requires=IS_NOT_EMPTY()),
                format = '%(nombre)s'
                )

db.define_table('universidad',
                Field('pais', db.pais, requires=IS_IN_DB(db, db.pais.id, '%(nombre)s')),
                Field('nombre', 'string', requires=IS_NOT_EMPTY()),
                Field('convenio', db.convenio, requires=IS_IN_DB(db, db.convenio.id, '%(nombre)s')),
                Field('cupos', 'integer', default=0),
                format = '%(nombre)s'
                )

db.define_table('datos_intercambio',
                Field('univ', db.universidad,
                      requires=IS_IN_DB(db, db.universidad.id, '%(nombre)s')),
                Field('inicio', 'string', requires=IS_NOT_EMPTY()),
                Field('fin', 'string', requires=IS_NOT_EMPTY()),
                Field('actividad', 'string', requires=IS_NOT_EMPTY())
                )

db.define_table('estudiante',
                Field('carnet', 'string', unique=True),
                Field('nombres', 'string', requires=IS_NOT_EMPTY()),
                Field('apellidos', 'string', requires=IS_NOT_EMPTY()),
                Field('cedula', requires=IS_MATCH('^[0-9]{8}$',
                                                  error_message='No es una cedula'), unique=True),
                Field('telefono_habitacion', requires=IS_MATCH('^[0-9]{11}$',
                                                               error_message='No es un telefono de habitacion')),
                Field('telefono_celular', requires=IS_MATCH('^[0-9]{11}$',
                                                            error_message='No es un telefono celular')),

                Field('Correo', requires=IS_MATCH('[^@]+@[^@]+\.[^@]+',
                                                  error_message='No es un correo valido')),
                Field('pasaporte', 'string', requires=IS_NOT_EMPTY()),
                Field('genero', 'string', requires=IS_NOT_EMPTY()),
                Field('nacionalidad', 'string', requires=IS_NOT_EMPTY()),
                Field('direccion', 'string', requires=IS_NOT_EMPTY()),
                Field('contacto_emergencia', db.contacto_emergencia,
                      requires=IS_IN_DB(db, db.contacto_emergencia.id)),
                Field('idioma_destino', db.maneja_idioma,
                      requires=IS_IN_DB(db, db.maneja_idioma.id)),
                Field('redes', 'string'),
                Field('act_comp', db.actividades_complementarias,
                      requires=IS_IN_DB(db, db.actividades_complementarias.id)),
                Field('op_interc_1', db.datos_intercambio,
                      requires=IS_IN_DB(db, db.datos_intercambio.id)),
                Field('op_interc_2', db.datos_intercambio,
                      requires=IS_IN_DB(db, db.datos_intercambio.id)),

                Field('universidad_1', db.universidad,
                      requires=IS_IN_DB(db, db.universidad.id, '%(nombre)s')),
                Field('periodo_1', 'string', requires=IS_NOT_EMPTY()),
                Field('actividad_1', 'string', requires=IS_NOT_EMPTY()),

                Field('universidad_2', db.universidad,
                      requires=IS_IN_DB(db, db.universidad.id, '%(nombre)s')),
                Field('periodo_2', 'string', requires=IS_NOT_EMPTY()),
                Field('actividad_2', 'string', requires=IS_NOT_EMPTY()),

                format = '%(carnet)s'
                )

db.define_table('materia',
                Field('codigo_usb', 'string',),
                Field('materia_usb', 'string',),
                Field('creditos_usb', 'integer'),
                Field('codigo_ext', 'string'),
                Field('materia_ext', 'string'),
                Field('numero_horas','integer'),
                Field('fk_estudiante', db.estudiante, requires=IS_IN_DB(db, db.estudiante.id, '%(nombre)s'))
                )

db.define_table('informacion_academica',
                Field('sede', requires=IS_IN_SET(('Sartenejas','Litoral'), error_message='Debe completar este campo', zero='Seleccione una sede')),
                Field('creditos_aprob', 'integer', requires=IS_NOT_EMPTY(error_message='Debe completar este campo')),
                Field('indice', requires=IS_MATCH('^[0-4].[0-9][0-9][0-9][0-9]|5.0000', error_message='El índice debe estar con el formato: x.xxxx')),
                Field('carrera', db.carrera,
                      requires=IS_IN_DB(db, db.carrera.id, '%(nombre)s', error_message='Debe completar este campo', zero='Seleccione su carrera')),
                Field('decanato', db.decanato,
                      requires=IS_IN_DB(db, db.decanato.id, '%(nombre)s', error_message='Debe completar este campo', zero='Seleccione el decanato')),
                Field('estudiante', db.estudiante, requires=IS_IN_DB(db, db.estudiante.id), writable=False, readable=False)
                )

db.define_table('recaudos',
                Field('informe_academico', 'upload', requires=IS_UPLOAD_FILENAME(extension='^pdf', error_message='Formato de archivo inválido')),
                Field('carta_motivacion', 'upload', requires=IS_UPLOAD_FILENAME(extension='^pdf', error_message='Formato de archivo inválido')),
                Field('curriculum_vitae', 'upload', requires=IS_UPLOAD_FILENAME(extension='^pdf', error_message='Formato de archivo inválido')),
                Field('comprobante', 'upload', requires=IS_UPLOAD_FILENAME(extension='^pdf', error_message='Formato de archivo inválido')),
                Field('constancias_cv', 'upload', requires=IS_UPLOAD_FILENAME(extension='^pdf', error_message='Formato de archivo inválido')),
                Field('flujograma', 'upload', requires=IS_UPLOAD_FILENAME(extension='^pdf', error_message='Formato de archivo inválido')),
                Field('programas_de_estudio', 'upload', requires=IS_UPLOAD_FILENAME(extension='^pdf', error_message='Formato de archivo inválido')),
                Field('foto', 'upload', requires=IS_UPLOAD_FILENAME(extension='^(png|jpg|jpeg)$', error_message='Formato de archivo inválido')),
                Field('carnet', 'upload', requires=IS_UPLOAD_FILENAME(extension='^pdf', error_message='Formato de archivo inválido')),
                Field('cedula', 'upload', requires=IS_UPLOAD_FILENAME(extension='^pdf', error_message='Formato de archivo inválido')),
                Field('actividades_extracurriculares', 'upload', requires=IS_UPLOAD_FILENAME(extension='^pdf', error_message='Formato de archivo inválido')),
                Field('certificado_lengua', 'upload', requires=IS_NULL_OR(IS_UPLOAD_FILENAME(extension='^pdf', error_message='Formato de archivo inválido'))),
                Field('estudiante', db.estudiante, requires=IS_IN_DB(db, db.estudiante.id), writable=False, readable=False)
                )
