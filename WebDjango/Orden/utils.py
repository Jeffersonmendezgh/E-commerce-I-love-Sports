from .models import Orden
from carts.funciones import funcionCarrito
from django.urls import reverse #cuando hagamos click nos refirija
def funcion_orden(cart, request):#cart es una instancia del modelo cart, objeto carrito especifico del usuario en la sesion actual
    #request es el HTTP object que django entrega en todas las vistas
    #contiene: metodo,hedaers,POST,GET, usuario actual request.user y sesion actual request.session
    #necesario para verificar si usuario es autenticado y para guardar orden id
    
    orden = cart.orden #busca si ya existe una orden asiciada a ese carrito
    #filter(cart=cart) devuelve queryset con todas las ordenes que tenga ese carrito
    #first() devuelve la primera, o NOne si no encuentra, como resultado orden es la orden que exite o None

    if orden is None and request.user.is_authenticated:#si no existe orden y el user is authenticad entonces se crea nueva orden
        #asegurando que solo user logeados puedan generar ordenes
        orden = Orden.objects.create(cart=cart, user=request.user)#crea orden en db, vincualda al carrito y user actual

    if orden: #si existe una orden se guarda su id en la sesion del usuario
        request.session['orden_id']= orden.id #permite que en futuras peticiones se recuopere orden actiuva desde la session sin tener que buscarla de nuevo
    return orden # devuelve la orden creada o encontrada para poder usarla en la vista

#flujo: la vista obtiene el carrito con funcioncarrito(request)
#llama a funcu¿ion:orden(cart, request)pasando carrito actual y peticion HTTP
#la fun busca si ya existe una orden para ese carrito, sino crea una y guarda el orden_id en la sesion del request y devuelve la orden

def breadcrumb(products=True, addres=False, payment=False, confirmation=False):
    return(
        {'title':'Productos', 'active':products,'url': reverse('orden')},
        {'title':'Direccion', 'active':addres,'url': reverse('direccion')},
        {'title':'Pago', 'active':payment,'url': reverse('orden')},
        {'title':'Confirmacion', 'active':confirmation,'url': reverse('orden')},
    )
#funcion para eliminar orden
def deleteOrden(request):#elimina la orden asociada al usuario en session
    request.session['cart_id'] = None