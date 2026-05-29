from .models import Cart
#funcion para manejar el carrito de acuerdo a la sesion
#la variable user a continuacion garantiza que exista el carrito para usuarios autenticados y visitantes
def funcionCarrito(request):
    user = request.user if request.user.is_authenticated else None # si ese usuario en la peticion se encuentra autenticado nos devuelva el usuario autenticado sino none, 
    cart_id = request.session.get('cart_id')#recuperamos la session del usuario con el identificador del carrito que ya esta en curso
    cart = Cart.objects.filter(cart_id=cart_id).first()#si hay cart_id en la sesion lo busca en la db
    #sino encuentra devuelve none
    if cart is None:
        cart = Cart.objects.create(user=user)#sino esta cart_id lo creamos, si user esta se le asigna, sino se crea sin usuario
    
    if user and cart.user is None: #si hay user registrado pero no carrito registrado entonces se lo crea y se le asigna
        cart.user = user #asi cuando se logea user se vincula a su cuenta
        cart.save()

    request.session['cart_id'] = cart.cart_id #guardamos el cart_id en la sesion, then aunque el usur no este logeado el carrito durara mientras dure la session

    return cart

#funcion para eliminar el carrito
def deleteCart(request):#elimina el id del carrito de la session del usuario, user ya no tendra carrito asociado
    request.session['cart_id'] = None
    