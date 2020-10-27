from django.contrib import admin
from .models import Denuncia, Articulo, Compra, Pregunta, Respuesta, Categoria, Notificacion,Detallesusuario

# Register your models here.
admin.site.register(Articulo)
admin.site.register(Compra)
admin.site.register(Pregunta)
admin.site.register(Respuesta)
admin.site.register(Categoria)
admin.site.register(Notificacion)
admin.site.register(Denuncia)
admin.site.register(Detallesusuario)