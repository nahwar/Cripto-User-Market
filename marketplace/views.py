from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Articulo, Pregunta, Respuesta, Categoria, Compra, Detallesusuario, Denuncia
from .forms import ReCaptchaForm


def index(request):
    articulos = Articulo.objects.filter(finalizado = False)
    if not hasattr(request.user, 'detallesusuario') and not request.user.is_anonymous():
        i = Detallesusuario(user=request.user)
        i.save()
    return render(request, 'index.html', {"articulos":reversed(articulos)})

def signin(request):
    if request.method == "GET":
        return HttpResponseRedirect(reverse('index'))
    elif request.method == "POST":

        captchaform = ReCaptchaForm(request.POST)
        if not captchaform.is_valid():
            error_message = "Captcha Incorrecto"
            return render(request, 'login.html', {'captcha': ReCaptchaForm,"mensajeerror":error_message})
        if not request.POST['password'] == request.POST['password2']:
            error_message = "Las contraseñas no coinciden"
            return render(request, 'login.html', {'captcha': ReCaptchaForm,"mensajeerror":error_message})

        user = User.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password'])
        auth_login(request, user)
        return HttpResponseRedirect(reverse('index'))

def login(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))
        else:

            return render(request, 'login.html', {'captcha': ReCaptchaForm})
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('index'))
                #return HttpResponseRedirect(request.POST.get('next'))
            else:
                error_message = "Esta cuenta a sido baneada"
                return render(request, 'login.html', {'mensajeerror':error_message, 'username':username})

        else:
            error_message = "Usuario o contraseña incorrectos"
            return render(request, 'login.html', {'mensajeerror':error_message, 'username':username})

