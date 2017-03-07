# -*- coding: utf-8 -*-

from applications.SIGPIE.modules.ubsutils import get_ldap_data
from applications.SIGPIE.modules.ubsutils import random_key

URL_RETORNO = "http%3A%2F%2Flocalhost%3A8000%2FSIGPIE%2Fdefault%2Flogin_cas"


def index():
	return dict()

def about():
	if session.usuario is not None:
		return dict()
	else:
		redirect(URL('index'))


def postularse():
	if session.usuario is not None:

		generos = ('Masculino','Femenino')

		niveles = ('Básico', 'Intermedio', 'Avanzado')

		parentezco = ('Madre', 'Padre', 'Otro Familiar', 'Otro')

		form = SQLFORM.factory(
				Field('carnet', default=session.usuario['usbid'], label='Carnet', writable=False),
				Field('nombres', default=session.usuario['first_name'], label='Nombres', writable=False),
				Field('apellidos', default=session.usuario['last_name'], label='Apellidos', writable=False),
				Field('cedula',default=session.usuario['cedula'], label='Cédula', writable=False),
				Field('telefono_habitacion','string', label='Teléfono habitación'),
				Field('telefono_celular','string', label='Teléfono celular'),
				Field('correo','string', label='Correo'),
				Field('pasaporte','string', label='Pasaporte'),
				Field('genero','string', requires=IS_NULL_OR(IS_IN_SET(generos)), label='Género'),
				Field('nacionalidad','string', label='Nacionalidad'),
				Field('direccion','string', label='Dirección'),
				Field('idioma_destino','string', requires=IS_NULL_OR(IS_IN_DB(db, 'idioma.id', '%(nombre)s')), label='Idioma'),
				Field('oral','string', requires=IS_NULL_OR(IS_IN_SET(niveles)),label='Oral:'),
				Field('escrito','string', requires=IS_NULL_OR(IS_IN_SET(niveles)),label='Escrito:'),
				Field('lectura','string', requires=IS_NULL_OR(IS_IN_SET(niveles)),label='Lectura:'),
				Field('nombres_cont', 'string', label='Nombres del Contacto de emergencia'),
				Field('apellidos_cont', 'string', label='Apellidos del Contacto de emergencia'),
				Field('direccion_cont', 'string', label='Dirección del Contacto'),
				Field('relacion_cont', 'string', requires=IS_NULL_OR(IS_IN_SET(parentezco)),label='Relación con el estudiante'),
				Field('telefono_habitacion_cont', 'string', label='Teléfono de Habitacion del contacto'),
				Field('telefono_celular_cont', 'string', label='Teléfono celular del contacto'),
				Field('correo_cont', 'string', label='Correo del contacto'))

		rows = db(db.estudiante.carnet == session.usuario['usbid']).select()

		estudiante = rows.first()

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
						direccion=form.vars.direccion)
			redirect(URL('form2'))

		return dict(form_estudiante = form)
	else:
		redirect(URL('index'))

def user():
	return dict(login=auth.login())


def register():
	return dict(form=auth.register())

def form2():
	if session.usuario is not None:
		form = SQLFORM(db.informacion_academica)

		if form.process().accepted:
			id_info = form.vars.id

			db(db.estudiante.carnet == session.usuario['usbid']).update(info_academica=id_info)

			redirect(URL('form3'))

		return dict(form_informacion_academica = form)
	else:
		redirect(URL('index'))

