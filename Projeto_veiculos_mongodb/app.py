from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
db = client.veiculos
collection_carros = db.carros


@app.route("/")
def index():
    carros = list(collection_carros.find({}))
    return render_template("index.html", carros=carros)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'GET':
        return render_template("create.html")
    elif request.method == 'POST':
        data = request.form
        carro = {
            'marca': data.get('marca'),
            'modelo': data.get('modelo'),
            'ano': data.get('ano'),
            'preco': data.get('preco'),
            'categoria': data.get('categoria'),
            'fabricante': data.get('fabricante')
        }
        result = collection_carros.insert_one(carro)
        return redirect(url_for('index'))


@app.route('/read')
def read():
    carros = list(collection_carros.find({}))
    return render_template("read.html", carros=carros)


@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'GET':
        carro = collection_carros.find_one({"_id": ObjectId(id)})
        return render_template("edit.html", carro=carro)
    elif request.method == 'POST':
        data = request.form
        carro = {
            'marca': data.get('marca'),
            'modelo': data.get('modelo'),
            'ano': data.get('ano'),
            'preco': data.get('preco'),
            'categoria': data.get('categoria'),
            'fabricante': data.get('fabricante')
        }
        collection_carros.update_one({"_id": ObjectId(id)}, {"$set": carro})
        return redirect(url_for('index'))


@app.route('/delete/<string:id>', methods=['GET'])
def delete(id):
    collection_carros.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


@app.route('/search_by_id/<string:id>', methods=['GET'])
def search_by_id(id):
    carro = collection_carros.find_one({"_id": ObjectId(id)})

    if carro:
        return render_template("search_by_id.html", carro=carro)  # Página de detalhes do carro
    else:
        return render_template("search_by_id.html", error="Carro não encontrado.")  # Exibir mensagem de erro


if __name__ == "__main__":
    app.run(debug=True)
