from django.forms import ModelForm
from .models import DireccionEnvio

class DireccionEnvioForm(ModelForm):
    class Meta:
        model = DireccionEnvio
        fields = [
            'line1', 'line2', 'city', 'state', 'country', 'postal_code', 'reference'
        ]

        labels = {
            'line1':'calle 1',
            'line2':'calle 2',
            'city':'ciudad',
            'state':'estado',
            'country':'pais',
            'postal_code':'codigo postal',
            'reference':'referencia'
        }

    def __init__(self, *args, **kwargs):#sobreescribimos el constructor del form, asi modificamos los campos despues de que django los cree automatic
        super().__init__(*args, **kwargs)#llamamos constructor original de ModelForm asi django inicializa los campos normalmente


        self.fields['line1'].widget.attrs.update({
            'class': 'form-control'
        })
    #self.fiels.['line1'] accedemos a ese campo cada campo tiene un widget q es el objeto responsable de renderizar el input html
    # .widget.attrs.update class form-control; modificamos los atributos html del widget en este caso añadimos una clase css asi se aplica al input generado    
        self.fields['line2'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['city'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['state'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['country'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['postal_code'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '7600'
        })

        self.fields['reference'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'porton blanco'
        })

#OBJETO WIDGET
#que es? objeto responsable de renderizar el input html de un campo de form
#cada campo charfield, integerfield etc, tiene un widget asociado por defecto
#ejemplo: CartField usa TextInput, BooleanField usa CheckbocInput
#el widget no valida datos, solo se muestra y como se recibe la entrada html
#COMO FUNCIONA: al definir un form en django creamos campos, cada campo tiene un widget que sabe: que tipo de etiqueta html usar; input, select etc
#que atributos poner; class placeholder id etc, como renderizar en el template en este caso cuando hacemos {{field}}
