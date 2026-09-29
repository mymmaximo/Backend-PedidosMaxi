-- Tabla. {Banners de la Pagina Principal}
create table banner (
	id serial4 not null,
	s3_key varchar(255) not null,
	nombre_original varchar(255) not null,
	tipo_contenido varchar(50) not null,
	tamanio int4 not null,
	activo bool default true null,
	enlace varchar(255) not null,
	orden int4 null,
	created_at timestamp default current_timestamp null,
	constraint banner_pkey primary key (id)
);

-- Tabla. {Clientes Registrados}
create table clientes (
	id serial4 not null,
	nombre varchar(100) not null,
	email varchar(150) not null,
	dni varchar(20) not null,
	created_at timestamp default current_timestamp null,
	updated_at timestamp default current_timestamp null,
	contrasena varchar(255) null,
	activo bool null,
	constraint clientes_dni_key unique (dni),
	constraint clientes_email_key unique (email),
	constraint clientes_pkey primary key (id)
);

-- Tabla. {Direcciones de los Pedidos de los Clientes}
create table direcciones (
	id serial4 not null,
	calle varchar(150) not null,
	numero int4 not null,
	barrio varchar(100) not null,
	ciudad varchar(100) not null,
	provincia varchar(100) not null,
	activo bool null,
	constraint direcciones_pkey primary key (id)
);

-- Tabla. {Estatus de la Entrega del Pedido}
create table estados_pedido (
	id serial4 not null,
	estatus varchar(50) not null,
	constraint estados_pedido_estatus_key unique (estatus),
	constraint estados_pedido_pkey primary key (id)
);

-- Tabla. {Productos}
create table productos (
	id serial4 not null,
	nombre varchar(100) not null,
	precio numeric(10, 2) not null,
	stock int4 default 0 null,
	categoria varchar(50) null,
	codigo_barra varchar(50) not null,
	created_at timestamp default current_timestamp null,
	updated_at timestamp default current_timestamp null,
	activo bool null,
	constraint productos_codigo_barra_key unique (codigo_barra),
	constraint productos_pkey primary key (id)
);

-- Tabla. {Roles y su Descripcion}
create table roles (
	id serial4 not null,
	rol varchar(50) not null,
	descripcion varchar(100) null,
	constraint roles_pkey primary key (id),
	constraint roles_rol_key unique (rol)
);

-- Tabla. {Usuarios con Permisos}
create table usuarios (
	id serial4 not null,
	nombre varchar(100) not null,
	email varchar(150) not null,
	dni varchar(20) not null,
	contrasena varchar(255) null,
	activo bool null,
	created_at timestamp default current_timestamp null,
	updated_at timestamp default current_timestamp null,
	constraint usuarios_dni_key unique (dni),
	constraint usuarios_email_key unique (email),
	constraint usuarios_pkey primary key (id)
);

-- Tabla. {Archivos (Imagenes)}
create table archivos (
	id serial4 not null,
	id_producto int4 not null,
	s3_key varchar(255) not null,
	nombre_original varchar(255) not null,
	tipo_contenido varchar(50) not null,
	tamanio int4 not null,
	created_at timestamp default current_timestamp null,
	constraint archivos_pkey primary key (id),
	constraint fk_producto foreign key (id_producto) references productos(id) on delete cascade
);

-- Tabla. {Productos Favoritos de los Clientes}
create table favoritos (
	id serial4 not null,
	id_cliente int4 not null,
	id_producto int4 not null,
	created_at timestamp default current_timestamp null,
	constraint favoritos_id_cliente_id_producto_key unique (id_cliente,id_producto),
	constraint favoritos_pkey primary key (id),
	constraint favoritos_id_cliente_fkey foreign key (id_cliente) references clientes(id) on delete cascade,
	constraint favoritos_id_producto_fkey foreign key (id_producto) references productos(id) on delete cascade
);

-- Tabla. {Pedidos}
create table pedidos (
	id serial4 not null,
	id_cliente int4 not null,
	id_direccion int4 not null,
	transaccion_id varchar(100) null,
	url_recibo text null,
	detalle_pago varchar(100) null,
	metodo_pago varchar(50) null,
	monto_pagado numeric(10, 2) null,
	tiempo_entrega int2 null,
	tiempo_estimado_entrega int2 not null,
	created_at timestamp default current_timestamp null,
	updated_at timestamp default current_timestamp null,
	estatus int4 null,
	constraint pedidos_pkey primary key (id),
	constraint fk_estatus_id foreign key (estatus) references estados_pedido(id),
	constraint pedidos_id_cliente_fkey foreign key (id_cliente) references clientes(id),
	constraint pedidos_id_direccion_fkey foreign key (id_direccion) references direcciones(id)
);

-- Tabla. {Registros de Precios: Historial de Cambios Fijos y Promociones}
create table registro_precios (
	id int4 default nextval('promociones_id_seq'::regclass) not null,
	id_producto int4 not null,
	motivo varchar(100) null,
	precio_nuevo numeric(10, 2) not null,
	fecha_inicio timestamptz not null,
	fecha_fin timestamptz not null,
	created_at timestamptz default current_timestamp null,
	precio_anterior numeric(10, 2) null,
	porcentaje_descuento int4 null,
	es_promocion bool default true null,
	activa bool default true null,
	constraint promociones_pkey primary key (id),
	constraint promociones_id_producto_fkey foreign key (id_producto) references productos(id) on delete cascade
);

-- Tabla. {Usuarios y Sus Multiples Roles (Conexion)}
create table usuarios_roles (
	id_usuario int4 not null,
	id_rol int4 not null,
	constraint usuarios_roles_pkey primary key (id_usuario,id_rol),
	constraint fk_ur_rol foreign key (id_rol) references roles(id) on delete cascade,
	constraint fk_ur_usuario foreign key (id_usuario) references usuarios(id) on delete cascade
);

-- Tabla. {Detalles de los Productos en los Pedidos}
create table detalles_pedido (
	id serial4 not null,
	id_pedido int4 not null,
	id_producto int4 not null,
	cantidad int4 not null,
	precio_unitario numeric(10, 2) not null,
	constraint detalles_pedido_pkey primary key (id),
	constraint fk_detalles_pedido foreign key (id_pedido) references pedidos(id) on delete cascade,
	constraint fk_detalles_producto foreign key (id_producto) references productos(id) on delete restrict
);

-- Trigger. {Restar Stock de Producto Comprado}
create trigger restar_stock_despues_de_venta after
	insert
		on
		public.detalles_pedido for each row execute function actualizar_stock_auto();

#Borrar Tablas de Base de Datos

drop table banner;

drop table clientes;

drop table direcciones;

drop table estados_pedido;

drop table productos;

drop table roles;

drop table usuarios;

drop table archivos;

drop table favoritos;

drop table pedidos;

drop table registro_precios;

drop table usuarios_roles;

drop table detalles_pedido;
