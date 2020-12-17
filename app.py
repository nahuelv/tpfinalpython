from flask import (
    Flask, render_template, request,jsonify
)

import requests
from db import *




user = ""
idUsuarioLogeado= None

crear_tabla()



app = Flask(__name__)




@app.route('/')
def main():
    #peliculas = f['results']
    #return render_template('index.html',peliculas = peliculas)

    return render_template('index.html',user = user)


@app.route('/listado',methods=['POST'])
def listado():
    if request.method == 'POST':
        name = request.form['inputName']
        x = requests.get(
        'https://api.themoviedb.org/3/search/movie?api_key=6427e11274426be9030b97aab51ef6f8&query='+name)
        f = x.json()
        global peliculas
        peliculas= f['results']


@app.route('/lista')
def lista ():
    categorias = obtener_categorias()
    return render_template('listado.html', peliculas=peliculas,categorias=categorias,user = user)


def registrar(name,passw):

    msg = ''
    if buscarPersona(name) == False:
        alta_usuario(name,passw)
        msg = "0" #usuario creado
    else:
        msg = "1"  #usuario no creado

    return msg


@app.route('/registro',methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':

        name = request.form['username']
        passw = request.form['pass']
        msg = registrar(name, passw)

        return msg


def buscarPeliculaPorId(idPelicula):
    idPelicula = str(idPelicula)

    x = requests.get('https://api.themoviedb.org/3/movie/'+idPelicula+'?api_key=6427e11274426be9030b97aab51ef6f8&language=en-US')
    p = x.json()
    return p


@app.route('/coleccion',methods=['GET', 'POST'])
def coleccion():
    mensaje = ""
    if request.method == 'POST':
        global idUsuarioLogeado
        if idUsuarioLogeado is None:

            return "-1"
        else:
            pelicula = request.get_json()

            mensaje = agregar_a_coleccion(
                idUsuarioLogeado, pelicula['idPelicula'], pelicula['categoria'], pelicula['titulo'], pelicula['rating']
            )

            return "1"
    return ""



@app.route('/validarRegistro',methods=['GET', 'POST'])
def validarRegistro():
    if request.method == 'POST':
        name = request.form['usuario']
        passw = request.form['contraseña']

        global user
        global idUsuarioLogeado

        error = None
        usuario = buscar_usuario(name,passw)
        if usuario is not None:
            user = usuario[1]
            idUsuarioLogeado = usuario[0]
        return user


@app.route('/cerrarSesion',methods=['GET', 'POST'])
def cerrarSesion():
    if request.method == 'POST':
        global user
        user = ""
        return user

@app.route('/userHome' , methods=['GET', 'POST'])
def userHome():
    global idUsuarioLogeado
    if idUsuarioLogeado is None:
        return render_template('error.html',error="Acceso denegado")
    else:

        coleccion = listarColeccion(idUsuarioLogeado)

        categorias = obtener_categorias()

        return render_template('user.html',coleccion = coleccion, categorias =categorias )



@app.route('/listarCategorias' , methods=['GET', 'POST'])
def listarCategorias():
    categorias = obtener_categorias()
    return jsonify(categorias)

@app.route('/pelisaborrar' , methods=['GET', 'POST'])
def pelisaborrar():
    if request.method == 'POST':
        global idUsuarioLogeado
        peliculas = request.get_json()
        for p in peliculas:
            borrar_pelicula_en_coleccion(idUsuarioLogeado,p['_id'])


    return jsonify(peliculas)

if __name__ == "__main__":
    app.run(debug=True)

