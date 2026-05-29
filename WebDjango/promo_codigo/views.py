from django.shortcuts import render
from .models import PromoCodigo
from django.http import JsonResponse
from Orden.decorador import validar_cart_and_orden


@validar_cart_and_orden
def validar(request, cart, orden):
        codigo = request.GET.get('code')#obtiene el parametro code de la url ?code=promo123 ejmplo: promo123 
        promo_codigo = PromoCodigo.objects.get_validar(codigo)#buscamos el codigo en db

        if promo_codigo is None:#si no existe, responde json con status false y 404
                return JsonResponse({
                        'status': False
                },      status = 404)
        
        orden.aplicarCodigo(promo_codigo)#metodo definido aplicarCodigo aca se usa

        return JsonResponse({#si existe responde con: json
                'status':True,
                'codigo':promo_codigo.codigo,#codigo encontrado
                'descuento':promo_codigo.descuento, #descuento asociado al modelo o objeto
                'total':orden.total# total llevara el total de la orden
        })
