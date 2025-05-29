from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

# Configuración conexión SQL Server
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=ParroquiasEclesiales;'
    'UID=sa;'
    'PWD=15987352'
)
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catequizados')
def ver_catequizados():
    cursor.execute("SELECT * FROM Catequizado")
    datos = cursor.fetchall()
    return render_template("ver_catequizados.html", catequizados=datos)

# ✅ Solo UNA función con la ruta /registrar
@app.route('/registrar')
def registrar():
    return render_template('formulario_catequizado.html')  # ← usa el nombre correcto

@app.route('/registrar', methods=['POST'])
def nuevo_catequizado():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    fecha_nacimiento = request.form['fecha_nacimiento']
    fe_bautizmo = request.form['fe_bautizmo']
    correo_contacto = request.form['correo_contacto']

    cursor.execute("""
        INSERT INTO Catequizado (nombre, apellido, fecha_nacimiento, fe_bautizmo, correo_contacto)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, apellido, fecha_nacimiento, fe_bautizmo, correo_contacto))
    conn.commit()

    return redirect('/catequizados')

# ✅ Ruta adicional: /nuevo redirige a /registrar
@app.route('/nuevo')
def redireccionar_a_formulario():
    return redirect('/registrar')

if __name__ == '__main__':
    app.run(debug=True)
