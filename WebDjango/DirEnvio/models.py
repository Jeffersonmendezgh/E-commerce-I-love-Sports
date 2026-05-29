from django.db import models
from users.models import User

class DireccionEnvio(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    line1 = models.CharField(max_length=300)
    line2 = models.CharField(max_length=300, blank=True)# si usuario no tiene direccion la puede dejar en blanco
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    reference = models.CharField(max_length=300)
    postal_code = models.CharField(max_length=10, null=False, blank=False)
    default = models.BooleanField(default=False)
    create_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.postal_code
    #metodo para actualizar la direccion_envio
    #cambia el valor del campo default, si no pasamos nada lo pone False
    #si pasamos true lo marca como default
    def update_default(self, default=False):
        self.default = default
        self.save()
    #metodo para que si una direccion esta asocuada auna orden no se elimine
    def has_orden(self):
        return self.orden_set.count() >= 1

    @property
    def direccion(self):
        return '{},{},{}'.format(self.city, self.state, self.country)#cada llavesita llevara una variable de estas de format