@login_required
def logoutpath(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

@login_required
def userindex(request, user_id):
    if request.method == "POST" and request.user.id != user_id:
        captchaform = ReCaptchaForm(request.POST)
        if not captchaform.is_valid():
            error_message = "Captcha Incorrecto"
            return render(request, 'userajeno.html', {'user':user,'captcha': ReCaptchaForm, 'mensajeerror': error_message})
        user = get_object_or_404(User, id=user_id)
        denuncia = Denuncia.objects.create(texto=request.POST['texto'],owner=request.user,denunciado=user)
        return HttpResponseRedirect(reverse('index'))

    user = get_object_or_404(User, id=user_id)
    articulos = user.articulo_set.filter(finalizado = False)

    if(user != request.user):
        detalles = Detallesusuario.objects.get(user=user)
        return render(request, 'userajeno.html', {'detalles':detalles,'user':user, 'captcha': ReCaptchaForm, 'articulos': reversed(articulos)})

    compras = user.comprador.all()
    ventas = user.vendedor.all()
    detalles = Detallesusuario.objects.get(user=user)
    notificaciones = user.notificaciones.filter(vista = False)
    #if(notificaciones):
    #    for i in notificaciones:
    #        i.vista = True
    #        i.save()
    return render(request, 'user.html', {'detalles':detalles,'ventas':reversed(ventas), 'compras':reversed(compras), 'user' : user, 'articulos': reversed(articulos), 'notificaciones': reversed(notificaciones)})

@login_required
def newart(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        return render(request, 'newart.html', {'captcha': ReCaptchaForm, 'categorias': categorias})
    elif request.method == "POST":
        captchaform = ReCaptchaForm(request.POST)
        if not captchaform.is_valid():
            error_message = "Captcha Incorrecto"
            return render(request, 'newart.html', {'mensajeerror': error_message})


        if 'image' in request.FILES:
            file = request.FILES['image']
        else:
            file = 'no-img.jpg'

        if 'image2' in request.FILES:
            file2 = request.FILES['image2']
        else:
            file2 = None

        if 'image3' in request.FILES:
            file3 = request.FILES['image3']
        else:
            file3 = None

        if 'image4' in request.FILES:
            file4 = request.FILES['image4']
        else:
            file4 = None

        if 'image5' in request.FILES:
            file5 = request.FILES['image5']
        else:
            file5 = None

        envnac = False
        envint = False
        if 'nac' in request.POST:
            envnac = True
        if 'int' in request.POST:
            envint = True
        cate = get_object_or_404(Categoria, nombre=request.POST['cat'])
        articulo = Articulo.objects.create(nombre=request.POST['nombre'],precio=request.POST['precio'],descripcion=request.POST['descripcion'],owner=request.user,imagen=file,imagen2=file2,imagen3=file3,imagen4=file4,imagen5=file5,pais=request.POST['pais'],ciudad=request.POST['ciudad'],region=request.POST['region'],envionacional=envnac,enviointer=envint,detallesenvio=request.POST['detallesenvio'],categoria=cate)
        return HttpResponseRedirect(reverse('index'))

def articulo(request,articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    if articulo.finalizado == True:
        return HttpResponseRedirect(reverse('index'))
    preguntas = articulo.pregunta_set.all()
    respuestas = articulo.respuesta_set.all()
    return render(request, 'articulo.html', {'articulo' : articulo, 'preguntas' : preguntas, 'respuestas' : respuestas, 'captcha': ReCaptchaForm})

@login_required
def pregunta(request,articulo_id):
    if request.method == "POST":
        captchaform = ReCaptchaForm(request.POST)
        if not captchaform.is_valid():
            error_message = "Captcha Incorrecto"
            return HttpResponseRedirect(reverse('articulo', kwargs={'articulo_id':articulo_id}))

        
        articulo = get_object_or_404(Articulo, id=articulo_id)
        pregunta = articulo.pregunta_set.create(texto=request.POST['texto'],owner=request.user)
        notificacion = articulo.owner.notificaciones.create(texto="Nueva pregunta por articulo '%s'"%(articulo.nombre))
        return HttpResponseRedirect(reverse('articulo', kwargs={'articulo_id':articulo_id}))
    else:
        return HttpResponseRedirect(reverse('index'))

@login_required
def resppregunta(request,pregunta_id):
    if request.method == "POST":
        pregunta = get_object_or_404(Pregunta, id=pregunta_id)
        if request.user == pregunta.articulo.owner:
            respuesta = pregunta.respuesta_set.create(texto=request.POST['texto'],owner=request.user,articulo=pregunta.articulo)
            pregunta.respondida = True
            pregunta.save()
            notificacion = pregunta.owner.notificaciones.create(texto="Respondieron a tu pregunta sobre '%s'"%(pregunta.articulo.nombre))
            return HttpResponseRedirect(reverse('articulo', kwargs={'articulo_id':pregunta.articulo.id}))
        return HttpResponseRedirect(reverse('articulo', kwargs={'articulo_id':pregunta.articulo.id}))
    return HttpResponseRedirect(reverse('index'))

@login_required
def editarart(request,articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    if request.method == "GET":
        if request.user == articulo.owner:
            return render(request, 'editart.html', {'articulo' : articulo, 'captcha': ReCaptchaForm})
        else:
            return HttpResponseRedirect(reverse('index'))
    elif request.method == "POST":
        captchaform = ReCaptchaForm(request.POST)
        if not captchaform.is_valid():
            error_message = "Captcha Incorrecto"
            return HttpResponseRedirect(reverse('editarart', kwargs={'articulo_id':articulo_id}))

        if request.user == articulo.owner:
            if 'image' in request.FILES:
                file = request.FILES['image']
            else:
                file = 'no-img.jpg'

            if 'image2' in request.FILES:
                file2 = request.FILES['image2']
            else:
                file2 = None

            if 'image3' in request.FILES:
                file3 = request.FILES['image3']
            else:
                file3 = None

            if 'image4' in request.FILES:
                file4 = request.FILES['image4']
            else:
                file4 = None

            if 'image5' in request.FILES:
                file5 = request.FILES['image5']
            else:
                file5 = None

            envnac = False
            envint = False
            if 'nac' in request.POST:
                envnac = True
            if 'int' in request.POST:
                envint = True

            
            articulo.nombre = request.POST['nombre']
            articulo.precio = request.POST['precio']
            articulo.descripcion = request.POST['descripcion']
            articulo.pais = request.POST['pais']
            articulo.ciudad = request.POST['ciudad']
            articulo.region = request.POST['region']
            articulo.envionacional = envnac
            articulo.enviointer = envint
            articulo.detallesenvio = request.POST['detallesenvio']

            articulo.save()

            return HttpResponseRedirect(reverse('articulo', kwargs={'articulo_id':articulo.id}))
        else:
            return HttpResponseRedirect(reverse('index'))



@login_required
def borrarart(request,articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    if request.user == articulo.owner:
        articulo.finalizado = True
        articulo.save()
        return HttpResponseRedirect(reverse('index'))


    return HttpResponseRedirect(reverse('index'))

@login_required
def comprar(request,articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    if request.user != articulo.owner:

        # VERIFICAR QUE EL USUARIO TENGA SUFICIENTE BALANCE EN LA CUENTA

        compra = Compra.objects.create(comprador=request.user,vendedor=articulo.owner,articulo=articulo)
        mensaje = 'Compra realizada, Puede encontrar informacion sobre el vendedor en "Mi Perfil"'
        
        return render(request, 'index.html', {"mensajesuc":mensaje})


    return HttpResponseRedirect(reverse('index'))
    
@login_required
def compra(request,compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    if request.POST['conf'] == "c":
        if request.user == compra.comprador:

            if request.POST['rad'] == "si":
                detalles = Detallesusuario.objects.get(user=compra.vendedor)
                detalles.reputacion += 1
                detalles.save()
            else:
                detalles = Detallesusuario.objects.get(user=compra.vendedor)
                detalles.reputacion -= 1
                detalles.save()

            compra.compconfirm = True
            compra.save()
    if request.POST['conf'] == "v":
        if request.user == compra.vendedor:
            compra.vendconfirm = True
            compra.save()

    if compra.compconfirm and compra.vendconfirm:   
        ####
        #### ENVIAR COINS A LA CUENTA DEL VENDEDOR
        ####
        return HttpResponseRedirect(reverse('index'))

    return HttpResponseRedirect(reverse('index'))