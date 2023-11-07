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
    return redirect(url_for('read'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        car_id = request.form.get('car_id')
        carro = collection_carros.find_one({"_id": ObjectId(car_id)})

        if carro:
            return render_template("search_result.html", carro=carro)
        else:
            return render_template("search_result.html", error="Carro não encontrado.")

    return render_template("search.html")



if __name__ == "__main__":
    app.run(debug=True)
