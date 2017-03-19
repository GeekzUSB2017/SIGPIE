# -*- coding: utf-8 -*-

from applications.SIGPIE.modules.ubsutils import get_ldap_data
from applications.SIGPIE.modules.ubsutils import random_key

import datetime

URL_RETORNO = "http%3A%2F%2Flocalhost%3A8000%2FSIGPIE%2Fdefault%2Flogin_cas"



######################################
#            NO BORRAR               #
######################################
def user():
    return dict(login=auth.login())

def register():
    return dict(form=auth.register())
######################################
def expediente():
	return dict()


def index():
	if session.usuario is not None:
		redirect(URL('welcome'))
	else:
		return dict()

def about():
	if session.usuario is not None:
		estudiante = db(db.estudiante.carnet == session.usuario['usbid']).select().first()
		return dict(estudiante = estudiante)
	else:
		redirect(URL('index'))

def renuncia():
	if session.usuario is not None:
		estudiante = db(db.estudiante.carnet == session.usuario['usbid']).select().first()

		if (estudiante.renuncio):
			redirect(URL('renunciar'))
		else:
			form = SQLFORM(db.renuncia, hidden=dict(estudiante=estudiante.id))

			if form.process().accepted:

				id_renuncia = form.vars.id

				db(db.renuncia.id == id_renuncia).update(estudiante=estudiante.id)

				if estudiante.completo:
					db(db.estudiante.id == estudiante.id).update(renuncio=True)
					redirect(URL('renunciar'))
				else:
					response.flash = 'No ha completado el formulario'
					redirect(URL(renuncia))

			return dict(form_renuncia = form)
	else:
		redirect(URL('index'))

def renunciar():
	return dict()

def postularse():
	if session.usuario is not None:

		estudiante = db(db.estudiante.carnet == session.usuario['usbid']).select().first()

		if (estudiante.renuncio):
			redirect(URL('renunciar'))
		else:
			generos = ('Masculino','Femenino')

			niveles = ('Básico', 'Intermedio', 'Avanzado')

			parentezco = ('Madre', 'Padre', 'Representante Legal', 'Otro')

			form = SQLFORM.factory(
					Field('carnet', default=session.usuario['usbid'], label='Carnet', writable=False),
					Field('nombres', default=session.usuario['first_name'], label='Nombres', writable=False),
					Field('apellidos', default=session.usuario['last_name'], label='Apellidos', writable=False),
					Field('cedula',default=session.usuario['cedula'], label='Cédula', writable=False),
					Field('telefono_habitacion','string', label='Teléfono habitación', requires=IS_MATCH('^[0-9]{4}-[0-9]{7}$', error_message='No es un teléfono válido')),
					Field('telefono_celular','string', label='Teléfono celular', requires=IS_MATCH('^[0-9]{4}-[0-9]{7}$', error_message='No es un celular válido')),
					Field('correo','mail', label='Correo', requires=IS_MATCH('[^@]+@[^@]+\.[^@]+',
	                                                  error_message='No es un correo válido')),
					Field('pasaporte','string', label='Pasaporte', requires=IS_MATCH('^[0-9]{9}$', error_message='No es un pasaporte válido')),
					Field('genero','string', requires=IS_IN_SET(generos, error_message='Debe completar este campo', zero = 'Seleccione un género'), label='Género'),
					Field('nacionalidad','string', label='Nacionalidad', requires=IS_NOT_EMPTY(error_message='Debe completar este campo')),
					Field('direccion','string', label='Dirección', requires=IS_NOT_EMPTY(error_message='Debe completar este campo')),
					Field('idioma_destino','string', requires=IS_IN_DB(db, 'idioma.id', '%(nombre)s', zero='Seleccione un idioma',error_message='Debe completar este campo'), label='Idioma'),
					Field('oral','string', requires=IS_IN_SET(niveles, error_message='Debe completar este campo', zero='Seleccione un nivel'),label='Oral:'),
					Field('escrito','string', requires=IS_IN_SET(niveles, error_message='Debe completar este campo', zero='Seleccione un nivel'),label='Escrito:'),
					Field('lectura','string', requires=IS_IN_SET(niveles, error_message='Debe completar este campo', zero='Seleccione un nivel'),label='Lectura:'),
					Field('redes_sociales', 'string', label='Redes sociales'),
					Field('nombres_cont', 'string', label='Nombres del Contacto de emergencia', requires=IS_NOT_EMPTY(error_message='Debe completar este campo')),
					Field('apellidos_cont', 'string', label='Apellidos del Contacto de emergencia', requires=IS_NOT_EMPTY(error_message='Debe completar este campo')),
					Field('direccion_cont', 'string', label='Dirección del Contacto', requires=IS_NOT_EMPTY(error_message='Debe completar este campo')),
					Field('relacion_cont', 'string', requires=IS_IN_SET(parentezco, error_message='Debe completar este campo', zero='Seleccione una relación'),label='Relación con el estudiante'),
					Field('telefono_habitacion_cont', 'string', label='Teléfono de Habitacion del contacto', requires=IS_MATCH('^[0-9]{4}-[0-9]{7}$', error_message='No es un teléfono válido')),
					Field('telefono_celular_cont', 'string', label='Teléfono celular del contacto', requires=IS_MATCH('^[0-9]{4}-[0-9]{7}$', error_message='No es un celular válido')),
					Field('correo_cont', 'string', label='Correo del contacto', requires=IS_MATCH('[^@]+@[^@]+\.[^@]+',
	                                                  error_message='No es un correo valido')))

			# Obtener el manejo del idioma que haga match con el estudiante en sesión
			manejo_idioma = db(db.maneja_idioma.id == estudiante.idioma_destino).select().first()

			# Obtener el contacto de emergencia que haga match con el estudiante en sesión
			contacto_emergencia = db(db.contacto_emergencia.id == estudiante.contacto_emergencia).select().first()

			# Cargar valores de la base de datos
			form.vars.carnet = session.usuario['usbid']
			form.vars.nombres = estudiante.nombres
			form.vars.apellidos = estudiante.apellidos
			form.vars.cedula = estudiante.cedula
			form.vars.telefono_habitacion = estudiante.telefono_habitacion
			form.vars.telefono_celular = estudiante.telefono_celular
			form.vars.correo = session.usuario['email']
			form.vars.pasaporte = estudiante.pasaporte
			form.vars.genero = estudiante.genero
			form.vars.nacionalidad = estudiante.nacionalidad
			form.vars.direccion = estudiante.direccion
			form.vars.redes_sociales = estudiante.redes

			# Si el estudiante tiene un manejo de idioma, lo cargo
			if (manejo_idioma != None):
				form.vars.idioma_destino = db(db.idioma.id == manejo_idioma.idioma).select().first().id
				form.vars.oral = manejo_idioma.oral
				form.vars.escrito = manejo_idioma.escrito
				form.vars.lectura = manejo_idioma.lectura

			# Si el estudiante tiene un contacto de emergencia, lo cargo
			if (contacto_emergencia != None):
				form.vars.nombres_cont = contacto_emergencia.nombres
				form.vars.apellidos_cont = contacto_emergencia.apellidos
				form.vars.direccion_cont = contacto_emergencia.direccion
				form.vars.relacion_cont = contacto_emergencia.relacion
				form.vars.telefono_habitacion_cont = contacto_emergencia.telefono_habitacion
				form.vars.telefono_celular_cont = contacto_emergencia.telefono_celular
				form.vars.correo_cont = contacto_emergencia.Correo

			if form.process().accepted:
				# Si todos los campos del idioma no están vacíos
				if (form.vars.idioma_destino != None and form.vars.oral != '' and	form.vars.escrito != '' and	form.vars.lectura != ''):
					# Query para ver si ya existe un manejo_idioma igual en la base
					idioma = db((db.maneja_idioma.idioma == form.vars.idioma_destino) &
								(db.maneja_idioma.oral == form.vars.oral) &
								(db.maneja_idioma.escrito == form.vars.escrito) &
								(db.maneja_idioma.lectura == form.vars.lectura)
								).select().first()
					# Si el manejo_idioma ya está guardado
					if idioma != None:
						id_manejo = idioma.id
					else:
						id_manejo = db.maneja_idioma.insert(idioma=form.vars.idioma_destino, oral=form.vars.oral, escrito=form.vars.escrito,lectura=form.vars.lectura)
					# Actualizar el idioma_destino del estudiante en sesión
					db(db.estudiante.carnet == session.usuario['usbid']).update(idioma_destino=id_manejo)
				# Si todos los campos del contacto de emergencia son llenados, actualizo la tabla
				if (form.vars.nombres_cont != '' and form.vars.apellidos_cont != '' and	form.vars.direccion_cont != '' and form.vars.relacion_cont != '' and form.vars.telefono_habitacion_cont != '' and form.vars.telefono_celular_cont != '' and	form.vars.correo_cont != ''):
					# Query para ver si ya existe un contacto de emergencia igual en la base
					contacto = db((db.contacto_emergencia.nombres == form.vars.nombres_cont) &
								(db.contacto_emergencia.apellidos == form.vars.apellidos_cont) &
								(db.contacto_emergencia.direccion == form.vars.direccion_cont) &
								(db.contacto_emergencia.relacion == form.vars.relacion_cont) &
								(db.contacto_emergencia.telefono_habitacion == form.vars.telefono_habitacion_cont) &
								(db.contacto_emergencia.telefono_celular == form.vars.telefono_celular_cont) &
								(db.contacto_emergencia.Correo == form.vars.correo_cont)
								).select().first()
					# Si el contacto ya está guardado
					if contacto != None:
						id_contacto_emer = contacto.id
					else:
						id_contacto_emer = db.contacto_emergencia.insert(
									nombres=form.vars.nombres_cont,
									apellidos=form.vars.apellidos_cont,
									direccion=form.vars.direccion_cont,
									relacion=form.vars.relacion_cont,
									telefono_habitacion=form.vars.telefono_habitacion_cont,
									telefono_celular=form.vars.telefono_celular_cont,
									Correo=form.vars.correo_cont)
					db(db.estudiante.carnet == session.usuario['usbid']).update(contacto_emergencia=id_contacto_emer)
				# Actualizar los datos del estudiante en sesión
				db(db.estudiante.carnet == session.usuario['usbid']).update(
							telefono_habitacion=form.vars.telefono_habitacion,
							telefono_celular=form.vars.telefono_celular,
							Correo=form.vars.correo,
							pasaporte=form.vars.pasaporte,
							genero=form.vars.genero,
							nacionalidad=form.vars.nacionalidad,
							direccion=form.vars.direccion,
							redes=form.vars.redes_sociales)
				redirect(URL('form2'))

			return dict(form_estudiante = form, estudiante = estudiante)
	else:
		redirect(URL('index'))

