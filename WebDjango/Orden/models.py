from django.db import models
from users.models import User
from carts.models import Cart
from promo_codigo.models import PromoCodigo
from DirEnvio.models import DireccionEnvio
from enum import Enum
from django.db.models.signals import pre_save
import uuid
from .comun import OrdenStatus
from .comun import choises
import decimal






#RELACIONES 
#ForeignKey: muchas instancias de este modelo pueden apuntar a una sola instancia del modelo relacionado
#en este caso 1 usuario muchas ordenes, todas las ordenes tienen el mismo user_id
#entonces cada orden tendra su id de usuario aca que al final pueden ser muchas ordenes
class Orden(models.Model):
    orden_id = models.CharField(max_length=100, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)#relacion con el usuario que hizo la orden, cascade:si se borra el user tambien la orden
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)#relacion con el carrito que genera la orden
    status = models.CharField(max_length=40, choices=choises, default=OrdenStatus.CREATED)#al usar choise solo puede tomar los valores del enum arriba
    envio_total = models.DecimalField(default=10, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=9, decimal_places=2)#subtatotal del carrito + envio
    created_at = models.DateTimeField(auto_now_add=True)
    direccion_envio = models.ForeignKey(DireccionEnvio, null=True, blank=True, on_delete=models.CASCADE) #relacion direccionEnvio y Orden
    promo_codigo = models.OneToOneField(PromoCodigo, null=True, blank=True, on_delete=models.CASCADE)#ahora usuario puede comprar orden sin tener codigo de promocion

    def __str__(self):
        return self.orden_id
    
    def aplicarCodigo(self, promo_codigo):
        if self.promo_codigo is None:
            self.promo_codigo = promo_codigo
            self.save()

            self.update_total()
            promo_codigo.codigo_usado()#cuando se use se marcara a true en el metodo promo_codigo

    def get_descuento(self):
        if self.promo_codigo:
            return self.promo_codigo.descuento
        
        return 0
    
    #suma del total mas el impuesto para mostrarlo en detalle del pedido
    def get_total(self):#toma el total del carrito y le suma el costo del envio y devuleve el resultado
        return self.cart.total + self.envio_total - decimal.Decimal(self.get_descuento()) #retornara tambien el descuento en caso de que exista el codigo
    
    def update_total(self):#llama a get total para calcular el monto final
        self.total = self.get_total()#se asigna el valor calculado a  self.total de la orden
        self.save()

    #obtener direccion envio si hay
    def get_or_set_direccion_envio(self):
        if self.direccion_envio:
            return self.direccion_envio
        direccion_envio = self.user.direccion_envio
        if direccion_envio:
            self.update_direccion_envio(direccion_envio)
            
        return direccion_envio #entonces usamos por defecto la que tenga

    #metodo para cancelar orden, guarda el cambio en la db, 
    def cancelar(self):
        self.status = OrdenStatus.CANCELED
        self.save()
#metodo para marcar como completada la orden
    def completado(self):
        self.status = OrdenStatus.COMPLETED
        self.save()

    def update_direccion_envio(self, direccion_envio):
        self.direccion_envio = direccion_envio
        self.save()

def enviarOrden(sender, instance, *args, **kwargs):
    if not instance.orden_id:#antes de guardar orden pre_save verifica sino tiene orden_id y le asigna uno
        instance.orden_id = str(uuid.uuid4())

#nuevo signal, antes de guardar todo con pre_save, recalcula el total
#usando get_total() y asigna el valor al campo total
def enviar_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()

#conectamos las funciones a la señal pre_save del modelo Orden
#aseguramos que tenga orden_id y recalculamos el total
pre_save.connect(enviarOrden, sender=Orden)
pre_save.connect(enviar_total, sender=Orden)#sender modelo que dispara el objbeto

#sender: modelo o clase que dispara la señal, "es quien activo la señal"
#instance: es la instancia especifica del modelo que esta siendo guradada o modificada
#por ejemplo, si guardamos una orden con id5 instance es ese objeto, es el que realmente se esta procesando en ese momento
# *args: argumentos pocicionales,
# **kwargs: dic con info extra, por ejemplo; update_fields si se esta guardando solo ciertos campos,
#raw: si el objeto se esta cargando desde fixtures
#using: que db se esta usando si hay varias
#created: en señales como post_save indica si el objeto fue creado o actualizado