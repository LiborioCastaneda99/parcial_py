from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configura la conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="py"
)

cursor = db.cursor()

# Rutas del API
@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    cursor.execute("SELECT id, nombre, email FROM clientes")
    clientes = cursor.fetchall()
    clientes_list = [{'id': cliente[0], 'nombre': cliente[1], 'email': cliente[2]} for cliente in clientes]
    return jsonify(clientes_list)

@app.route('/api/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    cursor.execute("SELECT id, nombre, email FROM clientes WHERE id = %s", (cliente_id,))
    cliente = cursor.fetchone()
    if cliente:
        return jsonify({'id': cliente[0], 'nombre': cliente[1], 'email': cliente[2]})
    else:
        return jsonify({'error': 'Cliente no encontrado'}), 404

@app.route('/api/clientes', methods=['POST'])
def create_cliente():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')

    # Validar que los campos obligatorios están presentes
    if not nombre or not email:
        return jsonify({'error': 'Nombre y email son campos obligatorios'}), 400

    # Insertar nuevo cliente en la base de datos
    cursor.execute("INSERT INTO clientes (nombre, email) VALUES (%s, %s)", (nombre, email))
    db.commit()

    return jsonify({'mensaje': 'Cliente creado satisfactoriamente'}), 201

@app.route('/api/clientes/<int:cliente_id>', methods=['PUT'])
def update_cliente(cliente_id):
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')

    # Validar que los campos obligatorios están presentes
    if not nombre or not email:
        return jsonify({'error': 'Nombre y email son campos obligatorios'}), 400

    # Actualizar cliente en la base de datos
    cursor.execute("UPDATE clientes SET nombre=%s, email=%s WHERE id=%s", (nombre, email, cliente_id))
    db.commit()

    return jsonify({'mensaje': 'Cliente actualizado satisfactoriamente'})

@app.route('/api/clientes/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    # Eliminar cliente de la base de datos
    cursor.execute("DELETE FROM clientes WHERE id=%s", (cliente_id,))
    db.commit()

    return jsonify({'mensaje': 'Cliente eliminado satisfactoriamente'})

if __name__ == '__main__':
    app.run(debug=True)
