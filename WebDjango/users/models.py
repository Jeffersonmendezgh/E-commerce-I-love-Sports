from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from Orden.comun import OrdenStatus

"""AbstractUser modelo completo con toda la logica de autenticacion y permisos
 pero que se puede extender con mas campos y metodos
User no se le puede cambiar nada de lo que trae por defecto
AbstractBaseUser modelo basico toca definir casi todo, login, permisos etc """

class User(AbstractUser): #nuestro model heredara todos los campos y metodos de AbstractUser
    def get_full_name(self) -> str:#sobreescribimos este metodo para que devuelva los campos a continuacion
        def get_full_name(self):#este metodo ya lo tiene la clase devuelve frist_name y last_name osea el nombre
            return '{},{}'.format(self.first_name, self.last_name)#devuelve nombre y apellido pero ahora con ,

    @property #decorador para la direccion_envio lo combertimos en una propiedad y luego lo usamos como si fuera un atributo
    def direccion_envio(self):
        return self.direccionenvio_set.filter(default=True).first()
    #direccionenvio_set;es la realacion inversa:todas las direcciones asiciadas al usuario
    #filtra la primera, trayendo la direccion actual por default del usuario
    def has_direccion_envio(self):#este metodo devuelve true si el usuario tiene direccion default, y false si no tiene
        return self.direccion_envio is not None

    #metodo para obtener las ordenes completadas
    def ordenes_completadas(self):
        return self.orden_set.filter(status=OrdenStatus.COMPLETED).order_by('-id')#ordenar por id 
#OneToOneFiel()


class Cliente(User):#clase que nos permite obtener los usuarios
    class Meta:
        proxy = True

    def get_product(self):
        return []
# 1 * 1 si el usuario se borra se borra el profile tambien.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    biografia = models.TextField()