def user():
	return dict(login=auth.login())

def register():
	return dict(form=auth.register())

def form2():
	if session.usuario is not None:
		estudiante = db(db.estudiante.carnet == session.usuario['usbid']).select().first()

		if (estudiante.renuncio):
			redirect(URL('renunciar'))
		else:
			informacion = db(db.informacion_academica.estudiante == estudiante.id).select().first()

			if informacion != None:
				record = db.informacion_academica(informacion.id)
				form = SQLFORM(db.informacion_academica, record, hidden=dict(estudiante=estudiante.id))
			else:
				form = SQLFORM(db.informacion_academica, hidden=dict(estudiante=estudiante.id))

			if form.process().accepted:
				id_info = form.vars.id

				db(db.informacion_academica.id == id_info).update(estudiante=estudiante.id)

				redirect(URL('form3'))

			return dict(form_informacion_academica = form, estudiante = estudiante)
	else:
		redirect(URL('index'))

def form3():
	if session.usuario is not None:

		estudiante = db(db.estudiante.carnet == session.usuario['usbid']).select().first()

		if (estudiante.renuncio):
			redirect(URL('renunciar'))
		else:

			actividades = ('Solo Asignaturas','Asignaturas + Proyecto de Grado','Asignaturas + Pasantía','Doble Titulación')

			periodos = ('Primer Semestre (A partir de Septiembre)','Segundo Semestre (A partir de Enero)','Año Académico')

			form = SQLFORM.factory(
					Field('pais_1', requires=IS_IN_DB(db, 'pais.id', '%(nombre)s', error_message='Debe completar este campo', zero='Seleccione un país'), label='País'),
					Field('convenio_1', requires=IS_IN_DB(db, 'convenio.id', '%(nombre)s', error_message='Debe completar este campo', zero='Seleccione un convenio'), label='Nombre del convenio'),
					Field('universidad_1','string', requires=IS_IN_DB(db, 'universidad.id', '%(nombre)s', error_message='Debe completar este campo', zero='Seleccione una universidad'), label='Universidad de destino'),
					Field('actividad_1', requires=IS_IN_SET(actividades, error_message='Debe completar este campo', zero='Seleccione el tipo de actividad académica'), label='Actividad académica'),
					Field('periodo_1', requires=IS_IN_SET(periodos, error_message='Debe completar este campo', zero='Seleccione un período tentativo'), label='Período tentativo, según calendario de la universidad de destino'),

					Field('pais_2', requires=IS_IN_DB(db, 'pais.id', '%(nombre)s', error_message='Debe completar este campo', zero='Seleccione un país'), label='País'),
					Field('convenio_2', requires=IS_IN_DB(db, 'convenio.id', '%(nombre)s', error_message='Debe completar este campo', zero='Seleccione un convenio'), label='Nombre del convenio'),
					Field('universidad_2','string', requires=IS_IN_DB(db, 'universidad.id', '%(nombre)s', error_message='Debe completar este campo', zero='Seleccione una universidad'), label='Universidad de destino'),
					Field('actividad_2', requires=IS_IN_SET(actividades, error_message='Debe completar este campo', zero='Seleccione el tipo de actividad académica'), label='Actividad académica'),
					Field('periodo_2', requires=IS_IN_SET(periodos, error_message='Debe completar este campo', zero='Seleccione un período tentativo'), label='Período tentativo, según calendario de la universidad de destino')
					)

			# Cargar valores de la base de datos
			if (estudiante.universidad_1 != None):
				form.vars.pais_1 = estudiante.universidad_1.pais
				form.vars.convenio_1 = estudiante.universidad_1.convenio
				form.vars.universidad_1 = estudiante.universidad_1
				form.vars.actividad_1 = estudiante.actividad_1
				form.vars.periodo_1 = estudiante.periodo_1

			if (estudiante.universidad_2 != None):
				form.vars.pais_2 = estudiante.universidad_2.pais
				form.vars.convenio_2 = estudiante.universidad_2.convenio
				form.vars.universidad_2 = estudiante.universidad_2
				form.vars.actividad_2 = estudiante.actividad_2
				form.vars.periodo_2 = estudiante.periodo_2

			if form.process().accepted:
				db(db.estudiante.carnet == session.usuario['usbid']).update(
							universidad_1=form.vars.universidad_1,
							periodo_1=form.vars.periodo_1,
							actividad_1=form.vars.actividad_1,

							universidad_2=form.vars.universidad_2,
							periodo_2=form.vars.periodo_2,
							actividad_2=form.vars.actividad_2)
				redirect(URL('planestudios'))
			return dict(form_convenio = form, estudiante = estudiante)
	else:
		redirect(URL('index'))

