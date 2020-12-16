

CREATE TABLE IF not EXISTS Usuarios(
    id integer PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)

CREATE TABLE IF not EXISTS Coleccion(
    id integer PRIMARY KEY AUTOINCREMENT,
    idUsuario integer not null,
    idPelicula integer not null
)