from django.urls import path
from .import views

urlpatterns = [
    path('', views.EnvioDirecciones.as_view(), name='direccion_envio'),
    path('nueva', views.form_direccion, name='form_direccion'),
    path('editar/<int:pk>', views.UpdateDireccion.as_view(), name='update'),
    path('eliminar/<int:pk>', views.DeleteDireccion.as_view(), name='remove'),
    path('default/<int:pk>', views.FuncDefault, name='default'),
]

#<int:pk> le dice a django "esta ruta espera un int llamado pk"
#el navegador ejecuta la ruta y django captura el pk= y lo pasa como argumento a la view 
"""ejemplo del objeto que se arma
Dentro de ese objeto tienes:
- request.method → "GET" (porque el enlace dispara un GET).
- request.user → el usuario autenticado que hizo clic.
- request.path → "/direccion_envio/default/7/".
- request.GET → parámetros de query string (si hubiera, ej. ?next=/orden/).
- request.POST → vacío en este caso, porque es un GET.
- request.session → datos de sesión del usuario.
Y además, Django pasa el pk como argumento separado a tu función:
"""