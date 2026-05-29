from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login as lg #damos alias para no repetir la funcion login
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from .forms import Registro # de mi clase importo la clase que cree
#from django.contrib.auth.models import User # clase q crea usuarios y encripta password
from users.models import User
from products.models import Product
from django.http import HttpResponseRedirect

#request es un objeto que represena la solicitud http que se hace al navegador
# cada vez que el user hace una peticion ya sea get, post, django recibe esa solicitud y la convierte en un objeto HttpRequest
#El objeto request guarda toda la información de esa petición.
#Algunas partes importantes que puedes usar son:- request.method → te dice si la petición fue GET, POST, PUT, etc.


def index(request):
    productos = Product.objects.all()
    return render(request, 'index.html', {
        'mensaje':'STORE',
        'titulo':'Inicio',
        'productos': productos,
    })

def login(request):
    if request.method == 'POST':#obtebenemos los valores  del post
        username = request.POST.get('username')
        password = request.POST.get('password')
        #guardamos en una variable usuarios los valores que vienen en el post
        usuarios = authenticate(username=username, password=password) #clave autentivate para revisar los user en db
        if usuarios:
           lg(request,usuarios)#llamamos libreria login
           messages.success(request, f'Bienvenido{usuarios.username}')
           #entonces next lo agrega djanago en la url
           if request.GET.get('next'):# busca si hay un parametro next en la url?
               return HttpResponseRedirect(request.GET['next'])#si existe, redirije al usuario a la pagina que estaba intentando visitar
           
           return redirect('index')#enviamos a la funcion index
        


        else:
            messages.error(request, 'Datos incorrectos')# en caso de datos incorrectos
    return render(request, 'users/login.html',{})  


def salir(request):
    logout(request)
    messages.success(request, 'Session cerrada correctamente') #pasamos al request este mensaje
    return redirect(login)

def registro(request):
    if request.user.is_authenticated:#si el user is autenticado al coloacar la ruta registro lo lleva al index
        return redirect ('index')
    form = Registro(request.POST or None)#POST ro None pq permite usar esta linea para get y post, osea get es none no tiene nada pero igual se muestra, si post entoncs tiene el form
    if request.method=='POST' and form.is_valid(): #si es post y el form es valido

            #ahora esto esta en el metodo form de la clase form
        usuario = form.save() #var que guarda el usuario creado
        if usuario: #
            lg(request, usuario)#si es correcto le enviamos la info del login
            messages.success(request, f'Bienvenido {usuario.username}')#mensaje de bienve
            return redirect('index')
    return render(request, 'users/registro.html', {
        'form':form #guardara la clase form
    })