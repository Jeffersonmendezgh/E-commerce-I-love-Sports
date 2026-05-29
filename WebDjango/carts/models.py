from django.db import models
from users.models import User
from products.models import Product
from django.db.models.deletion import CASCADE
from django.db.models.signals import pre_save, post_save
import uuid
import decimal
from django.db.models.signals import m2m_changed
from Orden.comun import OrdenStatus, choises
#entra en accion n*m 
class Cart(models.Model):
    cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProduct')#indica la realacion n*M con Product
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)


    FEE = 0.01
    
    def __str__(self):
        return self.cart_id #cuando se genere un id se refleje en la web
    
    def update_totals(self):#este metodo actualiza los dos siguientes
        self.update_subtotal()
        self.update_total()
        if self.orden:
            self.orden.update_total()

    def update_subtotal(self):#calcular suptotal
        self.subtotal = sum([#itera sobre nuestros elementos que esten en el carrito y trae el total
           i.quantity * i.product.price for i in self.product_related()])#product.price for product in..itera cada producto y acomula el precio
        self.save()

    def update_total(self):#tiene que eestar actualizado el subtotal
        self.total = self.subtotal + (self.subtotal * decimal.Decimal(Cart.FEE))#sum el recargo al subtotal para optener total final
        self.save()

    def product_related(self):#seleccionar todos los productos  para mostarrlos en la view mediante el metodo, al aprecer se adquiere todos los products qie esten en el cart
        return self.cartproduct_set.select_related('product')#-select_related Cuando traigas los objetos CartProduct, haz un JOIN con la tabla Product y carga esos datos en la misma consulta SQL.
    #@property; convierte el metodo en un atributo haciendolo mas natural de usar como si fuera un atrivuto mas del modelo
    @property
    def orden(self):#obtenemos un carrito siempre y cuendo la orden tenga status created
        return self.orden_set.filter(status=OrdenStatus.CREATED).first()#devuelve la primera orden asociada al carrito
    #como se llega hasta el campo status en orden? pues django crea una realacion  inversa en este caso orden_set
    #entonces orden_set es un queryset con todas las ordenes relacionadas con ese carrito
    #basicamente accedemos gracias a que este modelo es foreign key en el modelo orden
#clase para controlar la cantidad de nuestro products
class CartProductManager(models.Manager):
    def crear_actualizar(self, cart, product, quantity=1):
        object, created = self.get_or_create(cart=cart, product=product)#obtene o crea nuestro producto a partir de nuestro cart y product

        if not created:
            quantity = object.quantity + quantity
        object.update_quantity(quantity)
        return object
    
#modelo intermedio cart * product
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)

    objects = CartProductManager()

    def update_quantity(self, quantity=1):
        self.quantity = quantity
        self.save()

#generamos callv}bakc
def set_cart_id(sender,  instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())

#callback para las sumas no tiene que ver con el metodo
#django la ejecuta cuando cambia la relacion n * m Cart:products

def update_totals(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear': #action, cadena que describe que ocurrio en la relacion n*m  se genera al llamar metodos cart.products.add(product)etc
        instance.update_totals()#instance es el carrito afectado, update_totals para recalcular desdepues de ca,bios en carrito

#postsave para que se actualize despues de actualizar todos nuestros totales
def postActualizar(sender, instance, *args, **kwargs):
    instance.cart.update_totals()

post_save.connect(postActualizar, sender=CartProduct)

pre_save.connect(set_cart_id, sender=Cart)

#sender identifica que modelo disparo la señal, escucha la relacion n*m en este caso solo Cart.products
#entonces se crea modelo intermedio al crear relacion n*m
#en ese model se guarda cart_id y product_id y se accede a el con .through, aca posteriormente se crea el modelo manualmente y se le da el name CardProduct

m2m_changed.connect(update_totals, sender=Cart.products.through)#clave trough pq los cambios ocurren en esa tabla asi se identifica el product y carrito afectado

