from django.contrib import admin
from .models import PromoCodigo
#clase para excluir campo del admin
class CodigoPromoAdmin(admin.ModelAdmin):
    exclude = ['codigo']

admin.site.register(PromoCodigo, CodigoPromoAdmin)
