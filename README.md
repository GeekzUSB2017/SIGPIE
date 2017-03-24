## SIGPIE

## REQUERIMIENTOS BÁSICOS

Sistema Operativo: Linux   
Python: Python 2.7.9  
Pip: 9.0.1  
Base de Datos: SQLite  


## DEPENDENCIAS

Para ejecutar SIGPIE debe poseer las siguiente librerias  

libsasl2-dev  
python-dev  
libldap2-dev  
libssl-dev  
ldap-utils  
gcc  
pdftk  


Para instalarlas, ejecutar el siguiente comando desde un terminal:  

sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev ldap-utils gcc pdtfk 

Adicionalmente, se deben instalar los siguientes módulos a través de Python Pip:  

setuptools  
python-ldap  

Para instalarlos, ejecutar el siguiente comando desde un terminal:  

sudo pip install setuptools  
sudo pip install python-ldap  

Para la generación de las páginas del PDF se utilizó la libreria PYFPDF incluida en web2py, sin embargo se actualizó a la última versión disponible a la fecha (1.7.2) disponible en su repositorio oficial (ver referencias al final). Para esto, se substituyó la carpeta fpdf dentro de la gluon/contrib, y se colocó la carpeta con la nueva versión. Además para la edición de las páginas del formulario de postulación se utilizó el designer que trae fpdf el cual se encuentra dentro de la carpeta /tools dentro del contenido descargado de fpdf. Para hacer servir este designer se necesita tener instalado wxPython. Se recomienda que se use la versin 2.8, sin embargo, debido a que la instalación de esta versión es bastante compleja, el equipo de desarrollo probó la versión 3 de wxPython y se encontró que funciona correctamente. wxPython3 se encuentra en los repositorios oficiales del sistema operativo (se probó en Debian, Ubuntu y Mint).   

Cabe destacar que para hacer funcionar fpdf no solamente se necesita copiar el contenido de la libreria en /gluon/contrib/fpdf, sino que también se debe instalar. Para esto, se descarga la última versión de fpdf, se descomprime y se navega hasta dentro de la carpeta desde el terminal y se ejecuta el comando: sudo python setup install  

## DESCARGA
A continuación se presentan los distintos modos de poder ejecutar  el SIGPIE:  

Descargar archivo .zip desde la página de Github que contiene el sistema completo  

Ejecutar el comando: wget https://github.com/GeekzUSB2017/SIGPIE/archive/master.zip  

Clonar el repositorio de SIGPIE a través de git: git clone https://github.com/GeekzUSB2017/SIGPIE.git  

## EJECUCIÓN  
Navegar hasta la carpeta recien descargada y descomprimida y ejecutar de la siguiente manera:

python web2py.py  

Cargar desde el appadmin de web2py (localhost:8000/admin) en la base de datos los archivos CSV que contienen la información necesiaria para poder llenar correctamente los formularios. Para esto, dentro del admin de web2py, se seleccionar el Botón Manage de la aplicación SIGPIE, Edit, presionar el botón database administration, y cargar los archivos CSV uno por uno desde la opción Import. Si ocurre que se genera un error por FOREIGN KEY, seguir cargando los archivos CSV en las tablas restantes y al terminar, volver a intentar cargar de nuevo los archivos que dieron error. Esto ocurre porque al momento de cargar los datos en una cierta tabla, no existe la referencia (foreign key) a otra tabla que aun no se ha llenado. 
## REFERENCIAS  
Repositorio para descargar pyfpdf: https://github.com/reingart/pyfpdf  
Documentación de pyfpdf: https://pyfpdf.readthedocs.io/en/latest/  