def planestudios():
	if session.usuario is not None:

		estudiante = db(db.estudiante.carnet == session.usuario['usbid']).select().first()

		if (estudiante.renuncio):
			redirect(URL('renunciar'))
		else:

			form = SQLFORM.factory(
					Field('codigo_usb_1', 'string', requires=IS_NOT_EMPTY(error_message = 'Debe completar este campo'), label='Código'),
					Field('materia_usb_1', 'string', requires=IS_NOT_EMPTY(error_message = 'Debe completar este campo'), label='Denominación'),
					Field('creditos_usb_1', 'integer', requires=IS_NOT_EMPTY(error_message = 'Debe completar este campo'), label='N° de créditos'),
					Field('codigo_ext_1', 'string', requires=IS_NOT_EMPTY(error_message = 'Debe completar este campo'), label='Código'),
					Field('materia_ext_1', 'string', requires=IS_NOT_EMPTY(error_message = 'Debe completar este campo'), label='Denominación'),
					Field('numero_horas_1', 'integer', requires=IS_NOT_EMPTY(error_message = 'Debe completar este campo'), label='N° de créditos/N° de horas x semana'),

					Field('codigo_usb_2', 'string', label='Código'),
					Field('materia_usb_2', 'string', label='Denominación'),
					Field('creditos_usb_2', 'integer', label='N° de créditos'),
					Field('codigo_ext_2', 'string', label='Código'),
					Field('materia_ext_2', 'string', label='Denominación'),
					Field('numero_horas_2', 'integer', label='N° de créditos/N° de horas x semana'),

					Field('codigo_usb_3', 'string', label='Código'),
					Field('materia_usb_3', 'string', label='Denominación'),
					Field('creditos_usb_3', 'integer', label='N° de créditos'),
					Field('codigo_ext_3', 'string', label='Código'),
					Field('materia_ext_3', 'string', label='Denominación'),
					Field('numero_horas_3', 'integer', label='N° de créditos/N° de horas x semana'),

					Field('codigo_usb_4', 'string', label='Código'),
					Field('materia_usb_4', 'string', label='Denominación'),
					Field('creditos_usb_4', 'integer', label='N° de créditos'),
					Field('codigo_ext_4', 'string', label='Código'),
					Field('materia_ext_4', 'string', label='Denominación'),
					Field('numero_horas_4', 'integer', label='N° de créditos/N° de horas x semana'),

					Field('codigo_usb_5', 'string', label='Código'),
					Field('materia_usb_5', 'string', label='Denominación'),
					Field('creditos_usb_5', 'integer', label='N° de créditos'),
					Field('codigo_ext_5', 'string', label='Código'),
					Field('materia_ext_5', 'string', label='Denominación'),
					Field('numero_horas_5', 'integer', label='N° de créditos/N° de horas x semana'),

					Field('codigo_usb_6', 'string', label='Código'),
					Field('materia_usb_6', 'string', label='Denominación'),
					Field('creditos_usb_6', 'integer', label='N° de créditos'),
					Field('codigo_ext_6', 'string', label='Código'),
					Field('materia_ext_6', 'string', label='Denominación'),
					Field('numero_horas_6', 'integer', label='N° de créditos/N° de horas x semana'),

					Field('codigo_usb_7', 'string', label='Código'),
					Field('materia_usb_7', 'string', label='Denominación'),
					Field('creditos_usb_7', 'integer', label='N° de créditos'),
					Field('codigo_ext_7', 'string', label='Código'),
					Field('materia_ext_7', 'string', label='Denominación'),
					Field('numero_horas_7', 'integer', label='N° de créditos/N° de horas x semana'),

					Field('codigo_usb_8', 'string', label='Código'),
					Field('materia_usb_8', 'string', label='Denominación'),
					Field('creditos_usb_8', 'integer', label='N° de créditos'),
					Field('codigo_ext_8', 'string', label='Código'),
					Field('materia_ext_8', 'string', label='Denominación'),
					Field('numero_horas_8', 'integer', label='N° de créditos/N° de horas x semana'),

					Field('codigo_usb_9', 'string', label='Código'),
					Field('materia_usb_9', 'string', label='Denominación'),
					Field('creditos_usb_9', 'integer', label='N° de créditos'),
					Field('codigo_ext_9', 'string', label='Código'),
					Field('materia_ext_9', 'string', label='Denominación'),
					Field('numero_horas_9', 'integer', label='N° de créditos/N° de horas x semana'),

					Field('codigo_usb_10', 'string', label='Código'),
					Field('materia_usb_10', 'string', label='Denominación'),
					Field('creditos_usb_10', 'integer', label='N° de créditos'),
					Field('codigo_ext_10', 'string', label='Código'),
					Field('materia_ext_10', 'string', label='Denominación'),
					Field('numero_horas_10', 'integer', label='N° de créditos/N° de horas x semana'),

					Field('codigo_usb_11', 'string', label='Código'),
					Field('materia_usb_11', 'string', label='Denominación'),
					Field('creditos_usb_11', 'integer', label='N° de créditos'),
					Field('codigo_ext_11', 'string', label='Código'),
					Field('materia_ext_11', 'string', label='Denominación'),
					Field('numero_horas_11', 'integer', label='N° de créditos/N° de horas x semana'),

					Field('codigo_usb_12', 'string', label='Código'),
					Field('materia_usb_12', 'string', label='Denominación'),
					Field('creditos_usb_12', 'integer', label='N° de créditos'),
					Field('codigo_ext_12', 'string', label='Código'),
					Field('materia_ext_12', 'string', label='Denominación'),
					Field('numero_horas_12', 'integer', label='N° de créditos/N° de horas x semana')
					)

			estudiante = db(db.estudiante.carnet == session.usuario['usbid']).select().first()

			materias = db(db.materia.fk_estudiante == estudiante.id).select()

			materia_1 = db((db.materia.formulario == 1) &
						(db.materia.fk_estudiante == estudiante.id)).select().first()

			if materia_1 != None:
				form.vars.codigo_usb_1 = materia_1.codigo_usb
				form.vars.materia_usb_1 = materia_1.materia_usb
				form.vars.creditos_usb_1 = materia_1.creditos_usb
				form.vars.codigo_ext_1 = materia_1.codigo_ext
				form.vars.materia_ext_1 = materia_1.materia_ext
				form.vars.numero_horas_1 = materia_1.numero_horas

			materia_2 = db((db.materia.formulario == 2) &
						(db.materia.fk_estudiante == estudiante.id)).select().first()

			if materia_2 != None:
				form.vars.codigo_usb_2 = materia_2.codigo_usb
				form.vars.materia_usb_2 = materia_2.materia_usb
				form.vars.creditos_usb_2 = materia_2.creditos_usb
				form.vars.codigo_ext_2 = materia_2.codigo_ext
				form.vars.materia_ext_2 = materia_2.materia_ext
				form.vars.numero_horas_2 = materia_2.numero_horas

			materia_3 = db((db.materia.formulario == 3) &
						(db.materia.fk_estudiante == estudiante.id)).select().first()

			if materia_3 != None:
				form.vars.codigo_usb_3 = materia_3.codigo_usb
				form.vars.materia_usb_3 = materia_3.materia_usb
				form.vars.creditos_usb_3 = materia_3.creditos_usb
				form.vars.codigo_ext_3 = materia_3.codigo_ext
				form.vars.materia_ext_3 = materia_3.materia_ext
				form.vars.numero_horas_3 = materia_3.numero_horas

			materia_4 = db((db.materia.formulario == 4) &
						(db.materia.fk_estudiante == estudiante.id)).select().first()

			if materia_4 != None:
				form.vars.codigo_usb_4 = materia_4.codigo_usb
				form.vars.materia_usb_4 = materia_4.materia_usb
				form.vars.creditos_usb_4 = materia_4.creditos_usb
				form.vars.codigo_ext_4 = materia_4.codigo_ext
				form.vars.materia_ext_4 = materia_4.materia_ext
				form.vars.numero_horas_4 = materia_4.numero_horas

			materia_5 = db((db.materia.formulario == 5) &
						(db.materia.fk_estudiante == estudiante.id)).select().first()

			if materia_5 != None:
				form.vars.codigo_usb_5 = materia_5.codigo_usb
				form.vars.materia_usb_5 = materia_5.materia_usb
				form.vars.creditos_usb_5 = materia_5.creditos_usb
				form.vars.codigo_ext_5 = materia_5.codigo_ext
				form.vars.materia_ext_5 = materia_5.materia_ext
				form.vars.numero_horas_5 = materia_5.numero_horas

			materia_6 = db((db.materia.formulario == 6) &
						(db.materia.fk_estudiante == estudiante.id)).select().first()

			if materia_6 != None:
				form.vars.codigo_usb_6 = materia_6.codigo_usb
				form.vars.materia_usb_6 = materia_6.materia_usb
				form.vars.creditos_usb_6 = materia_6.creditos_usb
				form.vars.codigo_ext_6 = materia_6.codigo_ext
				form.vars.materia_ext_6 = materia_6.materia_ext
				form.vars.numero_horas_6 = materia_6.numero_horas

			materia_7 = db((db.materia.formulario == 7) &
						(db.materia.fk_estudiante == estudiante.id)).select().first()

			if materia_7 != None:
				form.vars.codigo_usb_7 = materia_7.codigo_usb
				form.vars.materia_usb_7 = materia_7.materia_usb
				form.vars.creditos_usb_7 = materia_7.creditos_usb
				form.vars.codigo_ext_7 = materia_7.codigo_ext
				form.vars.materia_ext_7 = materia_7.materia_ext
				form.vars.numero_horas_7 = materia_7.numero_horas

			materia_8 = db((db.materia.formulario == 8) &
						(db.materia.fk_estudiante == estudiante.id)).select().first()

			if materia_8 != None:
				form.vars.codigo_usb_8 = materia_8.codigo_usb
				form.vars.materia_usb_8 = materia_8.materia_usb
				form.vars.creditos_usb_8 = materia_8.creditos_usb
				form.vars.codigo_ext_8 = materia_8.codigo_ext
				form.vars.materia_ext_8 = materia_8.materia_ext
				form.vars.numero_horas_8 = materia_8.numero_horas

			materia_9 = db((db.materia.formulario == 9) &
						(db.materia.fk_estudiante == estudiante.id)).select().first()

			if materia_9 != None:
				form.vars.codigo_usb_9 = materia_9.codigo_usb
				form.vars.materia_usb_9 = materia_9.materia_usb
				form.vars.creditos_usb_9 = materia_9.creditos_usb
				form.vars.codigo_ext_9 = materia_9.codigo_ext
				form.vars.materia_ext_9 = materia_9.materia_ext
				form.vars.numero_horas_9 = materia_9.numero_horas

			materia_10 = db((db.materia.formulario == 10) &
						(db.materia.fk_estudiante == estudiante.id)).select().first()

			if materia_10 != None:
				form.vars.codigo_usb_10 = materia_10.codigo_usb
				form.vars.materia_usb_10 = materia_10.materia_usb
				form.vars.creditos_usb_10 = materia_10.creditos_usb
				form.vars.codigo_ext_10 = materia_10.codigo_ext
				form.vars.materia_ext_10 = materia_10.materia_ext
				form.vars.numero_horas_10 = materia_10.numero_horas

			materia_11 = db((db.materia.formulario == 11) &
						(db.materia.fk_estudiante == estudiante.id)).select().first()

			if materia_11 != None:
				form.vars.codigo_usb_11 = materia_11.codigo_usb
				form.vars.materia_usb_11 = materia_11.materia_usb
				form.vars.creditos_usb_11 = materia_11.creditos_usb
				form.vars.codigo_ext_11 = materia_11.codigo_ext
				form.vars.materia_ext_11 = materia_11.materia_ext
				form.vars.numero_horas_11 = materia_11.numero_horas

			materia_12 = db((db.materia.formulario == 12) &
						(db.materia.fk_estudiante == estudiante.id)).select().first()

			if materia_12 != None:
				form.vars.codigo_usb_12 = materia_12.codigo_usb
				form.vars.materia_usb_12 = materia_12.materia_usb
				form.vars.creditos_usb_12 = materia_12.creditos_usb
				form.vars.codigo_ext_12 = materia_12.codigo_ext
				form.vars.materia_ext_12 = materia_12.materia_ext
				form.vars.numero_horas_12 = materia_12.numero_horas

			if form.process().accepted:

				if materia_1 != None:
					db((db.materia.formulario == 1) & (db.materia.fk_estudiante == estudiante.id)).update(
								codigo_usb=form.vars.codigo_usb_1,
								materia_usb=form.vars.materia_usb_1,
								creditos_usb=form.vars.creditos_usb_1,
								codigo_ext=form.vars.codigo_ext_1,
								materia_ext=form.vars.materia_ext_1,
								numero_horas=form.vars.numero_horas_1)
				else:
					db.materia.insert(
								formulario=1,
								codigo_usb=form.vars.codigo_usb_1,
								materia_usb=form.vars.materia_usb_1,
								creditos_usb=form.vars.creditos_usb_1,
								codigo_ext=form.vars.codigo_ext_1,
								materia_ext=form.vars.materia_ext_1,
								numero_horas=form.vars.numero_horas_1,
								fk_estudiante=estudiante.id)

				if (form.vars.codigo_usb_2 != '' and
					form.vars.materia_usb_2 != '' and
					form.vars.creditos_usb_2 != '' and
					form.vars.codigo_ext_2 != '' and
					form.vars.materia_ext_2 != '' and
					form.vars.numero_horas_2 != ''):

					if materia_2 != None:
						db((db.materia.formulario == 2) & (db.materia.fk_estudiante == estudiante.id)).update(
									codigo_usb=form.vars.codigo_usb_2,
									materia_usb=form.vars.materia_usb_2,
									creditos_usb=form.vars.creditos_usb_2,
									codigo_ext=form.vars.codigo_ext_2,
									materia_ext=form.vars.materia_ext_2,
									numero_horas=form.vars.numero_horas_2)
					else:
						db.materia.insert(
									formulario=2,
									codigo_usb=form.vars.codigo_usb_2,
									materia_usb=form.vars.materia_usb_2,
									creditos_usb=form.vars.creditos_usb_2,
									codigo_ext=form.vars.codigo_ext_2,
									materia_ext=form.vars.materia_ext_2,
									numero_horas=form.vars.numero_horas_2,
									fk_estudiante=estudiante.id)

				elif (form.vars.codigo_usb_2 == '' and
					form.vars.materia_usb_2 == '' and
					form.vars.creditos_usb_2 == '' and
					form.vars.codigo_ext_2 == '' and
					form.vars.materia_ext_2 == '' and
					form.vars.numero_horas_2 == ''):


					if materia_2 != None:
						db((db.materia.formulario == 2) & (db.materia.fk_estudiante == estudiante.id)).delete()

				else:
					redirect(URL('planestudios'))

				if (form.vars.codigo_usb_3 != '' and
					form.vars.materia_usb_3 != '' and
					form.vars.creditos_usb_3 != '' and
					form.vars.codigo_ext_3 != '' and
					form.vars.materia_ext_3 != '' and
					form.vars.numero_horas_3 != ''):

					if materia_3 != None:
						db((db.materia.formulario == 3) & (db.materia.fk_estudiante == estudiante.id)).update(
									codigo_usb=form.vars.codigo_usb_3,
									materia_usb=form.vars.materia_usb_3,
									creditos_usb=form.vars.creditos_usb_3,
									codigo_ext=form.vars.codigo_ext_3,
									materia_ext=form.vars.materia_ext_3,
									numero_horas=form.vars.numero_horas_3)
					else:
						db.materia.insert(
									formulario=3,
									codigo_usb=form.vars.codigo_usb_3,
									materia_usb=form.vars.materia_usb_3,
									creditos_usb=form.vars.creditos_usb_3,
									codigo_ext=form.vars.codigo_ext_3,
									materia_ext=form.vars.materia_ext_3,
									numero_horas=form.vars.numero_horas_3,
									fk_estudiante=estudiante.id)

				elif (form.vars.codigo_usb_3 == '' and
					form.vars.materia_usb_3 == '' and
					form.vars.creditos_usb_3 == '' and
					form.vars.codigo_ext_3 == '' and
					form.vars.materia_ext_3 == '' and
					form.vars.numero_horas_3 == ''):

					if materia_3 != None:
						db((db.materia.formulario == 3) & (db.materia.fk_estudiante == estudiante.id)).delete()

				else:
					redirect(URL('planestudios'))


				if (form.vars.codigo_usb_4 != '' and
					form.vars.materia_usb_4 != '' and
					form.vars.creditos_usb_4 != '' and
					form.vars.codigo_ext_4 != '' and
					form.vars.materia_ext_4 != '' and
					form.vars.numero_horas_4 != ''):

					if materia_4 != None:
						db((db.materia.formulario == 4) & (db.materia.fk_estudiante == estudiante.id)).update(
									codigo_usb=form.vars.codigo_usb_4,
									materia_usb=form.vars.materia_usb_4,
									creditos_usb=form.vars.creditos_usb_4,
									codigo_ext=form.vars.codigo_ext_4,
									materia_ext=form.vars.materia_ext_4,
									numero_horas=form.vars.numero_horas_4)
					else:
						db.materia.insert(
									formulario=4,
									codigo_usb=form.vars.codigo_usb_4,
									materia_usb=form.vars.materia_usb_4,
									creditos_usb=form.vars.creditos_usb_4,
									codigo_ext=form.vars.codigo_ext_4,
									materia_ext=form.vars.materia_ext_4,
									numero_horas=form.vars.numero_horas_4,
									fk_estudiante=estudiante.id)

				elif (form.vars.codigo_usb_4 == '' and
					form.vars.materia_usb_4 == '' and
					form.vars.creditos_usb_4 == '' and
					form.vars.codigo_ext_4 == '' and
					form.vars.materia_ext_4 == '' and
					form.vars.numero_horas_4 == ''):

					if materia_4 != None:
						db((db.materia.formulario == 4) & (db.materia.fk_estudiante == estudiante.id)).delete()

				else:
					redirect(URL('planestudios'))

				if (form.vars.codigo_usb_5 != '' and
					form.vars.materia_usb_5 != '' and
					form.vars.creditos_usb_5 != '' and
					form.vars.codigo_ext_5 != '' and
					form.vars.materia_ext_5 != '' and
					form.vars.numero_horas_5 != ''):

					if materia_5 != None:
						db((db.materia.formulario == 5) & (db.materia.fk_estudiante == estudiante.id)).update(
									codigo_usb=form.vars.codigo_usb_5,
									materia_usb=form.vars.materia_usb_5,
									creditos_usb=form.vars.creditos_usb_5,
									codigo_ext=form.vars.codigo_ext_5,
									materia_ext=form.vars.materia_ext_5,
									numero_horas=form.vars.numero_horas_5)
					else:
						db.materia.insert(
									formulario=5,
									codigo_usb=form.vars.codigo_usb_5,
									materia_usb=form.vars.materia_usb_5,
									creditos_usb=form.vars.creditos_usb_5,
									codigo_ext=form.vars.codigo_ext_5,
									materia_ext=form.vars.materia_ext_5,
									numero_horas=form.vars.numero_horas_5,
									fk_estudiante=estudiante.id)

				elif (form.vars.codigo_usb_5 == '' and
					form.vars.materia_usb_5 == '' and
					form.vars.creditos_usb_5 == '' and
					form.vars.codigo_ext_5 == '' and
					form.vars.materia_ext_5 == '' and
					form.vars.numero_horas_5 == ''):

					if materia_5 != None:
						db((db.materia.formulario == 5) & (db.materia.fk_estudiante == estudiante.id)).delete()

				else:
					redirect(URL('planestudios'))

				if (form.vars.codigo_usb_6 != '' and
					form.vars.materia_usb_6 != '' and
					form.vars.creditos_usb_6 != '' and
					form.vars.codigo_ext_6 != '' and
					form.vars.materia_ext_6 != '' and
					form.vars.numero_horas_6 != ''):

					if materia_6 != None:
						db((db.materia.formulario == 6) & (db.materia.fk_estudiante == estudiante.id)).update(
									codigo_usb=form.vars.codigo_usb_6,
									materia_usb=form.vars.materia_usb_6,
									creditos_usb=form.vars.creditos_usb_6,
									codigo_ext=form.vars.codigo_ext_6,
									materia_ext=form.vars.materia_ext_6,
									numero_horas=form.vars.numero_horas_6)
					else:
						db.materia.insert(
									formulario=6,
									codigo_usb=form.vars.codigo_usb_6,
									materia_usb=form.vars.materia_usb_6,
									creditos_usb=form.vars.creditos_usb_6,
									codigo_ext=form.vars.codigo_ext_6,
									materia_ext=form.vars.materia_ext_6,
									numero_horas=form.vars.numero_horas_6,
									fk_estudiante=estudiante.id)

				elif (form.vars.codigo_usb_6 == '' and
					form.vars.materia_usb_6 == '' and
					form.vars.creditos_usb_6 == '' and
					form.vars.codigo_ext_6 == '' and
					form.vars.materia_ext_6 == '' and
					form.vars.numero_horas_6 == ''):

					if materia_6 != None:
						db((db.materia.formulario == 6) & (db.materia.fk_estudiante == estudiante.id)).delete()

				else:
					redirect(URL('planestudios'))

				if (form.vars.codigo_usb_7 != '' and
					form.vars.materia_usb_7 != '' and
					form.vars.creditos_usb_7 != '' and
					form.vars.codigo_ext_7 != '' and
					form.vars.materia_ext_7 != '' and
					form.vars.numero_horas_7 != ''):

					if materia_7 != None:
						db((db.materia.formulario == 7) & (db.materia.fk_estudiante == estudiante.id)).update(
									codigo_usb=form.vars.codigo_usb_7,
									materia_usb=form.vars.materia_usb_7,
									creditos_usb=form.vars.creditos_usb_7,
									codigo_ext=form.vars.codigo_ext_7,
									materia_ext=form.vars.materia_ext_7,
									numero_horas=form.vars.numero_horas_7)
					else:
						db.materia.insert(
									formulario=7,
									codigo_usb=form.vars.codigo_usb_7,
									materia_usb=form.vars.materia_usb_7,
									creditos_usb=form.vars.creditos_usb_7,
									codigo_ext=form.vars.codigo_ext_7,
									materia_ext=form.vars.materia_ext_7,
									numero_horas=form.vars.numero_horas_7,
									fk_estudiante=estudiante.id)

				elif (form.vars.codigo_usb_7 == '' and
					form.vars.materia_usb_7 == '' and
					form.vars.creditos_usb_7 == '' and
					form.vars.codigo_ext_7 == '' and
					form.vars.materia_ext_7 == '' and
					form.vars.numero_horas_7 == ''):

					if materia_7 != None:
						db((db.materia.formulario == 7) & (db.materia.fk_estudiante == estudiante.id)).delete()

				else:
					redirect(URL('planestudios'))

				if (form.vars.codigo_usb_8 != '' and
					form.vars.materia_usb_8 != '' and
					form.vars.creditos_usb_8 != '' and
					form.vars.codigo_ext_8 != '' and
					form.vars.materia_ext_8 != '' and
					form.vars.numero_horas_8 != ''):

					if materia_8 != None:
						db((db.materia.formulario == 8) & (db.materia.fk_estudiante == estudiante.id)).update(
									codigo_usb=form.vars.codigo_usb_8,
									materia_usb=form.vars.materia_usb_8,
									creditos_usb=form.vars.creditos_usb_8,
									codigo_ext=form.vars.codigo_ext_8,
									materia_ext=form.vars.materia_ext_8,
									numero_horas=form.vars.numero_horas_8)
					else:
						db.materia.insert(
									formulario=8,
									codigo_usb=form.vars.codigo_usb_8,
									materia_usb=form.vars.materia_usb_8,
									creditos_usb=form.vars.creditos_usb_8,
									codigo_ext=form.vars.codigo_ext_8,
									materia_ext=form.vars.materia_ext_8,
									numero_horas=form.vars.numero_horas_8,
									fk_estudiante=estudiante.id)

				elif (form.vars.codigo_usb_8 == '' and
					form.vars.materia_usb_8 == '' and
					form.vars.creditos_usb_8 == '' and
					form.vars.codigo_ext_8 == '' and
					form.vars.materia_ext_8 == '' and
					form.vars.numero_horas_8 == ''):

					if materia_8 != None:
						db((db.materia.formulario == 8) & (db.materia.fk_estudiante == estudiante.id)).delete()

				else:
					redirect(URL('planestudios'))

				if (form.vars.codigo_usb_9 != '' and
					form.vars.materia_usb_9 != '' and
					form.vars.creditos_usb_9 != '' and
					form.vars.codigo_ext_9 != '' and
					form.vars.materia_ext_9 != '' and
					form.vars.numero_horas_9 != ''):

					if materia_9 != None:
						db((db.materia.formulario == 9) & (db.materia.fk_estudiante == estudiante.id)).update(
									codigo_usb=form.vars.codigo_usb_9,
									materia_usb=form.vars.materia_usb_9,
									creditos_usb=form.vars.creditos_usb_9,
									codigo_ext=form.vars.codigo_ext_9,
									materia_ext=form.vars.materia_ext_9,
									numero_horas=form.vars.numero_horas_9)
					else:
						db.materia.insert(
									formulario=9,
									codigo_usb=form.vars.codigo_usb_9,
									materia_usb=form.vars.materia_usb_9,
									creditos_usb=form.vars.creditos_usb_9,
									codigo_ext=form.vars.codigo_ext_9,
									materia_ext=form.vars.materia_ext_9,
									numero_horas=form.vars.numero_horas_9,
									fk_estudiante=estudiante.id)

				elif (form.vars.codigo_usb_9 == '' and
					form.vars.materia_usb_9 == '' and
					form.vars.creditos_usb_9 == '' and
					form.vars.codigo_ext_9 == '' and
					form.vars.materia_ext_9 == '' and
					form.vars.numero_horas_9 == ''):

					if materia_9 != None:
						db((db.materia.formulario == 9) & (db.materia.fk_estudiante == estudiante.id)).delete()

				else:
					redirect(URL('planestudios'))

				if (form.vars.codigo_usb_10 != '' and
					form.vars.materia_usb_10 != '' and
					form.vars.creditos_usb_10 != '' and
					form.vars.codigo_ext_10 != '' and
					form.vars.materia_ext_10 != '' and
					form.vars.numero_horas_10 != ''):

					if materia_10 != None:
						db((db.materia.formulario == 10) & (db.materia.fk_estudiante == estudiante.id)).update(
									codigo_usb=form.vars.codigo_usb_10,
									materia_usb=form.vars.materia_usb_10,
									creditos_usb=form.vars.creditos_usb_10,
									codigo_ext=form.vars.codigo_ext_10,
									materia_ext=form.vars.materia_ext_10,
									numero_horas=form.vars.numero_horas_10)
					else:
						db.materia.insert(
									formulario=10,
									codigo_usb=form.vars.codigo_usb_10,
									materia_usb=form.vars.materia_usb_10,
									creditos_usb=form.vars.creditos_usb_10,
									codigo_ext=form.vars.codigo_ext_10,
									materia_ext=form.vars.materia_ext_10,
									numero_horas=form.vars.numero_horas_10,
									fk_estudiante=estudiante.id)

				elif (form.vars.codigo_usb_10 == '' and
					form.vars.materia_usb_10 == '' and
					form.vars.creditos_usb_10 == '' and
					form.vars.codigo_ext_10 == '' and
					form.vars.materia_ext_10 == '' and
					form.vars.numero_horas_10 == ''):

					if materia_10 != None:
						db((db.materia.formulario == 10) & (db.materia.fk_estudiante == estudiante.id)).delete()

				else:
					redirect(URL('planestudios'))

				if (form.vars.codigo_usb_11 != '' and
					form.vars.materia_usb_11 != '' and
					form.vars.creditos_usb_11 != '' and
					form.vars.codigo_ext_11 != '' and
					form.vars.materia_ext_11 != '' and
					form.vars.numero_horas_11 != ''):

					if materia_11 != None:
						db((db.materia.formulario == 11) & (db.materia.fk_estudiante == estudiante.id)).update(
									codigo_usb=form.vars.codigo_usb_11,
									materia_usb=form.vars.materia_usb_11,
									creditos_usb=form.vars.creditos_usb_11,
									codigo_ext=form.vars.codigo_ext_11,
									materia_ext=form.vars.materia_ext_11,
									numero_horas=form.vars.numero_horas_11)
					else:
						db.materia.insert(
									formulario=11,
									codigo_usb=form.vars.codigo_usb_11,
									materia_usb=form.vars.materia_usb_11,
									creditos_usb=form.vars.creditos_usb_11,
									codigo_ext=form.vars.codigo_ext_11,
									materia_ext=form.vars.materia_ext_11,
									numero_horas=form.vars.numero_horas_11,
									fk_estudiante=estudiante.id)

				elif (form.vars.codigo_usb_11 == '' and
					form.vars.materia_usb_11 == '' and
					form.vars.creditos_usb_11 == '' and
					form.vars.codigo_ext_11 == '' and
					form.vars.materia_ext_11 == '' and
					form.vars.numero_horas_11 == ''):

					if materia_11 != None:
						db((db.materia.formulario == 11) & (db.materia.fk_estudiante == estudiante.id)).delete()

				else:
					redirect(URL('planestudios'))

				if (form.vars.codigo_usb_12 != '' and
					form.vars.materia_usb_12 != '' and
					form.vars.creditos_usb_12 != '' and
					form.vars.codigo_ext_12 != '' and
					form.vars.materia_ext_12 != '' and
					form.vars.numero_horas_12 != ''):

					if materia_12 != None:
						db((db.materia.formulario == 12) & (db.materia.fk_estudiante == estudiante.id)).update(
									codigo_usb=form.vars.codigo_usb_12,
									materia_usb=form.vars.materia_usb_12,
									creditos_usb=form.vars.creditos_usb_12,
									codigo_ext=form.vars.codigo_ext_12,
									materia_ext=form.vars.materia_ext_12,
									numero_horas=form.vars.numero_horas_12)
					else:
						db.materia.insert(
									formulario=12,
									codigo_usb=form.vars.codigo_usb_12,
									materia_usb=form.vars.materia_usb_12,
									creditos_usb=form.vars.creditos_usb_12,
									codigo_ext=form.vars.codigo_ext_12,
									materia_ext=form.vars.materia_ext_12,
									numero_horas=form.vars.numero_horas_12,
									fk_estudiante=estudiante.id)

				elif (form.vars.codigo_usb_12 == '' and
					form.vars.materia_usb_12 == '' and
					form.vars.creditos_usb_12 == '' and
					form.vars.codigo_ext_12 == '' and
					form.vars.materia_ext_12 == '' and
					form.vars.numero_horas_12 == ''):

					if materia_12 != None:
						db((db.materia.formulario == 12) & (db.materia.fk_estudiante == estudiante.id)).delete()

				else:
					redirect(URL('planestudios'))

				redirect(URL('documentos'))
			return dict(form_plan=form, estudiante = estudiante)
	else:
		redirect(URL('index'))

