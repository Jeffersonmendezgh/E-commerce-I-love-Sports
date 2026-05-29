#funcion para dar formato tipo js a los precios


from django import template

register = template.Library()#django, reconosca las nuevas herramientas que vamos acrear aca

@register.filter()#indica a django q la funcion a continuacion es un filtro para usar en el html
def precio_tag(value):#value:dato que esta e la izquierda en el html
    return '${0:.2f}'.format(value)
#{} lugar a insertar la variable, value en este caso
#0: PRIMER argumento pasado a format
#: separa la referencia de la variable de instrucciones
#.2 precision decimal, mostrara 2 en este caso
#f punto fijo, indica a python que trate como decimal
#$texto
