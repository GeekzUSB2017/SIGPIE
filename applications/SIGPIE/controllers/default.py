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
		return dict()
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
			nombre=session.usuario["first_name"],
			apellido=session.usuario["last_name"])


			print "se agrego un nuevo usuario"
			redirect(URL('welcome'))

		#ARREGLAR, ESTA DUPLICANDO DATA Y NO ACTUALIZANDO
		else:

			db.estudiante.insert(nombre=session.usuario["first_name"],
			apellido=session.usuario["last_name"])


			print "se actualizo un usuario existente"
			redirect(URL('welcome'))

def logout_cas():
	session.usuario = None
	redirect('https://secure.dst.usb.ve/logout')
