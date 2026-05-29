from .utils import funcion_orden
from carts.funciones import funcionCarrito

def validar_cart_and_orden(function):
    def wrap(request, *args, **kwargs):

        cart = funcionCarrito(request)
        orden = funcion_orden(cart, request)

        return function(request, cart, orden, *args, **kwargs)
    
    return wrap

"""
Un decorador es una fun que recibe otra fun y devuelve una nueva fun envuelta en logica adiccional
- En este caso, validar_cart_and_orden recibe una view (función de Django) y le añade automáticamente la lógica para obtener el carrito y la orden
asi evitamos repetir codigo
flujo
- Usuario hace una petición → Django llama a la view.
- El decorador intercepta la llamada.
- El decorador obtiene cart y orden.
- El decorador llama a la view original, pasándole request, cart, orden.
- La view usa esos objetos directamente.
"""