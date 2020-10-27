from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/(?P<user_id>[1-9](?:\d+)?)/$', views.userindex, name='userindex'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logoutpath, name='logoutpath'),
    url(r'^signin', views.signin, name='signin'),
    url(r'^nuevo', views.newart, name='newart'),
    url(r'^search/', include('haystack.urls')),
    url(r'^articulo/(?P<articulo_id>[1-9](?:\d+)?)/$', views.articulo, name='articulo'),
    url(r'^compra/(?P<compra_id>[1-9](?:\d+)?)/$', views.compra, name='compra'),
    url(r'^articulo/(?P<articulo_id>[1-9](?:\d+)?)/comprar/$', views.comprar, name='comprar'),
    url(r'^articulo/(?P<articulo_id>[1-9](?:\d+)?)/editar/$', views.editarart, name='editarart'),
    url(r'^articulo/(?P<articulo_id>[1-9](?:\d+)?)/borrar/$', views.borrarart, name='borrarart'),
    url(r'^articulo/(?P<articulo_id>[1-9](?:\d+)?)/postpregunta/$', views.pregunta, name='pregunta'),
    url(r'^pregunta/(?P<pregunta_id>[1-9](?:\d+)?)/resp/$', views.resppregunta, name='resppregunta'),

]
