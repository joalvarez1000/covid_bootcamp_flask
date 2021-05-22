'''
creamos una ruta para los datos que estan en el modulo covid
aqui dejaremos las rutas para el navegador
'''
from flask import render_template, request
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
    if request.method == 'GET':
        return render_template("alta.html", casos_pcr=0)
    
    #Validar que los valores de los casos sean números y sean enteros positivos
    #estudiar objeto request de la libreria
    Valores = request.form
    #vslorar num_casos_prueba_pcr >= 0 y entero
    try:
        num_pcr = int(request.form["num_casos_prueba_pcr"])
        if num_pcr < 0:
            raise ValueError('Debe ser positivo')
    except ValueError:
        return render_template("alta.html", casos_pcr="Introduce un valor correcto")
    
    #Validar la información que llega
    #Que el total de casos sea la suma del resto de casos
    #Que la provincia sea correcta
    #Que la fecha sea correcta en formato y supongo que en valor
    #Que la fecha no sea a futuro y la fecha no sea anterior a fecha covid
    #Si la informacion es incorrecta
    return "Se ha hecho un post"