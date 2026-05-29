from django.shortcuts import render, get_object_or_404
from .models import DireccionEnvio
from django.views.generic import ListView #listview; vista generica de django, sirve para mostrar una lista de objetos de un modelo
from .form import DireccionEnvioForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from carts.funciones import funcionCarrito
from Orden.utils import funcion_orden
from django.http.response import HttpResponseRedirect

class EnvioDirecciones(LoginRequiredMixin, ListView):
    login_url = 'login' #si queremos entrar a direcciones lo enviara a login
    model = DireccionEnvio#pasamos a la vista el modelo que vamos a listar, en este caso todas las dir de envio
    template_name = 'direccion_envio/direccion_envio.html'
#por defecto listWiew mostrara todas las direcciones
#entonces a continuacion lo personalizamos para que muestre solo direcciones del usuario actual
    def get_queryset(self):
        return DireccionEnvio.objects.filter(user=self.request.user).order_by('-default')
        #filter(user=self.request.user);filtra las direcciones de envio que pertenecen al usuario autenticado en la peticion request.user
    #order_by 'default'; ordena las direcciones por el campo default, -significa descendente, ordenara y la predeterminada aparecera primero
#LISTAR; traer varios objetos y mostrarlos en pantalla uno tras otro
#entonces aca traemos todas las DIreccionesEnvio que pertenecen al user actual,   y las pasamos al template como una objet_list en donde se usaran

#- DetailView → muestra un solo objeto (ej. una dirección específica).
#- ListView → muestra varios objetos (ej. todas las direcciones del usuario)
@login_required(login_url='login')
def form_direccion(request):
    form = DireccionEnvioForm(request.POST or None)# cargamos todos los datos

    if request.method == 'POST' and form.is_valid: #verificamos que se enviara el formulario y que los datos seaan correctos
        direccion_envio = form.save(commit=False) #creamos el objeto pero no lo guardamos todavia, permite modificar campos
        direccion_envio.user = request.user #asignamos al usuario actual la direccion de envio, vinculando direccion a cada usuario que la creo
        direccion_envio.default = not request.user.has_direccion_envio()#sino tiene relacion se la creamos

        direccion_envio.save()

        if request.GET.get('next'):
            if request.GET['next'] == reverse('direccion'):
                cart = funcionCarrito(request)
                orden = funcion_orden(cart, request)

                orden.update_direccion_envio(direccion_envio)

                return HttpResponseRedirect(request.GET['next'])

        messages.success(request, 'Direccion creada correctamente')
        return redirect('direccion_envio')


    return render(request, 'direccion_envio/form.html',{
        'form':form
    })


class UpdateDireccion(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login' #loginrequiredmixin restringe acceso, solo users auth accederan, login es para redirijir si no esta autenticado
    model = DireccionEnvio #django usara este modelo para buscar su direccion mediante su pk
    form_class = DireccionEnvioForm #es el form que se usara para renderizar los datos que vamos a actualziar
    template_name = 'direccion_envio/actualizar.html'
    success_message = 'Enhorabuena Direccion Actualizada'  #sucessmessagemixin permite mostrar el mensaje de exito que definimos en succes_messajes

    def get_success_url(self):
        return reverse('direccion_envio')#rederigimos a direccion_envio
    
#clase para eliminar
class DeleteDireccion(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = DireccionEnvio
    template_name = 'direccion_envio/delete.html'
    success_url = reverse_lazy('direccion_envio') #cuando la elimine se redirije a esta url
    #metodo para seguridad por si alguien ejecuta un ataque para eliminar las direcciones
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().default:
            return redirect('direccion_envio')
        
        if self.get_object().has_orden():
            messages.error(request, "No se puede eliminar direccion asociada a la orden")
            return redirect('direccion_envio')
        
        if request.user.id != self.get_object().user_id:
            return redirect('index')
        
        return super(DeleteDireccion, self).dispatch(request, *args, **kwargs)
    #flujo de esta clase
    """
    - El objeto se elimina en el método post() de DeleteView
    - El pk llega desde la URL (<int:pk>
    - Django usa ese pk para buscar el objeto en el modelo (get_object())
    - Tu dispatch añade seguridad antes de permitir la eliminación
el delete lo ejecuta internamete la clase DeleteView
    """
@login_required(login_url='login')
def FuncDefault(request, pk):
    direccion_envio = get_object_or_404(DireccionEnvio, pk=pk)#busca la direccion con el pk que llega en la url 

    if request.user.id != direccion_envio.user_id:#si el user que hace la request es != a la direccion actual redirijimos
        return redirect('index')
    #ahora, este metodo verifica si el usuario ya tiene direccion default
    #de ser asi entonces desmarcarla para ponerla nue
    if request.user.has_direccion_envio():
        request.user.direccion_envio.update_default() #request.user.direccion_envio, obtiene la direccion actual por defecto del usuario
        #llama al metodo update_default() sin parametros que por defecto esta False, asi se desmarca la direccion como default

    direccion_envio.update_default(True)#marca la direccion nueva que llego por pk como default

    return redirect('direccion_envio')
