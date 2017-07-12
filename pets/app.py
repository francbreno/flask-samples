from flask import Flask, request, abort, json

# cria uma application instance
app = Flask(__name__) # nome do main module para o Flask determinar o root path

last_index = 3
pets = [
    {
        'id': 1,
        'name': 'Ralf',
        'genero': 'Cachorro',
        'idade': 6
    },
    {
        'id': 2,
        'name': 'Tinx',
        'genero': 'Gato',
        'idade': 2
    },
    {
        'id': 3,
        'name': 'Bozo',
        'genero': 'Periquito',
        'idade': 1
    }
]

@app.route('/')
def index():
    return "<h1>Bad Request</h1>", 400

@app.route('/pets', methods=['GET'])
def all_pets():
    return json.jsonify(pets)

@app.route('/pets/<int:id>', methods=['GET'])
def pet(id):
    pet = load_pet_or_404(id)
    return json.jsonify(pet)

@app.route('/pets', methods=['POST'])
def add_pet():
    new_pet = request.json

    global last_index
    last_index += 1
    new_pet['id'] = last_index

    pets.append(new_pet)

    return json.jsonify({ 'url': "http://localhost:5000/pets/{}".format(new_pet['id']) }), 201

@app.route('/pets/<int:id>', methods=['DELETE'])
def remove_pet(id):
    pet = load_pet_or_404(id)

    global pets
    pets = filter(lambda p: p['id'] != id, pets)

    return json.jsonify(''), 204

@app.route('/pets/<int:id>', methods=['PATCH'])
def update_pet_property(id):
    pet = load_pet_or_404(id)

    properties = request.json
    if 'nome' in properties:
        pet['nome'] = properties['nome']
    if 'genero' in properties:
        pet['genero'] = properties['genero']
    if 'idade' in properties:
        pet['idade'] = properties['idade']

    return json.jsonify({ 'url': "http://localhost:5000/pets/{}".format(pet['id']) }), 200

@app.route('/pets/<int:id>', methods=['PUT'])
def update_pet(id):
    pass

@app.errorhandler(404)
def page_not_found(e):
    return json.jsonify({ 'message': 'Página não encontrada. Que pena!' }), 404

def load_pet_or_404(id):
    pet = next((p for p in pets if p['id'] == id), None)
    if not pet:
        abort(404)
    return pet

if __name__ == '__main__':
    app.run(debug=True)
