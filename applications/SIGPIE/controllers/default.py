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

		generos = ('M','F','Otro')

		form = SQLFORM.factory(
				Field('carnet','string', label='Carnet'),
				Field('nombres','string', label='Nombres'),
				Field('apellidos','string', label='Apellidos'),
				Field('cedula','string', label='Cédula'),
				Field('telefono_habitacion','string', label='Teléfono habitación'),
				Field('telefono_celular','string', label='Teléfono celular'),
				Field('correo','string', label='Correo'),
				Field('pasaporte','string', label='Pasaporte'),
				Field('genero','string', requires=IS_NULL_OR(IS_IN_SET(generos)), label='Género'),
				Field('nacionalidad','string', label='Nacionalidad'),
				Field('direccion','string', label='Dirección'),
				Field('idioma_destino','string', requires=IS_NULL_OR(IS_IN_DB(db, 'idioma.id', '%(nombre)s')), label='Idioma'))
				
		rows = db(db.estudiante.carnet == session.usuario['usbid']).select()

		estudiante = rows.first()
		
		# Cargar valores de la base de datos
		form.vars.carnet = estudiante.carnet
		form.vars.nombres = estudiante.nombres
		form.vars.apellidos = estudiante.apellidos
		form.vars.cedula = estudiante.cedula
		form.vars.telefono_habitacion = estudiante.telefono_habitacion
		form.vars.telefono_celular = session.usuario['phone']
		form.vars.correo = session.usuario['email']
		form.vars.pasaporte = estudiante.pasaporte
		form.vars.genero = estudiante.genero
		form.vars.nacionalidad = estudiante.nacionalidad
		form.vars.direccion = estudiante.direccion
		form.vars.idioma_destino = estudiante.idioma_destino

		if form.process().accepted:
			# Actualizar la tabla del estudiante en sesión
			db(db.estudiante.carnet == session.usuario['usbid']).update(
					telefono_habitacion=form.vars.telefono_habitacion,
					telefono_celular=form.vars.telefono_celular,
					Correo=form.vars.correo,
					pasaporte=form.vars.pasaporte,
					genero=form.vars.genero,
					nacionalidad=form.vars.nacionalidad,
					direccion=form.vars.direccion,
					idioma_destino=form.vars.idioma_destino)

		return dict(form_estudiante = form)	
	else:
		redirect(URL('index'))


def user():
	return dict(login=auth.login())


def register():
	return dict(form=auth.register())

def form2():
	if session.usuario is not None:
		return dict()
	else:
		redirect(URL('index'))

def form3():
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
