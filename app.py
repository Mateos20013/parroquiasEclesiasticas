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

# RUTA PRINCIPAL
@app.route('/')
def index():
    return render_template('index.html')

# MOSTRAR TODOS LOS CATEQUIZADOS
@app.route('/catequizados')
def ver_catequizados():
    cursor.execute("""
        SELECT nombre, apellido, fecha_nacimiento, correo_contacto, fe_bautizmo, id_catequizando 
        FROM CATEQUIZADO
    """)
    datos = cursor.fetchall()
    return render_template("ver_catequizados.html", catequizados=datos)

# FORMULARIO PARA REGISTRAR
@app.route('/registrar')
def registrar():
    return render_template('formulario_catequizado.html')

# PROCESAR REGISTRO
@app.route('/registrar', methods=['POST'])
def nuevo_catequizado():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    fecha_nacimiento = request.form['fecha_nacimiento']
    fe_bautizmo = request.form['fe_bautizmo']
    correo_contacto = request.form['correo_contacto']

    cursor.execute("""
        INSERT INTO CATEQUIZADO (nombre, apellido, fecha_nacimiento, fe_bautizmo, correo_contacto)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, apellido, fecha_nacimiento, fe_bautizmo, correo_contacto))
    conn.commit()

    return redirect('/catequizados')

# REDIRECCIÓN OPCIONAL
@app.route('/nuevo')
def redireccionar_a_formulario():
    return redirect('/registrar')

# ELIMINAR CATEQUIZADO
@app.route('/eliminar/<int:id>')
def eliminar_catequizado(id):
    # Verifica si tiene inscripciones relacionadas
    cursor.execute("SELECT COUNT(*) FROM INSCRIPCION WHERE id_catequizando = ?", (id,))
    conteo = cursor.fetchone()[0]

    if conteo > 0:
        return "<h3 style='color:red;'> No se puede eliminar: este catequizado tiene inscripciones asociadas.</h3><a href='/catequizados'>Volver</a>"

    cursor.execute("DELETE FROM CATEQUIZADO WHERE id_catequizando = ?", (id,))
    conn.commit()
    return redirect('/catequizados')

# EDITAR CATEQUIZADO
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_catequizado(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento = request.form['fecha_nacimiento']
        fe_bautizmo = request.form['fe_bautizmo']
        correo_contacto = request.form['correo_contacto']

        cursor.execute("""
            UPDATE CATEQUIZADO
            SET nombre = ?, apellido = ?, fecha_nacimiento = ?, fe_bautizmo = ?, correo_contacto = ?
            WHERE id_catequizando = ?
        """, (nombre, apellido, fecha_nacimiento, fe_bautizmo, correo_contacto, id))
        conn.commit()
        return redirect('/catequizados')

    cursor.execute("SELECT * FROM CATEQUIZADO WHERE id_catequizando = ?", (id,))
    catequizado = cursor.fetchone()
    return render_template('editar_catequizado.html', c=catequizado)

# INICIO DE FLASK
if __name__ == '__main__':
    app.run(debug=True)
