#INSTALACION




Crear el entorno virtual
- python -m venv venv

activarlo
- venv\Scripts\activate

instalar Flask
- pip install Flask


luego crear requerimientos del programa
- pip freeze > requerimientos.tx

instalar el entorno de desarrollo en python
- pip install python-dotenv

duplicar el fichero '.env_template' y renombrar a '.env'
los valores deben ser:
- Flask_APP = run.py
- FLASK_ENV = el que uno quiera