def welcome():
	if session.usuario is not None:
		estudiante = db(db.estudiante.carnet == session.usuario['usbid']).select().first()

		if (estudiante.renuncio):
			redirect(URL('renunciar'))
		else:
			return dict(nombre = session.usuario['first_name'], estudiante = estudiante)
	else:
		redirect(URL('index'))

def documentos():
	if session.usuario is not None:
		estudiante = db(db.estudiante.carnet == session.usuario['usbid']).select().first()

		if (estudiante.renuncio):
			redirect(URL('renunciar'))
		else:
			maneja_idioma = db(db.maneja_idioma.id == estudiante.idioma_destino).select().first()
			idioma = db(db.idioma.id == maneja_idioma.idioma).select().first()
			recaudo = db(db.recaudos.estudiante == estudiante.id).select().first()
			if recaudo != None:
				record = db.recaudos(recaudo.id)
				form = SQLFORM(db.recaudos, record, hidden=dict(estudiante=estudiante.id))
			else:
				form = SQLFORM(db.recaudos, hidden=dict(estudiante=estudiante.id))

			if form.process().accepted:
				id_docs = form.vars.id

				db(db.recaudos.id == id_docs).update(estudiante=estudiante.id)

				db(db.estudiante.id == estudiante.id).update(completo=True)

				redirect(URL('welcome'))


			return dict(form_documentos = form, recaudo = recaudo, idioma = idioma, estudiante = estudiante)
	else:
		redirect(URL('index'))

