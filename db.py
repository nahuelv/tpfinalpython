import sqlite3
from datetime import date

def conexion ():
    db = sqlite3.connect('C:\\Users\\Nahuel\\Desktop\\Web Peliculas\\pydb.db')
    return db

def crear_tabla():

    con = conexion()
    c = con.cursor()

    c.execute("""CREATE TABLE IF not EXISTS Usuarios(
    id integer PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
    );""")

    c.execute("""CREATE TABLE IF not EXISTS Coleccion(
    id integer PRIMARY KEY AUTOINCREMENT,
    idUsuario integer not null,
    idPelicula integer not null,
    idCategoria integer not null,
    nombre TEXT NOT NULL,
    puntuacion INTEGER NOT NULL,
    fecha datetime not null
    
);""")

    c.execute("""CREATE TABLE IF not EXISTS Categorias(
        idCategoria integer PRIMARY KEY AUTOINCREMENT,        
        nombre TEXT NOT NULL        
    );""")
    c.close()
    con.commit()
    con.close()


crear_tabla()

def obtener_categorias ():
    con = conexion()
    c = con.cursor()

    query = "SELECT * FROM Categorias"
    result = c.execute(query)

    rows = c.fetchall()
    c.close()
    con.commit()
    con.close()
    return rows

def buscar_usuario(name,passw):
    con = conexion()
    c = con.cursor()
    row = c.execute(
        'SELECT * FROM Usuarios WHERE username = ? and password = ?', (name, passw)
    ).fetchone()

    return row

def alta_usuario(name,passw):
    con = conexion()
    c = con.cursor()
    query = "INSERT INTO Usuarios (username, password) VALUES (?,?)"
    datos = (name, passw)
    c.execute(query, datos)

def buscarPersona(name):
    con = conexion()
    c = con.cursor()

    query = "SELECT * FROM Usuarios WHERE username = ?"
    result = c.execute(query, (name,))

    rows = c.fetchone()
    c.close()
    con.commit()
    con.close()
    return False if not rows else True

def listarColeccion (idUsuarioLogeado):
    con = conexion()
    c = con.cursor()
    query = "SELECT co.id,co.nombre as Pelicula,co.puntuacion,co.fecha, ca.nombre as Categoria, co.idPelicula FROM Coleccion co inner join Categorias ca on ca.idCategoria = co.idCategoria WHERE idUsuario = ?"

    result = c.execute(query, (idUsuarioLogeado,))

    rows = c.fetchall()
    c.close()
    con.commit()
    con.close()
    return rows

def agregar_a_coleccion (idUsuarioLogeado,idPelicula,categoria,titulo,rating):
    con = conexion()
    c = con.cursor()
    query = "INSERT INTO Coleccion (idUsuario, idPelicula,idCategoria,nombre,puntuacion,fecha) VALUES (?,?,?,?,?,?)"
    datos = (idUsuarioLogeado, idPelicula, categoria, titulo, rating,
             date.today())
    c.execute(query, datos)
    c.close()
    con.commit()
    con.close()
    return ""

def borrar_pelicula_en_coleccion(idUsuario,idPelicula):
    con = conexion()
    c = con.cursor()
    query = "DELETE  FROM Coleccion WHERE idUsuario = ? AND idPelicula = ?"
    datos = (idUsuario, idPelicula)
    c.execute(query, datos)
    c.close()
    con.commit()
    con.close()
    return ""