from django import forms
#from django.contrib.auth.models import User ahora no se usara el deault
from users.models import User # el nuestro
from django.forms.widgets import EmailInput

class Registro(forms.Form):
    username = forms.CharField(required=True, min_length=5, max_length=40, #maximo de caracteres y maximo
    widget=forms.TextInput(attrs={#widget objeto que ayuda a renderizar html, en este caso se le pasa clases y un placeholder
        'class':'form-control',
        'placeholder':'usuario'
      }))
    correo = forms.EmailField(required=True, widget=forms.EmailInput(attrs={#attrs significca los atrivutos que le vamos a pasar
        'class':'form-control',
        'placeholder':'correo'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'contraseña'
    }))
#nuevo campo para confirmar contraseña
    password2 = forms.CharField(label='COndirmar contraseña', required=True, widget=forms.PasswordInput
    (attrs={
           'class':'form-control',
           'placeholder':"Confirmar contraseña"                                                                   
    }))
    
#funcion para validacion
    def clean_username(self):
        username = self.cleaned_data.get('username')#obtenemos el valor que el usuario escribio en campo correo

        if User.objects.filter(username=username).exists():#filtramos para ver si hay un usuario igual
            raise forms.ValidationError('Usuario ya existe')
        
        return username #si no hay error que retorne el username
    #se crean metodos especiales  llanados clean_nombre_del campo
    #asi se se hacen validaciones personalizadas para campos especificos
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')

        if User.objects.filter(email=correo).exists():
            raise forms.ValidationError('correo ya registrado')
        
        return correo
    
    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password2') != cleaned_data.get('password'): #si el campo de arriba no es igual al segundo campo
            self.add_error('password2', 'La contraseña no coincide')#se lanza error
    

    #save metodo para obtener los datos que entran y guardarlos, lo mismo que teniamos en la wiew
    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('correo'),
            self.cleaned_data.get('password')
        )