def form3():
	if session.usuario is not None:

		actividades = ('Solo Asignaturas','Asignaturas + Proyecto de Grado','Asignaturas + Pasantía Internacional','Doble titulación')

		periodos = ('Primer Semestre (A partir de Septiembre)','Segundo Semestre (A partir de Enero)','Primer y Segundo Semestre (A partir de Enero)')

		form = SQLFORM.factory(
				Field('pais_1', requires=IS_NULL_OR(IS_IN_DB(db, 'pais.id', '%(nombre)s')), label='País'),
				Field('actividad_1', requires=IS_NULL_OR(IS_IN_SET(actividades)), label='Actividad académica'),
				Field('convenio_1', requires=IS_NULL_OR(IS_IN_DB(db, 'convenio.id', '%(nombre)s')), label='Nombre del convenio'),
				Field('periodo_1', requires=IS_NULL_OR(IS_IN_SET(periodos)), label='Período tentativo, según calendario de la universidad de destino'),
				Field('universidad_1','string', requires=IS_NULL_OR(IS_IN_DB(db, 'universidad.id', '%(nombre)s')), label='Universidad de destino'),
				Field('anio_1','string', label='Año académico'),
				Field('pais_2', requires=IS_NULL_OR(IS_IN_DB(db, 'pais.id', '%(nombre)s')), label='País'),
				Field('actividad_2', requires=IS_NULL_OR(IS_IN_SET(actividades)), label='Actividad académica'),
				Field('convenio_2', requires=IS_NULL_OR(IS_IN_DB(db, 'convenio.id', '%(nombre)s')), label='Nombre del convenio'),
				Field('periodo_2', requires=IS_NULL_OR(IS_IN_SET(periodos)), label='Período tentativo, según calendario de la universidad de destino'),
				Field('universidad_2','string', requires=IS_NULL_OR(IS_IN_DB(db, 'universidad.id', '%(nombre)s')), label='Universidad de destino'),
				Field('anio_2','string', label='Año académico')
				)

		# IMPORTANTE: COMO FECHA INICIO Y FECHA FIN ESTOY GUARDANDO EL AÑO, NO LAS FECHAS COMO DEBERÍA SER. ES SOLO PARA PROBAR
		# FALTA LA ACTIVIDAD ACADÉMICA EN LA BASE
		if form.process().accepted:
			# NO DEBERÍA HACER UN QUERY PARA BUSCAR EL ID DE LA UNIVERSIDAD, PORQUE LA UNIVERSIDAD SE DEBERÍA DESPLEGAR POR EL CONVENIO Y EL PAÍS Y ESO TRAE EL ID DE LA TABLA
			# Si eleccionó un país 1 y una universidad 1
			if (form.vars.pais_1 != None and form.vars.universidad_1 != None):
				# Query para saber si ya hay un datos_intercambio igual en la base
				intercambio_1 = db((db.datos_intercambio.univ == form.vars.universidad_1) &
							(db.datos_intercambio.f_inicio == form.vars.anio_1) &
							(db.datos_intercambio.f_fin == form.vars.anio_1)
							).select().first()

				# Si hay un datos_intercambio igual
				if intercambio_1 != None:
					id_intercambio_1 = intercambio_1.id
				else:
					id_intercambio_1 = db.datos_intercambio.insert(
								universidad=form.vars.universidad_1,
								f_inicio=form.vars.anio_1,
								f_fin=form.vars.anio_1)
				db(db.estudiante.carnet == session.usuario['usbid']).update(op_interc_1=id_intercambio_1)

			# Si eleccionó un país 2 y una universidad 2
			if (form.vars.pais_2 != None and form.vars.universidad_2 != None):
				# Query para saber si ya hay un datos_intercambio igual en la base
				intercambio_2 = db((db.datos_intercambio.univ == form.vars.universidad_2) &
							(db.datos_intercambio.f_inicio == form.vars.anio_2) &
							(db.datos_intercambio.f_fin == form.vars.anio_2)
							).select().first()

				# Si hay un datos_intercambio igual
				if intercambio_2 != None:
					id_intercambio_2 = intercambio_2.id
				else:
					id_intercambio_2 = db.datos_intercambio.insert(
								universidad=form.vars.universidad_2,
								f_inicio=form.vars.anio_2,
								f_fin=form.vars.anio_2)
				db(db.estudiante.carnet == session.usuario['usbid']).update(op_interc_2=id_intercambio_2)
		return dict(form_convenio = form)
	else:
		redirect(URL('index'))
def planestudios():
	if session.usuario is not None:
		return dict()
	else:
		redirect(URL('index'))


def welcome():
	if session.usuario is not None:
		return dict(nombre= session.usuario['first_name'])
	else:
		redirect(URL('index'))

def documentos():
	if session.usuario is not None:
		return dict()
	else:
		redirect(URL('index'))

def login_cas():
	if not request.vars.getfirst('ticket'):
		#redirect(URL('error'))
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
		# redirect(URL('error'))

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
		if db(tablaUsuarios.carnet == usbid).isempty():

			db.estudiante.insert(cedula=session.usuario["cedula"],  # Lo insertamos en la base de datos.
			carnet=session.usuario["usbid"],
			nombres=session.usuario["first_name"],
			apellidos=session.usuario["last_name"])


			print "se agrego un nuevo usuario"
			redirect(URL('welcome'))

		#ARREGLAR, ESTA DUPLICANDO DATA Y NO ACTUALIZANDO
		else:

			print "se actualizo un usuario existente"
			redirect(URL('welcome'))

def logout_cas():
	session.usuario = None
	redirect('https://secure.dst.usb.ve/logout')
