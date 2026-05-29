from django.urls import path
from .import views

urlpatterns = [#entonces dejar el path en '' para no incluir segunda ruta, name parece que es para acceder a la ruta desde el html
    path('', views.orden, name='orden'),#no olvidar que este nombre va primero y seguidamente va el de la urls.py principal en este caso '' para no incluir orden/orden en la url sino orden/
    path('direccion', views.direccion, name='direccion'),
    path('seleccionar/direccion', views.select_direccion, name='select_direccion'),
    path('establecer/direccion<int:pk>', views.check_direccion, name='check_direccion'),
    path('confirmacion', views.confirmacion, name='confirmacion'),
    path('cancelar', views.cancelar_orden, name='cancelar'),
    path('completado', views.completado, name='completado'),
    path('completados', views.OrdenViews.as_view(), name='completados'),
]