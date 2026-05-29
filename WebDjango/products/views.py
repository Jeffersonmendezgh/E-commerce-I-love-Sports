from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Product
from django.views.generic.detail import DetailView
from django.db.models import Q #clase que permite convinasciones avanzadas usando and || 


class ProductListView(ListView):
    template_name = 'index.html'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['mensaje'] = 'Productossss'

        return context


#esta detail view solo tiene metodo get obtenemos el objeto con el alias del modelo en este caso product
class ProductDetailview(DetailView):
    model = Product #nombre que se le pasa al objeto en minusculas
    template_name = 'products/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
#clase para busqueda
# clave, no olivdar que un listwiew django pasa la lista de objetos como object_list
#pero los guarda con un alias que es el nombre del modelo en minusculas product_list en este caso
class ProductSearchListView(ListView):
    template_name = 'products/search.html'

    def get_queryset(self):
        filters = Q(title__icontains=self.query() ) | Q(category__title__icontains=self.query())
        return Product.objects.filter(filters)#icontains busca sin importar a-A y coincidencias, y query es el metodo de abajo
    
    def query(self):#self.get es el objeto HTTPRequest
        return self.request.GET.get('i')#busca el parametro i en la url esta get i es el nombre en el form search
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)#llamamos al metodo original para no perder las variables que ya pone django como object_list
        context['query'] = self.query()#agregamos la variable query al contexto asi la plantilla puede buscar el termino buscado
        return context