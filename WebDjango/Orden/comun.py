from enum import Enum

class OrdenStatus(Enum):#enum = define un connjunto fijo de estados posibles para una orden
    CREATED = 'CREATED'
    PAYED = 'PAYED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'
    #al usar enum evitamos usar valores arbitrarios en el campo status de el siguiente modelo, asi usamos solamente estos

choises = [(tag, tag.value) for tag in OrdenStatus]#recorre todos los mienbros del enum y genera una lista de tuplas
#entonces choises se convierte en una lista de tuplas valor:etiqueta, el valor es el miembro del enum
#created etc y la etiqueta es su valor osea la cadena text
#esto permite que estas opciones se muestren en un menu desplegable
