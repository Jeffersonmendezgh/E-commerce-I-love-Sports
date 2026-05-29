from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from uuid import uuid4
# Create your models here.
#nosotros heredamos de model y modeles las columnas de la db
class Product(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)# dos digitos mas despues del punto
    image = models.ImageField(upload_to='products/', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    slug = models.SlugField(max_length=200, null=False, blank=False, unique=True)

    
    def __str__(self): #self hace referencia a todo el objeto que se forma
        return self.title #__str__ representación en texto de el objeto en texto.
    
def new_slug(sender, instance,*arg, **kwargs):#sender es el model y instance es todo el object de la clase
    if instance.title and not instance.slug:
        slug = slugify(instance.title)

        while Product.objects.filter(slug=slug).exists():
            slug = slugify(
                '{}-{}'.format(instance.title, str(uuid4())[:8])#uuid4 entonces genera code random :8 toma 8 caracteres
            )

        instance.slug = slug

pre_save.connect(new_slug, sender=Product)#antes de guardar un producto nuevo, genera el slug

