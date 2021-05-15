'''
creamos la aplicacions
'''

from flask import Flask

app = Flask (__name__) #instanciamos Flask

from covid import views #nos traemos la ruta del fichero views