def login_cas():

	if not request.vars.getfirst('ticket'):
		pass
	try:
		import urllib2, ssl
		ssl._create_default_https_context = ssl._create_unverified_context

		url = "https://secure.dst.usb.ve/validate?ticket="+\
		request.vars.getfirst('ticket') + "&service=" + URL_RETORNO


		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		the_page = response.read()


	except Exception, e:
		print "Exception: "
		print e

	if the_page[0:2] == "no":
		pass
	else:
		data  = the_page.split()
		usbid = data[1]

		usuario = get_ldap_data(usbid) #Se leen los datos del CAS

		tablaUsuarios = db.estudiante

		session.usuario = usuario
		session.usuario['usbid'] = usbid
		try:
			print "Información extraida del CAS: "
			print usuario['usbid']
			print usuario['first_name']
			print usuario['last_name']
			print usuario['email']
			print usuario['cedula']
			print usuario['phone']
			print usuario['tipo']


		except:
			print('Excepción')
		estudiante = db(db.estudiante.carnet == session.usuario['usbid']).select().first()
		if (estudiante != None):
			if (estudiante.renuncio):
				redirect(URL('renunciar'))
			redirect(URL('welcome'))
		else:
			db.estudiante.insert(cedula=session.usuario["cedula"], # Lo insertamos en la base de datos.
								 carnet=session.usuario["usbid"],
								 nombres=session.usuario["first_name"],
								 apellidos=session.usuario["last_name"])
			redirect(URL('welcome'))

