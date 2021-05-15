'''
creamos la aplicacions
'''

from flask import Flask


app = Flask (__name__) #instanciamos Flask

'''
creamos una ruta
'''

@app.route('/')

def index (): #puedo colocar el nombre que yo quiera
    return 'Flask esta funcionando'

