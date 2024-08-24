-- Borra la base de datos si existe


DROP DATABASE IF EXISTS vinoVerse;

------------------------------------------
|-- ¡¡¡¡     OJO CON ESTE COMANDO    !!!!|
------------------------------------------



-- Crea la base de datos
CREATE DATABASE vinoVerse;
USE vinoVerse;

-- Tabla bodegas
CREATE TABLE bodegas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    ubicacion VARCHAR(100),
    descripcion TEXT
);

-- Tabla vinos
CREATE TABLE vinos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    bodega_id INT,
    tipo_vino VARCHAR(50),
    año INT,
    FOREIGN KEY (bodega_id) REFERENCES bodegas(id)
);

-- Tabla usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    contraseña VARCHAR(255),
    fecha_registro DATE
);

-- Tabla perfiles
CREATE TABLE perfiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    foto_perfil VARCHAR(255),
    biografia TEXT,
    ubicacion VARCHAR(100),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla publicaciones
CREATE TABLE publicaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    tipo_publicacion VARCHAR(50),
    titulo VARCHAR(100),
    contenido TEXT,
    fecha_publicacion DATETIME,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla reseñas_vinos
CREATE TABLE reseñas_vinos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    publicacion_id INT,
    vino_id INT,
    puntuacion INT,
    FOREIGN KEY (publicacion_id) REFERENCES publicaciones(id),
    FOREIGN KEY (vino_id) REFERENCES vinos(id)
);

-- Tabla fotos_videos
CREATE TABLE fotos_videos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    publicacion_id INT,
    url VARCHAR(255),
    FOREIGN KEY (publicacion_id) REFERENCES publicaciones(id)
);

-- Tabla experiencias
CREATE TABLE experiencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    publicacion_id INT,
    tipo_experiencia VARCHAR(50),
    ubicacion VARCHAR(100),
    fecha_inicio DATETIME,
    fecha_fin DATETIME,
    FOREIGN KEY (publicacion_id) REFERENCES publicaciones(id)
);

-- Tabla eventos
CREATE TABLE eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    ubicacion VARCHAR(100),
    fecha_evento DATETIME,
    descripcion TEXT
);

-- Tabla empresas_transporte
CREATE TABLE empresas_transporte (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    contacto VARCHAR(100)
);

-- Tabla hoteles
CREATE TABLE hoteles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    ubicacion VARCHAR(100),
    contacto VARCHAR(100)
);

-- Tabla paquetes_turisticos
CREATE TABLE paquetes_turisticos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    precio DECIMAL(10, 2),
    transporte_id INT,
    hotel_id INT,
    bodega_id INT,
    FOREIGN KEY (transporte_id) REFERENCES empresas_transporte(id),
    FOREIGN KEY (hotel_id) REFERENCES hoteles(id),
    FOREIGN KEY (bodega_id) REFERENCES bodegas(id)
);
