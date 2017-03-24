# -*- coding: utf-8 -*-
from applications.SIGPIE.modules.ubsutils import get_ldap_data
from applications.SIGPIE.modules.ubsutils import random_key
import datetime
import cStringIO
import csv
from gluon.sqlhtml import ExportClass
import os

def expediente():

	if session.usuario is not None:
		#Se hace el query correspondiente al estudiante logueado actual para obtener la informacion y llenar el formulario

		try:
			from fpdf import Template
		except:
			print "No se ha podido cargar la libreria para la generacion de PDFs: FPDF"

		#Se instancia la plantilla de la pagina 1 del formulario de postulacion
		f = Template(format="letter",
					 title="Pagina 1 Expediente")

		#Se carga la plantilla en formato csv, se especifica que los campos se separaran por ; y
		#que el . se usa para decimales
		f.parse_csv("./applications/SIGPIE/static/formulario.csv", ";", ".")

		#Se agrega una pagina al PDF
		f.add_page()

		##################################################################
		# REVISAR CUALES CAMPOS PUEDEN SER MULTILINEA Y MODIFICAR EL CSV #
		##################################################################

		#Queries para llenar los campos del formulario
		
		estudiante = db(db.estudiante.carnet == session.usuario['usbid']).select().first()
		recaudos = db(db.recaudos.estudiante == estudiante.id).select().first()
		contacto_emergencia = db(db.contacto_emergencia.id == estudiante.contacto_emergencia).select().first()
		manejo_idioma = db(db.maneja_idioma.id == estudiante.idioma_destino).select().first()
		idioma = db(db.idioma.id == manejo_idioma.idioma).select().first()
		universidad1 = db(db.universidad.id == estudiante.universidad_1).select().first()
		pais1 = db(db.pais.id == universidad1.pais).select().first()
		convenio1 = db(db.convenio.id == universidad1.convenio).select().first()


		#Se empiezan a llenar los campos triviales (que no requieren queries)
		for campo in estudiante:
			f[campo] = estudiante[campo]


		#Se cargan manualmente los datos de la persona de contacto, idioma, y pais/universidad de destino
		f["apellidoContacto"] = contacto_emergencia.apellidos.decode("utf8").encode("latin1")
		f["direccionContacto"] = contacto_emergencia.direccion.decode("utf8").encode("latin1")
		f["emailContacto"] = contacto_emergencia.Correo.decode("utf8").encode("latin1")
		f["nombreContacto"] = contacto_emergencia.nombres.decode("utf8").encode("latin1")
		
		if contacto_emergencia.relacion == "Otro":
			f["relacionContacto"] = (contacto_emergencia.relacion + " - " + contacto_emergencia.relacion_otro).decode("utf8").encode("latin1")
		else:
			f["relacionContacto"] = contacto_emergencia.relacion.decode("utf8").encode("latin1")
		f["tlfoContacto"] = contacto_emergencia.telefono_habitacion + " - " + contacto_emergencia.telefono_celular

		f["idioma_destino"] = idioma.nombre.decode("utf8").encode("latin1")
		f["nivelOral"] = manejo_idioma.oral.decode("utf8").encode("latin1")
		f["nivelEscrito"] = manejo_idioma.escrito.decode("utf8").encode("latin1")
		f["nivelLectura"] = manejo_idioma.lectura.decode("utf8").encode("latin1")

		f["pais1"] = pais1.nombre.decode("utf8").encode("latin1")
		f["universidad_1"] = universidad1.nombre.decode("utf8").encode("latin1")
		f["convenio"] = convenio1.nombre.decode("utf8").encode("latin1")
		f['actividad_1'] = estudiante.actividad_1.decode("utf8").encode("latin1")
		f['periodo_1'] = estudiante.periodo_1.decode("utf8").encode("latin1")

		f["logo_univ"] = "./applications/SIGPIE/static/logo_usb.png"
		f["foto"] = "./applications/SIGPIE/uploads/{0}".format(recaudos.foto)

		#Escribo la informacion en el pdf
		stuff = open("/tmp/{0}(1).pdf".format(estudiante.carnet), 'w')
		stuff.write(f.render("./{0}(1).pdf".format(estudiante.carnet), 'S'))
		stuff.close()

		#Abro el archivo recien escrito
		stuff = open("/tmp/{0}(1).pdf".format(estudiante.carnet), 'r')
		
		#Lo almaceno en la base
		db(db.estudiante.carnet == session.usuario['usbid']).update(pagina_1 = stuff)
		stuff.close()
	
		############
		# PAGINA 2 #
		############

		g = Template(format="letter",
					 title="Pagina 2 Expediente")

		#Se carga la plantilla en formato csv, se especifica que los campos se separaran por ; y
		#que el . se usa para decimales
		g.parse_csv("./applications/SIGPIE/static/formulario_2.csv", ";", ".")

		#Se agrega una pagina al PDF
		g.add_page()

		##################################################################
		# REVISAR CUALES CAMPOS PUEDEN SER MULTILINEA Y MODIFICAR EL CSV #
		##################################################################

		# Estudiante en sesión
		estudiante = db(db.estudiante.carnet == session.usuario['usbid']).select().first()
		# Universidad segunda opçión
		universidad_2 = db(db.universidad.id == estudiante.universidad_2).select().first()
		if universidad_2 != None:
			# País segunda opción
			pais_2 = db(db.pais.id == universidad_2.pais).select().first()
			# Convenio segunda opción
			convenio_2 = db(db.convenio.id == universidad_2.convenio).select().first()
		# Información académica
		informacion_academica = db(db.informacion_academica.estudiante == estudiante.id).select().first()

		if informacion_academica.postgrado_nombre is None:
			g['carrera'] = informacion_academica.carrera.nombre.decode("utf8").encode("latin1")
		elif informacion_academica.postgrado_nombre == "":
			g['carrera'] = informacion_academica.carrera.nombre.decode("utf8").encode("latin1")
		elif informacion_academica.postgrado_nombre is not None:
			g['carrera'] = informacion_academica.postgrado_nombre.decode("utf8").encode("latin1")
		else:
			g['carrera'] = informacion_academica.carrera.nombre.decode("utf8").encode("latin1")
		
		g['creditos'] = informacion_academica.creditos_aprob
		g['indice'] = informacion_academica.indice
		if universidad_2 != None:
			g['opc_interc_2'] = pais_2.nombre.decode("utf8").encode("latin1")
			g['universidad_2'] = universidad_2.nombre.decode("utf8").encode("latin1")
			g['convenio'] = convenio_2.nombre.decode("utf8").encode("latin1")
			g['actividad_2'] = estudiante.actividad_2.decode("utf8").encode("latin1")
			g['periodo_2'] = estudiante.periodo_2.decode("utf8").encode("latin1")

		materia_1 = db((db.materia.formulario == 1) &
					(db.materia.fk_estudiante == estudiante.id)).select().first()

		if materia_1 != None:
			g["codigo_usb_1"] = materia_1.codigo_usb
			g['denominacion_usb_1'] = materia_1.materia_usb.decode("utf8").encode("latin1")
			g['creditos_usb_1'] = materia_1.creditos_usb
			g['codigo_ext_1'] = materia_1.codigo_ext
			g['denominacion_ext_1'] = materia_1.materia_ext.decode("utf8").encode("latin1")
			g['creditos_ext_1'] = materia_1.numero_horas

		materia_2 = db((db.materia.formulario == 2) &
					(db.materia.fk_estudiante == estudiante.id)).select().first()

		if materia_2 != None:
			g["codigo_usb_2"] = materia_2.codigo_usb
			g['denominacion_usb_2'] = materia_2.materia_usb.decode("utf8").encode("latin1")
			g['creditos_usb_2'] = materia_2.creditos_usb
			g['codigo_ext_2'] = materia_2.codigo_ext
			g['denominacion_ext_2'] = materia_2.materia_ext.decode("utf8").encode("latin1")
			g['creditos_ext_2'] = materia_2.numero_horas

		materia_3 = db((db.materia.formulario == 3) &
					(db.materia.fk_estudiante == estudiante.id)).select().first()

		if materia_3 != None:
			g["codigo_usb_3"] = materia_3.codigo_usb
			g['denominacion_usb_3'] = materia_3.materia_usb.decode("utf8").encode("latin1")
			g['creditos_usb_3'] = materia_3.creditos_usb
			g['codigo_ext_3'] = materia_3.codigo_ext
			g['denominacion_ext_3'] = materia_3.materia_ext.decode("utf8").encode("latin1")
			g['creditos_ext_3'] = materia_3.numero_horas

		materia_4 = db((db.materia.formulario == 4) &
					(db.materia.fk_estudiante == estudiante.id)).select().first()

		if materia_4 != None:
			g["codigo_usb_4"] = materia_4.codigo_usb
			g['denominacion_usb_4'] = materia_4.materia_usb.decode("utf8").encode("latin1")
			g['creditos_usb_4'] = materia_4.creditos_usb
			g['codigo_ext_4'] = materia_4.codigo_ext
			g['denominacion_ext_4'] = materia_4.materia_ext.decode("utf8").encode("latin1")
			g['creditos_ext_4'] = materia_4.numero_horas

		materia_5 = db((db.materia.formulario == 5) &
					(db.materia.fk_estudiante == estudiante.id)).select().first()

		if materia_5 != None:
			g["codigo_usb_5"] = materia_5.codigo_usb
			g['denominacion_usb_5'] = materia_5.materia_usb.decode("utf8").encode("latin1")
			g['creditos_usb_5'] = materia_5.creditos_usb
			g['codigo_ext_5'] = materia_5.codigo_ext
			g['denominacion_ext_5'] = materia_5.materia_ext.decode("utf8").encode("latin1")
			g['creditos_ext_5'] = materia_5.numero_horas

		materia_6 = db((db.materia.formulario == 6) &
					(db.materia.fk_estudiante == estudiante.id)).select().first()

		if materia_6 != None:
			g["codigo_usb_6"] = materia_6.codigo_usb
			g['denominacion_usb_6'] = materia_6.materia_usb.decode("utf8").encode("latin1")
			g['creditos_usb_6'] = materia_6.creditos_usb
			g['codigo_ext_6'] = materia_6.codigo_ext
			g['denominacion_ext_6'] = materia_6.materia_ext.decode("utf8").encode("latin1")
			g['creditos_ext_6'] = materia_6.numero_horas

		materia_7 = db((db.materia.formulario == 7) &
					(db.materia.fk_estudiante == estudiante.id)).select().first()

		if materia_7 != None:
			g["codigo_usb_7"] = materia_7.codigo_usb
			g['denominacion_usb_7'] = materia_7.materia_usb.decode("utf8").encode("latin1")
			g['creditos_usb_7'] = materia_7.creditos_usb
			g['codigo_ext_7'] = materia_7.codigo_ext
			g['denominacion_ext_7'] = materia_7.materia_ext.decode("utf8").encode("latin1")
			g['creditos_ext_7'] = materia_7.numero_horas

		materia_8 = db((db.materia.formulario == 8) &
					(db.materia.fk_estudiante == estudiante.id)).select().first()

		if materia_8 != None:
			g["codigo_usb_8"] = materia_8.codigo_usb
			g['denominacion_usb_8'] = materia_8.materia_usb.decode("utf8").encode("latin1")
			g['creditos_usb_8'] = materia_8.creditos_usb
			g['codigo_ext_8'] = materia_8.codigo_ext
			g['denominacion_ext_8'] = materia_8.materia_ext.decode("utf8").encode("latin1")
			g['creditos_ext_8'] = materia_8.numero_horas

		materia_9 = db((db.materia.formulario == 9) &
					(db.materia.fk_estudiante == estudiante.id)).select().first()

		if materia_9 != None:
			g["codigo_usb_9"] = materia_9.codigo_usb
			g['denominacion_usb_9'] = materia_9.materia_usb.decode("utf8").encode("latin1")
			g['creditos_usb_9'] = materia_9.creditos_usb
			g['codigo_ext_9'] = materia_9.codigo_ext
			g['denominacion_ext_9'] = materia_9.materia_ext.decode("utf8").encode("latin1")
			g['creditos_ext_9'] = materia_9.numero_horas

		materia_10 = db((db.materia.formulario == 10) &
					(db.materia.fk_estudiante == estudiante.id)).select().first()

		if materia_10 != None:
			g["codigo_usb_10"] = materia_10.codigo_usb
			g['denominacion_usb_10'] = materia_10.materia_usb.decode("utf8").encode("latin1")
			g['creditos_usb_10'] = materia_10.creditos_usb
			g['codigo_ext_10'] = materia_10.codigo_ext
			g['denominacion_ext_10'] = materia_10.materia_ext.decode("utf8").encode("latin1")
			g['creditos_ext_10'] = materia_10.numero_horas
		materia_11 = db((db.materia.formulario == 11) &
					(db.materia.fk_estudiante == estudiante.id)).select().first()

		if materia_11 != None:
			g["codigo_usb_11"] = materia_11.codigo_usb
			g['denominacion_usb_11'] = materia_11.materia_usb.decode("utf8").encode("latin1")
			g['creditos_usb_11'] = materia_11.creditos_usb
			g['codigo_ext_11'] = materia_11.codigo_ext
			g['denominacion_ext_11'] = materia_11.materia_ext.decode("utf8").encode("latin1")
			g['creditos_ext_11'] = materia_11.numero_horas

		materia_12 = db((db.materia.formulario == 12) &
					(db.materia.fk_estudiante == estudiante.id)).select().first()

		if materia_12 != None:
			g["codigo_usb_12"] = materia_12.codigo_usb
			g['denominacion_usb_12'] = materia_12.materia_usb.decode("utf8").encode("latin1")
			g['creditos_usb_12'] = materia_12.creditos_usb
			g['codigo_ext_12'] = materia_12.codigo_ext
			g['denominacion_ext_12'] = materia_12.materia_ext.decode("utf8").encode("latin1")
			g['creditos_ext_12'] = materia_12.numero_horas
		

		#Escribo la informacion en el pdf
		stuff = open("/tmp/{0}(2).pdf".format(estudiante.carnet), 'w')
		stuff.write(g.render("./{0}(2).pdf".format(estudiante.carnet), 'S'))
		stuff.close()

		#Abro el archivo recien escrito
		stuff = open("/tmp/{0}(2).pdf".format(estudiante.carnet), 'r')
		
		#Lo almaceno en la base
		db(db.estudiante.carnet == session.usuario['usbid']).update(pagina_2 = stuff)
		stuff.close()

		#working_dir = os.system("pwd")
		#print(working_dir)
		uploadpath = "./applications/SIGPIE/uploads/"
		#os.chdir("/tmp")

		statement = "pdftk "

		statement += "/tmp/{0}\(1\).pdf ".format(estudiante.carnet) + " "
		statement += "/tmp/{0}\(2\).pdf ".format(estudiante.carnet) + " "
		statement += os.path.join(uploadpath, recaudos.cedula) + " "
		statement += os.path.join(uploadpath, recaudos.carnet) + " "
		statement += os.path.join(uploadpath, recaudos.informe_academico) + " "
		statement += os.path.join(uploadpath, recaudos.comprobante) + " "
		statement += os.path.join(uploadpath, recaudos.carta_motivacion) + " "
		statement += os.path.join(uploadpath, recaudos.flujograma) + " "
		if recaudos.certificado_lengua != "":
			statement += os.path.join(uploadpath, recaudos.certificado_lengua) + " "
		statement += os.path.join(uploadpath, recaudos.curriculum_vitae) + " "
		statement += os.path.join(uploadpath, recaudos.programas_de_estudio) + " "
		if recaudos.actividades_extracurriculares != "":
			statement += os.path.join(uploadpath, recaudos.actividades_extracurriculares) + " "

		statement += "output /tmp/exp{0}.pdf".format(estudiante.carnet)

		os.system(statement)

		response.stream("/tmp/exp{0}.pdf".format(estudiante.carnet))
		

	else:
		redirect(URL('index'))


