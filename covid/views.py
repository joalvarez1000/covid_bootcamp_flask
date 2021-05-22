'''
creamos una ruta para los datos que estan en el modulo covid
aqui dejaremos las rutas para el navegador
'''
from flask import render_template, request
from covid import app   
import csv
import json
from datetime import date

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

@app.route ('/casos/<int:year>', defaults  = {'mes' : None, 'dia': None}) # Solo para que devuelva los valores del año
@app.route ('/casos/<int:year>/<int:mes>') #Solo devuelve los valores año mes
@app.route ('/casos/<int:year>/<int:mes>/<int:dia>')
def casos (year, mes, dia = None):
    
    
    if not mes:
        fecha = "{:04d}".format(year)
    elif not dia:
        fecha = "{:04d}-{:02d}".format(year,mes)
    else:
        fecha = "{:04d}-{:02d}-{:02d}".format(year,mes,dia)
    
    fichero = open ('data/casos_diagnostico_provincia.csv', 'r')
    dictreader = csv.DictReader (fichero)

    res = {
        'num_casos' : 0,
        'num_casos_prueba_pcr' : 0,
        'num_casos_prueba_test_ac' : 0,
        'num_casos_prueba_ag' :0,
        'num_casos_prueba_elisa' : 0,
        'num_casos_prueba_desconocida' : 0
    }

    
    for registro in dictreader:
        if fecha in registro ['fecha']:
            for clave in res:
                res[clave] += int (registro[clave])

        elif registro['fecha'] > fecha:
            break
        
    fichero.close()
    return json.dumps(res)
            
'''
1er caso: devolver el numero total de casos covid en un dia del año determinado para todas las provincias
2do caso . lo mismo pero detallado por tipo. PCR, AC, AG, ELISA, DESCONOCIDO - OTR
'''

@app.route ('/incidenciasdiarias', methods =['GET', 'POST'])
def incidencia():
    
    
    #Validar que los valores de los casos sean números y sean enteros positivos
    #estudiar objeto request de la libreria
    #vslorar num_casos_prueba_pcr >= 0 y entero
    formulario = {
        'provincia': '',
        'fecha': str(date.today()),
        'num_casos_prueba_pcr': 0,
        'num_casos_prueba_test_ac': 0, 
        'num_casos_prueba_ag': 0,
        'num_casos_prueba_elisa': 0,
        'num_casos_prueba_desconocida': 0
    }

    fichero = open ('data/provincias.csv', 'r')
    csvreader = csv.reader (fichero, delimiter =',') #ocupamos el metodo csv para delimitar la estructura ','
    next(csvreader)
    lista = []
    for registro in csvreader:
        d = {'codigo':registro[0], 'descripcion' : registro[1]}
        lista.append (d)

    fichero.close()

    if request.method == 'GET':
        return render_template("alta.html", datos=formulario, 
                               provincias=lista, error="")
    
    #validar que num_casos en general no es negativo

    for clave in formulario:
        formulario[clave] = request.form [clave]


    num_pcr = request.form ('num_casos_prueba_pcr')
    try:
        num_pcr = int (num_pcr)
        if num_pcr < 0:
            raise ValueError ('Debe ser no negativo')

    except ValueError:
        return render_template("alta.html", datos=formulario, error = "PCR no puede ser negativa")
    
    return "Se ha hecho un post"