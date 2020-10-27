from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    
    return 'imagenes-articulos/user{0}/{1}/'.format(instance.owner.id, filename)

class Detallesusuario(models.Model):
    user   = models.OneToOneField(User, on_delete = models.CASCADE)
    reputacion = models.IntegerField(default    = 0)
    balance = models.DecimalField(default = 0, max_digits= 19, decimal_places=10)

    def __str__(self):
        return str(self.user.username)

class Categoria(models.Model):
	nombre = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique=True)
	class Meta:
		ordering = ('nombre',)
		verbose_name = 'categoria'
		verbose_name_plural = 'categorias'

	def __str__(self):
		return self.nombre
class Articulo(models.Model):
	owner = models.ForeignKey(User, on_delete = models.CASCADE)
	categoria = models.ForeignKey(Categoria)
	nombre = models.CharField(max_length = 100, default="Sin Nombre")
	descripcion = models.CharField(max_length = 2000, default="Sin Descripcion")
	precio = models.CharField(max_length = 10,default="0")
	imagen = models.ImageField(upload_to = user_directory_path, default = 'no-img.jpg')
	imagen2 = models.ImageField(upload_to = user_directory_path, default = 'no-img.jpg')
	imagen3 = models.ImageField(upload_to = user_directory_path, default = 'no-img.jpg')
	imagen4 = models.ImageField(upload_to = user_directory_path, default = 'no-img.jpg')
	imagen5 = models.ImageField(upload_to = user_directory_path, default = 'no-img.jpg')
	finalizado = models.BooleanField(default=False)
	pais = models.CharField(max_length = 100, default="Sin Especificar")
	ciudad = models.CharField(max_length = 100, default="Sin Especificar")
	region = models.CharField(max_length = 100, default="Sin Especificar")
	envionacional = models.BooleanField(default=False)
	enviointer = models.BooleanField(default=False)
	detallesenvio = models.CharField(max_length = 300, default="Sin Especificar")

	def __str__(self):
		return "%s publicado por %s"%(self.nombre,self.owner)
class Compra(models.Model):
	comprador = models.ForeignKey(User, null=True, related_name='comprador')
	vendedor = models.ForeignKey(User, null=True, related_name='vendedor')
	articulo = models.ForeignKey(Articulo)
	compconfirm = models.BooleanField(default=False)
	vendconfirm = models.BooleanField(default=False)

	def __str__(self):
		return "Compra de %s, %s publicado por %s"%(self.comprador,self.articulo.nombre,self.vendedor)

class Pregunta(models.Model):
	owner = models.ForeignKey(User, null=True, related_name='owner_pregunta')
	articulo = models.ForeignKey(Articulo)
	texto = models.CharField(max_length = 500, default="Sin Pregunta")
	respondida = models.BooleanField(default=False)

	def __str__(self):
		return "Pregunta de %s en %s"%(self.owner,self.articulo.nombre)

class Notificacion(models.Model):
	owner = models.ForeignKey(User, null=True, related_name='notificaciones')
	texto = models.CharField(max_length = 500, default="Error")
	vista = models.BooleanField(default=False)

class Respuesta(models.Model):
	pregunta = models.ForeignKey(Pregunta, null=True)
	articulo = models.ForeignKey(Articulo)
	owner = models.ForeignKey(User, null=True, related_name='owner_respuesta')
	texto = models.CharField(max_length = 500, default="Sin Respuesta")

	def __str__(self):
		return "Respuesta de %s en el articulo %s"%(self.owner,self.articulo.nombre)

class Denuncia(models.Model):
	denunciado = models.ForeignKey(User, null=True, related_name='denunciado')
	owner = models.ForeignKey(User, null=True, related_name='owner')
	texto = models.CharField(max_length = 500, default="Sin Especificar")

	def __str__(self):
		return "Denuncia de %s a %s"%(self.owner,self.denunciado)




	