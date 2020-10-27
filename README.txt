
############
User Market
############

Dependencias:

Python3
pip/pip3 (Para instalar paquetes de python)
Django 1.11
Haystack (pip install django-haystack)  #Engine de busqueda
Whoosh (pip install Whoosh)   #Engine de busqueda
Pillow (pip install Pillow)   #Procesador de Imagenes
django-recaptcha2 (pip install django-recaptcha2)   #Google Captcha

Datos Importantes para el deploy:

"/media/no-img.jpg" es la imagen default en caso de que el articulo no tenga imagen

Static files:
Elementos estaticos como los .css y .js tienen que ser configurados de una manera distinta para el deploy
https://docs.djangoproject.com/en/1.11/howto/static-files/deployment/

Captcha:
Ir a https://www.google.com/recaptcha y registrar el dominio de la pagina, despues insertar las keys recibidas en RECAPTCHA_PRIVATE_KEY y RECAPTCHA_PUBLIC_KEY respectivamente en settings.py

Base de Datos:

Por default Django usa sqlite como base de datos, esto es aceptable pero no recomendable para un server produccion, es una buena idea preparar otra base de datos como Mysql o PostgreSQL.
Mas informacion: https://docs.djangoproject.com/en/1.11/ref/databases/

Comandos importantes antes del deploy:

python manage.py makemigrations (Prepara las migraciones hacia la base de datos)
python manage.py migrate (Ejecuta las migraciones)
python manage.py rebuild_index (Migraciones del search engine)

Instrucciones para deploy:

Tener en cuenta todos estos puntos:
https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

La manera mas simple y recomendable es usar Gunicorn (http://gunicorn.org/)
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/gunicorn/

Luego preparar un server Nginx como reverse proxy para poder acceder al server de gunicorn desde internet.
https://www.nginx.com/resources/admin-guide/reverse-proxy/