def logout_cas():
	session.usuario = None
	redirect('https://secure.dst.usb.ve/logout')

def expediente():
	if session.usuario is not None:
		#Se hace el query correspondiente al estudiante logueado actual para obtener la informacion y llenar el formulario
		estudiante = db(db.estudiante.carnet == session.usuario['usbid']).select().first()

		try:
			from fpdf import Template
		except:
			print "No se ha podido cargar la libreria para la generacion de PDFs: FPDF"
		
		#Se instancia la plantilla de la pagina 1 del formulario de postulacion
		f = Template(format="letter",
		             title="Expediente de Usuario")

		#Se carga la plantilla en formato csv, se especifica que los campos se separaran por ; y 
		#que el . se usa para decimales
		f.parse_csv("formulario.csv", ";", ".")

		#Se agrega una pagina al PDF
		f.add_page()

		#Se empiezan a llenar los campos
		f["apellidos"] = estudiante.apellidos
		f['nombres'] = estudiante.nombres
		f["domicilio"] = estudiante.direccion
		f["carnet"] = estudiante.carnet

		#Se renderiza la pagina
		stuff = open("/tmp/{0}.pdf".format(estudiante.carnet), 'w')
		stuff.write(f.render("./{0}.pdf".format(estudiante.carnet), 'S'))
		stuff.close()
		response.stream("/tmp/{0}.pdf".format(estudiante.carnet))
	else: 
		redirect(URL('index'))