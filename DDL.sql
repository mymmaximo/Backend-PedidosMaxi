-- CREATE

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

create table estados_pedido (
	id serial4 not null,
	estatus varchar(50) not null,
	constraint estados_pedido_estatus_key unique (estatus),
	constraint estados_pedido_pkey primary key (id)
);

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

create table roles (
	id serial4 not null,
	rol varchar(50) not null,
	descripcion varchar(100) null,
	constraint roles_pkey primary key (id),
	constraint roles_rol_key unique (rol)
);

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

create table historial_precios (
	id serial4 not null,
	id_producto int4 null,
	precio_viejo numeric(10, 2) not null,
	precio_nuevo numeric(10, 2) not null,
	updated_at timestamp null,
	constraint historial_precios_pkey primary key (id),
	constraint historial_precios_id_producto_fkey foreign key (id_producto) references productos(id)
);

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

create table usuarios (
	id serial4 not null,
	nombre varchar(100) not null,
	email varchar(150) not null,
	dni varchar(20) not null,
	contrasena varchar(255) null,
	id_rol int4 null,
	activo bool null,
	created_at timestamp default current_timestamp null,
	updated_at timestamp default current_timestamp null,
	constraint usuarios_dni_key unique (dni),
	constraint usuarios_email_key unique (email),
	constraint usuarios_pkey primary key (id),
	constraint fk_usuarios_rol foreign key (id_rol) references roles(id)
);

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

-- DROP

drop table banner;

drop table clientes;

drop table direcciones;

drop table estados_pedido;

drop table productos;

drop table roles;

drop table archivos;

drop table historial_precios;

drop table pedidos;

drop table usuarios;

drop table detalles_pedido;

--ALTER

alter table clientes  add column activo boolean;

alter table pedidos
	add constraint fk_estatus_id
	foreign key (estatus)
	references estados_pedido (id);

alter table pedidos (
	id serial4 not null,
	id_usuted_at timestamp default current_timestamp null,
	estatus int4 null,
	constraint pedidos_pkey primary key (id),
	constraint fk_estatus_id foreign key (estatus) references estados_pedido(id),
	constraint pedidos_id_usuario_fkey foreign key (id_usuario) references usuarios(id),
	constraint pedidos_id_direccion_fkey foreign key (id_direccion) references direcciones(id)
);

alter table roles
	add column descripcion varchar(100);

--INSERT

insert into estados_pedido (estatus) values ('');

--TRIGGER

create trigger restar_stock_despues_de_venta after
	insert on detalles_pedido 
	for each row execute function actualizar_stock_auto();

create trigger save_precio before
	insert or update on productos 
	for each row execute function validar_precio();

create trigger almacenar_precios_trigger before
	update on productos 
	for each row execute function almacenar_precios();