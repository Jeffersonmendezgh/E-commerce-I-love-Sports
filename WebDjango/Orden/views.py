from django.shortcuts import render, redirect, get_object_or_404
from .models import Orden
from DirEnvio.models import DireccionEnvio
from carts.funciones import funcionCarrito, deleteCart
from Orden.utils import funcion_orden, deleteOrden
from django.contrib.auth.decorators import login_required
from .utils import breadcrumb
from django.contrib import messages
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import EmptyQuerySet
from .decorador import validar_cart_and_orden

class OrdenViews(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'orden/ordenes.html'

    def get_queryset(self):
        return self.request.user.ordenes_completadas()
    """recordemos que cuando heredamos de listwiew  
    nos da - Un queryset por defecto (Model.objects.all()).
- Un contexto con la lista de objetos (object_list).
- Renderizado automático en el template que definas
    """

#controlar que usuario no registrado no pueda ingresar a orden
#en este caso redirije a login
@login_required(login_url='login')#entonces lo que hacemos es restringir esta vista en caso que no este autenticado
def orden(request):
    cart = funcionCarrito(request)#obtenemos carrito actual
    orden = funcion_orden(cart, request)#usamos la funcion y asi tenemos la orden asociada al carrito y al usuario, sino existia se crea

    return render(request, 'orden/orden.html',{
        'cart':cart,
        'orden':orden,
        'breadcrumb':breadcrumb(addres=True),  #obtenemos la funcion para controlar 

    })

@login_required(login_url='login')
@validar_cart_and_orden #ahora este decorador hace lo mismo que funcioncarrito y orden en la view anterior
def direccion(request, cart, orden):#solo tenemos que agregarle el cart y la orden como parametro

    direccion_envio = orden.get_or_set_direccion_envio()
    contDireccion = request.user.direccionenvio_set.count() >1 #en caso de que solo exista una sola direccion no mostrar boton
    return render(request, 'orden/direccion.html',{
        'cart':cart,
        'orden':orden,
        "direccion_envio" : direccion_envio,
        'contDireccion': contDireccion,
        "breadcrumb":breadcrumb(addres=True),
    })

#vista para mostrar todas las ordenes
@login_required(login_url='login')
def select_direccion(request):
    direccion_envios = request.user.direccionenvio_set.all()
    return render(request, 'orden/select_direccion.html',{
        'breadcrumb': breadcrumb(addres=True),
        'direccion_envios': direccion_envios,
    })

#vista para seleccionar direccio "botn direccion"
@login_required(login_url='login')
@validar_cart_and_orden
def check_direccion(request, cart, orden, pk):

    direccion_envio = get_object_or_404(DireccionEnvio, pk=pk)

    if request.user.id != direccion_envio.user_id:
        return redirect('index')
    
    orden.update_direccion_envio(direccion_envio)
    return redirect('direccion')

#Vista para visualizar la informacionde la orden
@login_required(login_url='login')
@validar_cart_and_orden
def confirmacion(request, cart, orden):

    direccion_envio = orden.direccion_envio
    if direccion_envio is None:
        return redirect('direccion')
    
    return render(request, 'orden/confirmacion.html',{
        'cart' : cart,
        'orden': orden,
        'direccion_envio':direccion_envio,
        'breadcrumb':breadcrumb(addres=True, confirmation=True),
    })

#boton eliminar orden
@login_required(login_url='login')
def cancelar_orden(request):
    cart = funcionCarrito(request)#recupera el carrito actual del user en session
    orden = funcion_orden(cart, request)#construye o recupera orden asociada al carrito
#IMPORTANTE, user_id o cart_id etc hace referencia al campo de clave foranea de cada tabla
#el id de cada tabla por defecto es id, el id foraneo es ejemplo en orden user_id.
    if request.user.id != orden.user_id:#aseguramos que el usuario que va a cancelar la orden sea el dueño de la orden
        return redirect('index')
    
    orden.cancelar()#marca la orden como cancelada en la db, no la borra solo cambia estadp
    deleteCart(request)#limpia la sesion del user eliminando el cart_id
    deleteOrden(request)#de esta manera ya no habra ni cart ni orden para el user activo
    
    messages.error(request, 'Orden eliminada correctamente')
    return redirect('index')

@login_required(login_url='login')
@validar_cart_and_orden
def completado(request, cart, orden):

    if request.user.id != orden.user_id:
        return redirect('index')
    
    orden.completado()
    #ahora destruimos el carrito y la orden
    deleteCart(request)
    deleteOrden(request)

    messages.success(request, 'compra completa pronto llegara a destino')
    return redirect('index')