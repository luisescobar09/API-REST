DROP TABLE IF EXISTS clientes;

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL
);

INSERT INTO clientes (nombre, email) VALUES ('Evelyn Jimenez','evelyn@gmail.com');
INSERT INTO clientes (nombre, email) VALUES ('Marco Polo Cruz','marco@gmail.com');
INSERT INTO clientes (nombre, email) VALUES ('José Luis Escobar','luis@gmail.com');

DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios(
    username TEXT,
    password varchar(32),
    level INTEGER
);

CREATE UNIQUE INDEX index_usuario ON usuarios(username);

INSERT INTO usuarios(username, password, level) VALUES('admin','21232f297a57a5a743894a0e4a801fc3',0);
INSERT INTO usuarios(username, password, level) VALUES('user','ee11cbb19052e40b07aac0ca060c23ee',1);

SELECT * FROM usuarios;

.headers ON

SELECT * FROM clientes;