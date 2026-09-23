-- public.banner definition

-- Drop table

-- DROP TABLE banner;

CREATE TABLE banner (
	id serial4 NOT NULL,
	s3_key varchar(255) NOT NULL,
	nombre_original varchar(255) NOT NULL,
	tipo_contenido varchar(50) NOT NULL,
	tamanio int4 NOT NULL,
	activo bool DEFAULT true NULL,
	enlace varchar(255) NOT NULL,
	orden int4 NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT banner_pkey PRIMARY KEY (id)
);


-- public.clientes definition

-- Drop table

-- DROP TABLE clientes;

CREATE TABLE clientes (
	id serial4 NOT NULL,
	nombre varchar(100) NOT NULL,
	email varchar(150) NOT NULL,
	dni varchar(20) NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	contrasena varchar(255) NULL,
	activo bool NULL,
	CONSTRAINT clientes_dni_key UNIQUE (dni),
	CONSTRAINT clientes_email_key UNIQUE (email),
	CONSTRAINT clientes_pkey PRIMARY KEY (id)
);


-- public.direcciones definition

-- Drop table

-- DROP TABLE direcciones;

CREATE TABLE direcciones (
	id serial4 NOT NULL,
	calle varchar(150) NOT NULL,
	numero int4 NOT NULL,
	barrio varchar(100) NOT NULL,
	ciudad varchar(100) NOT NULL,
	provincia varchar(100) NOT NULL,
	activo bool NULL,
	CONSTRAINT direcciones_pkey PRIMARY KEY (id)
);


-- public.estados_pedido definition

-- Drop table

-- DROP TABLE estados_pedido;

CREATE TABLE estados_pedido (
	id serial4 NOT NULL,
	estatus varchar(50) NOT NULL,
	CONSTRAINT estados_pedido_estatus_key UNIQUE (estatus),
	CONSTRAINT estados_pedido_pkey PRIMARY KEY (id)
);


-- public.productos definition

-- Drop table

-- DROP TABLE productos;

CREATE TABLE productos (
	id serial4 NOT NULL,
	nombre varchar(100) NOT NULL,
	precio numeric(10, 2) NOT NULL,
	stock int4 DEFAULT 0 NULL,
	categoria varchar(50) NULL,
	codigo_barra varchar(50) NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	activo bool NULL,
	CONSTRAINT productos_codigo_barra_key UNIQUE (codigo_barra),
	CONSTRAINT productos_pkey PRIMARY KEY (id)
);


-- public.roles definition

-- Drop table

-- DROP TABLE roles;

CREATE TABLE roles (
	id serial4 NOT NULL,
	rol varchar(50) NOT NULL,
	descripcion varchar(100) NULL,
	CONSTRAINT roles_pkey PRIMARY KEY (id),
	CONSTRAINT roles_rol_key UNIQUE (rol)
);


-- public.usuarios definition

-- Drop table

-- DROP TABLE usuarios;

CREATE TABLE usuarios (
	id serial4 NOT NULL,
	nombre varchar(100) NOT NULL,
	email varchar(150) NOT NULL,
	dni varchar(20) NOT NULL,
	contrasena varchar(255) NULL,
	activo bool NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT usuarios_dni_key UNIQUE (dni),
	CONSTRAINT usuarios_email_key UNIQUE (email),
	CONSTRAINT usuarios_pkey PRIMARY KEY (id)
);


-- public.archivos definition

-- Drop table

-- DROP TABLE archivos;

CREATE TABLE archivos (
	id serial4 NOT NULL,
	id_producto int4 NOT NULL,
	s3_key varchar(255) NOT NULL,
	nombre_original varchar(255) NOT NULL,
	tipo_contenido varchar(50) NOT NULL,
	tamanio int4 NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT archivos_pkey PRIMARY KEY (id),
	CONSTRAINT fk_producto FOREIGN KEY (id_producto) REFERENCES productos(id) ON DELETE CASCADE
);


-- public.favoritos definition

-- Drop table

-- DROP TABLE favoritos;

CREATE TABLE favoritos (
	id serial4 NOT NULL,
	id_cliente int4 NOT NULL,
	id_producto int4 NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT favoritos_id_cliente_id_producto_key UNIQUE (id_cliente,id_producto),
	CONSTRAINT favoritos_pkey PRIMARY KEY (id),
	CONSTRAINT favoritos_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES clientes(id) ON DELETE CASCADE,
	CONSTRAINT favoritos_id_producto_fkey FOREIGN KEY (id_producto) REFERENCES productos(id) ON DELETE CASCADE
);


-- public.pedidos definition

-- Drop table

-- DROP TABLE pedidos;

CREATE TABLE pedidos (
	id serial4 NOT NULL,
	id_cliente int4 NOT NULL,
	id_direccion int4 NOT NULL,
	transaccion_id varchar(100) NULL,
	url_recibo text NULL,
	detalle_pago varchar(100) NULL,
	metodo_pago varchar(50) NULL,
	monto_pagado numeric(10, 2) NULL,
	tiempo_entrega int2 NULL,
	tiempo_estimado_entrega int2 NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	estatus int4 NULL,
	CONSTRAINT pedidos_pkey PRIMARY KEY (id),
	CONSTRAINT fk_estatus_id FOREIGN KEY (estatus) REFERENCES estados_pedido(id),
	CONSTRAINT pedidos_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES clientes(id),
	CONSTRAINT pedidos_id_direccion_fkey FOREIGN KEY (id_direccion) REFERENCES direcciones(id)
);


-- public.registro_precios definition

-- Drop table

-- DROP TABLE registro_precios;

CREATE TABLE registro_precios (
	id int4 DEFAULT nextval('promociones_id_seq'::regclass) NOT NULL,
	id_producto int4 NOT NULL,
	motivo varchar(100) NULL,
	precio_nuevo numeric(10, 2) NOT NULL,
	fecha_inicio timestamptz NOT NULL,
	fecha_fin timestamptz NOT NULL,
	created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
	precio_anterior numeric(10, 2) NULL,
	porcentaje_descuento int4 NULL,
	es_promocion bool DEFAULT true NULL,
	activa bool DEFAULT true NULL,
	CONSTRAINT promociones_pkey PRIMARY KEY (id),
	CONSTRAINT promociones_id_producto_fkey FOREIGN KEY (id_producto) REFERENCES productos(id) ON DELETE CASCADE
);


-- public.usuarios_roles definition

-- Drop table

-- DROP TABLE usuarios_roles;

CREATE TABLE usuarios_roles (
	id_usuario int4 NOT NULL,
	id_rol int4 NOT NULL,
	CONSTRAINT usuarios_roles_pkey PRIMARY KEY (id_usuario,id_rol),
	CONSTRAINT fk_ur_rol FOREIGN KEY (id_rol) REFERENCES roles(id) ON DELETE CASCADE,
	CONSTRAINT fk_ur_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
);


-- public.detalles_pedido definition

-- Drop table

-- DROP TABLE detalles_pedido;

CREATE TABLE detalles_pedido (
	id serial4 NOT NULL,
	id_pedido int4 NOT NULL,
	id_producto int4 NOT NULL,
	cantidad int4 NOT NULL,
	precio_unitario numeric(10, 2) NOT NULL,
	CONSTRAINT detalles_pedido_pkey PRIMARY KEY (id),
	CONSTRAINT fk_detalles_pedido FOREIGN KEY (id_pedido) REFERENCES pedidos(id) ON DELETE CASCADE,
	CONSTRAINT fk_detalles_producto FOREIGN KEY (id_producto) REFERENCES productos(id) ON DELETE RESTRICT
);