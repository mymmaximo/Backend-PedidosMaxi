-- public.clientes definition

-- Drop table

-- DROP TABLE clientes;

CREATE TABLE clientes (
	id serial4 NOT NULL,
	nombre varchar(100) NOT NULL,
	email varchar(150) NOT NULL,
	dni varchar(20) NOT NULL,
	apellido varchar(100) NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	usuario varchar(50) NULL,
	contrasena varchar(255) NULL,
	CONSTRAINT clientes_dni_key UNIQUE (dni),
	CONSTRAINT clientes_email_key UNIQUE (email),
	CONSTRAINT clientes_pkey PRIMARY KEY (id)
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
	CONSTRAINT productos_codigo_barra_key UNIQUE (codigo_barra),
	CONSTRAINT productos_pkey PRIMARY KEY (id)
);

-- Table Triggers

create trigger save_precio before
insert
    or
update
    on
    public.productos for each row execute function validar_precio();
create trigger almacenar_precios_trigger before
update
    on
    public.productos for each row execute function almacenar_precios();


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
	id_cliente int4 NOT NULL,
	CONSTRAINT direcciones_pkey PRIMARY KEY (id),
	CONSTRAINT fk_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id) ON DELETE CASCADE
);


-- public.historial_precios definition

-- Drop table

-- DROP TABLE historial_precios;

CREATE TABLE historial_precios (
	id serial4 NOT NULL,
	id_producto int4 NULL,
	precio_viejo numeric(10, 2) NOT NULL,
	precio_nuevo numeric(10, 2) NOT NULL,
	updated_at timestamp NULL,
	CONSTRAINT historial_precios_pkey PRIMARY KEY (id),
	CONSTRAINT historial_precios_id_producto_fkey FOREIGN KEY (id_producto) REFERENCES productos(id)
);


-- public.pedidos definition

-- Drop table

-- DROP TABLE pedidos;

CREATE TABLE pedidos (
	id serial4 NOT NULL,
	id_cliente int4 NOT NULL,
	id_direccion int4 NOT NULL,
	metodo_pago varchar(50) NOT NULL,
	tiempo_entrega int2 NULL,
	tiempo_estimado_entrega int2 NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	updated_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT pedidos_pkey PRIMARY KEY (id),
	CONSTRAINT pedidos_id_cliente_fkey FOREIGN KEY (id_cliente) REFERENCES clientes(id),
	CONSTRAINT pedidos_id_direccion_fkey FOREIGN KEY (id_direccion) REFERENCES direcciones(id)
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