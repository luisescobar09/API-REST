DROP TABLE IF EXISTS clientes;

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL
);

INSERT INTO clientes (nombre, email) VALUES ('Evelyn Jimenez','evelyn@gmail.com');
INSERT INTO clientes (nombre, email) VALUES ('Marco Polo Cruz','marco@gmail.com');
INSERT INTO clientes (nombre, email) VALUES ('José Luis Escobar','luis@gmail.com');

.headers ON

SELECT * FROM clientes;