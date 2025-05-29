from flask import Flask, render_template, request, redirect
import pyodbc
import json

app = Flask(__name__)

# Conexión desde config.json
with open('config.json') as config_file:
    config = json.load(config_file)

connection_string = (
    f"DRIVER={config['driver']};"
    f"SERVER={config['server']};"
    f"DATABASE={config['database']};"
    f"UID={config['user']};"
    f"PWD={config['password']};"
    f"TrustServerCertificate=yes"
)

conexion = pyodbc.connect(connection_string)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catequizados')
def listar_catequizados():
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM CATEQUIZADO")
    datos = cursor.fetchall()
    return render_template('listar_catequizados.html', catequizados=datos)

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo_catequizado():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        grupo = request.form['grupo']
        correo = request.form['correo']
        
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO CATEQUIZADO (Nombre, Apellido, Edad, Grupo, Correo)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, apellido, edad, grupo, correo))
        conexion.commit()
        return redirect('/catequizados')

    return render_template('formulario_catequizado.html')

if __name__ == '__main__':
    app.run(debug=True)
