from django.shortcuts import render, redirect #shorcuts(atajos, para formar plantillas html o manejar errores) 
from .models import Cart
from products.models import Product
from .funciones import funcionCarrito
from django.shortcuts import get_object_or_404
from .models import CartProduct

def cart(request): 
    cart = funcionCarrito(request) #traemos lla funcion
    return render(request, 'carts/cart.html', {
        'cart':cart
    })

#print(dir(request.session)) entonces podemos controlar la session del usuario sin cookies, con la session de django
    # 'session_key', ' set_expiry'
    #request.session.set_expiry(300) tiempo de fin de session
    #key = request.session.session_key
    #print(key)


def add(request):
    cart = funcionCarrito(request)
    product = get_object_or_404 (Product, pk=request.POST.get('product_id'))#se hace la solicitud a la tabla product y se busca el product que coincida con  el valor que lleva el product_id desde el input
    quantity = int(request.POST.get('quantity', 1))#var para obtener el valor de la request quantity del input en el add.html

   ## cart.products.add(product, through_defaults={#argumento que permite pasar valores a los campos adicionales a tabla intermedia necesario caunto tabla intermedia tiene mas valores aparte de los ids
     #   "quantity": quantity #el primero es el del modelo, el que creamos que viene con el request, y practicamente se le agrega a la columna quantity lo que viene en el valor que es el request.
   # })

    product_cart = CartProduct.objects.crear_actualizar(cart=cart, product=product, quantity=quantity)

    return render(request, 'carts/add.html', {
        'product' : product
    })

def remove(request):
    cart = funcionCarrito(request)
    #pk busca el objeto producto que en este caso coincida con el id que viene en el post product_id
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))#entonces get_object intenta obtener el objeto el cual se generea en el formulario con el post

    cart.products.remove(product)

    return redirect('cart')



