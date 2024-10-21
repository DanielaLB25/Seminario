from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Cargar los inscritos de un archivo JSON
def cargar_inscritos():
    try:
        with open('inscritos.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Guardar los inscritos en el archivo JSON
def guardar_inscritos(inscritos):
    with open('inscritos.json', 'w') as file:
        json.dump(inscritos, file)

# Página de registro
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        turno = request.form['turno']
        seminarios = request.form.getlist('seminarios')

        # Cargar inscritos existentes
        inscritos = cargar_inscritos()

        # Agregar nuevo inscrito
        inscritos.append({
            'fecha': fecha,
            'nombre': nombre,
            'apellidos': apellidos,
            'turno': turno,
            'seminarios': seminarios
        })

        # Guardar inscritos actualizados
        guardar_inscritos(inscritos)

        return redirect(url_for('inscritos'))

    return render_template('index.html')

# Página de lista de inscritos
@app.route('/inscritos')
def inscritos():
    inscritos = cargar_inscritos()
    return render_template('inscritos.html', inscritos=inscritos)

# Ruta para eliminar inscrito
@app.route('/eliminar/<int:id>')
def eliminar(id):
    inscritos = cargar_inscritos()
    if 0 <= id < len(inscritos):
        del inscritos[id]
        guardar_inscritos(inscritos)
    return redirect(url_for('inscritos'))

# Iniciar la app
if __name__ == '__main__':
    app.run(debug=True)

