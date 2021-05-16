'''
creamos una ruta para los datos que estan en el modulo covid
aqui dejaremos las rutas para el navegador
'''

from covid import app   
import csv
import json

@app.route('/provincias')
def provincias (): 
    fichero = open ('data/provincias.csv', 'r') #abrimos el fichero provincias
    csvreader = csv.reader (fichero, delimiter =',') #ocupamos el metodo csv para delimitar la estructura ','

    lista = []
    for registro in csvreader:
        d = {'codigo':registro[0], 'provincia':registro[1]}
        lista.append (d)

    fichero.close()
    print(lista)
    return json.dumps(lista)

@app.route ('/provincia/<codigoProvincia>') #cuando se quiere ingresar un parametro y no un literal <>
def laprovincia(codigoProvincia): # dentro de la funcion debe ir el mismo nombre dentro de <>
    fichero = open ('data/provincias.csv', 'r')
    dictreader = csv.DictReader (fichero, fieldnames=['codigo','provincia'])
    for registro in dictreader:
        if registro ['codigo'] == codigoProvincia:
            return registro['provincia']

    fichero.close()
    return 'el valor no existe. largo de aqui!'


'''
@app.route ('/casos/<int:years>' defaults= {'mes'= None, 'dia'= None}) # Solo para que devuelva los valores del año
@app.route ('/casos/<int:years>/<int:mes>'defaults= {'dia'= None}) #Solo devuelve los valores año mes
'''

@app.route ('/casos/<int:years>/<int:mes>/<int:dia>')
def casos (years, mes, dia):
    pass

'''
1er caso: devolver el numero total de casos covid en un dia del año determinado para todas las provincias
2do caso . lo mismo pero detallado por tipo. PCR, AC, AG, ELISA, DESCONOCIDO - OTR
'''