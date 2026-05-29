from django.db import models
import random
import string
from django.db.models.signals import pre_save
from django.utils import timezone

class PromoCodigoManager(models.Manager):

    def get_validar(self, code):
        actual = timezone.now()

        return self.filter(codigo=code).filter(used=False).filter(fecha_inicio__lte=actual).filter(fecha_final__gte=actual).first()


class PromoCodigo(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descuento = models.FloatField(default=0.0)
    fecha_inicio = models.DateTimeField()
    fecha_final = models.DateTimeField()
    used = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)


    objects = PromoCodigoManager()

    def __str__(self):
        return self.codigo
    #codigo usado
    def codigo_usado(self):
        self.used = True
        self.save()

#recordemos: sender modelo que dispara la señal PromoCOdigo en este caso
# instance: instance del modelo que se esta guardando
# *args **kwargs: argumentos adiccionales que django pasa a la señal   
def set_codigo(sender, instance, *args, **kwargs):
    if instance.codigo:#si la instancia ya tiene un codigo asignado no hace nada
        return
    
    coders = string.ascii_uppercase + string.digits#crea caracters a-z y o-9
    instance.codigo = ''.join(random.choice(coders) for _ in range(5))#genera cadena aleatoria de 5 cartsrs y se asigna a codigo en la instacia acltual

pre_save.connect(set_codigo, sender=PromoCodigo)#ahora django ejecuta set_codigo antes de hacer insert o update