# -*- coding: utf-8 -*-



def index():
	return dict()

def about():
	return dict()


def postularse():
	return dict()


def user():
	return dict(login=auth.login())

def register():
	return dict(form=auth.register())


URL_RETORNO = "http%3A%2F%2Flocalhost%3A8000%2FSIGPIE%2Fhome%2Flogin_cas"

# FUNCIONES USUARIO

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
		# session.casticket = request.vars.getfirst('ticket')
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
			redirect(URL('about'))

		#ARREGLAR, ESTA DUPLICANDO DATA Y NO ACTUALIZANDO
		else:

			db.estudiante.insert(nombre=session.usuario["first_name"],
			apellido=session.usuario["last_name"])


			print "se actualizo un usuario existente"
			redirect(URL('about'))
def logout_cas():
	session.usuario = None
	return response.render()




################
# SEPARAR      # Todo esto va a usbutils.py, en SIGPIE/modules, pero me daba error al importar usbutils.py
################


import ldap
import string
import random

# Requiere:
# sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev ldap-utils
# pip install ldap

def get_ldap_data(usbid):
	def getFirst(maybeList):
		# Evitar excepcion de index no encontrado
		if type(maybeList)==list and len(maybeList)>0:
			return maybeList[0]
		else:
			return None

	user = {}
	l    = ldap.open("ldap.usb.ve")
	searchScope        = ldap.SCOPE_SUBTREE
	retrieveAttributes = None #Traemos todos los atributos
	baseDN = "ou=People,dc=usb,dc=ve"
	searchFilter = "uid=*"+usbid+"*"
	ldap_result_id = l.search(baseDN,searchScope,searchFilter,retrieveAttributes)
	result_type, consulta = l.result(ldap_result_id, 0)
	datos = consulta[0][1]

	# print datos

	# Extraer datos evitando campos inexistentes
	user['first_name'] = getFirst(datos.get('givenName'))
	user['last_name']  = getFirst(datos.get('sn'))
	user['email']      = getFirst(datos.get('mail'))
	user['cedula']     = getFirst(datos.get('personalId'))
	user['phone']      = getFirst(datos.get('mobile'))
	user_type          = getFirst(datos.get('gidNumber'))

	if user_type == "1000":
		user['tipo'] = "Docente"
		user['dpto'] = getFirst(datos.get('department'))
	elif user_type == "1002":
		user['tipo'] = "Empleado"
	elif user_type == "1003":
		user['tipo'] = "Organización"
	elif user_type == "1004":
		user['tipo'] = "Pregrado"
		user['carrera'] = getFirst(datos.get('career'))
	elif user_type == "1006":
		user['tipo'] = "Postgrado"
		user['carrera'] = getFirst(datos.get('career'))
	elif user_type == "1007":
		user['tipo'] = "Egresado"
	elif user_type == "1008":
		user['tipo'] = "Administrativo"

	return user

def random_key():
	return ''.join(random.choice(string.ascii_uppercase) for _ in range(20))


