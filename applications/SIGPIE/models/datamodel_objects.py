# -*- coding: utf-8 -*-
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
