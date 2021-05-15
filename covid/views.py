'''
creamos una ruta para los datos que estan en el modulo covid
aqui dejaremos las rutas
'''

from covid import app   

@app.route('/')

def index (): #puedo colocar el nombre que yo quiera
    return 'Flask esta funcionando desde views!'