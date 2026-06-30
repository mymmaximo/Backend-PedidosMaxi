--PROCEDURE

create or replace procedure actualizar_stock (
	in p_id_producto integer, 
	in p_cantidad integer
)
	language plpgsql
	as $$
		declare
			v_stock_actual int;
		begin
		select p.stock 
		into v_stock_actual 
		from productos p
		where p.id = p_id_producto;
		if (v_stock_actual + p_cantidad) >= 0 then
			update productos
		    	set stock = v_stock_actual + p_cantidad
		    where id = p_id_producto;
		else
			raise notice 'stock insuficiente';
		end if;
		end;
	$$
;

-- CREATE

create or replace function actualizar_stock_auto ()
	returns trigger
	language plpgsql
	as $$
		begin
			update productos
				set stock = stock - new.cantidad
				where id = new.id_producto;
			return new;
		end;
	$$
;

create or replace function almacenar_precios ()
	returns trigger
	language plpgsql
	as $$
		begin
			if new.precio <> old.precio then
				insert into historial_precios (
					id_producto,
					precio_viejo,
					precio_nuevo,
					updated_at
				) 
				values (
					new.id,
					old.precio,
					new.precio,
					current_timestamp
				);
			end if;
			return new;
		end;
	$$
;

create or replace function caja_rejistradora (
	v_codigo_barra character varying,
	v_cantidad integer, 
	v_id_pedido integer
)
	returns table (
		recibo_producto character varying, 
		recibo_cantidad integer, 
		recibo_precio integer, 
		recibo_subtotal integer
	)
	language plpgsql
	as $$
		declare 
			v_id_producto int;
			v_precio_unitario int;
			v_nombre_producto varchar;
			v_stock_actual int;
		begin
			select 
				p.id, 
				p.precio, 
				p.nombre, 
				p.stock
			into 
				v_id_producto, 
				v_precio_unitario, 
				v_nombre_producto, 
				v_stock_actual 
			from productos p
			where p.codigo_barra = v_codigo_barra;
			if (v_stock_actual + v_cantidad) >= 0 then
				insert into detalles_pedido (
					id_pedido, 
					id_producto, 
					cantidad, 
					precio_unitario
				)
				values (
					v_id_pedido, 
					v_id_producto, 
					v_cantidad, 
					v_precio_unitario
				);
				update productos p
					set stock = stock - v_cantidad
					where p.codigo_barra = v_codigo_barra;
			else
				raise notice 'stock insuficiente';
			end if;
			return query
				select 
					v_nombre_producto, 
					v_cantidad, 
					v_precio_unitario, 
					(v_cantidad * v_precio_unitario);
		end;
	$$
;

create or replace function caja_rejistradora (
	p_codigo_barra character varying, 
	caja_cantidad integer
)
	returns table (
		dp_id_pedido integer, 
		dp_id_producto integer, 
		dp_cantidad integer, 
		dp_precio_unitario integer
	)
	language plpgsql
	as $$
		begin
			select 
				dp.id_pedido, 
				dp.id_producto, 
				dp.cantidad = dp_cantidad, 
				dp.precio_unitario
			from detalles_pedidos
			join productos on dp.id_producto = p.id
			where p.codigo_barra = p_codigo_barra;
		end;
	$$
;

create or replace function caja_rejistradora_2 (
	v_codigo_barra character varying, 
	v_cantidad integer, 
	v_id_pedido integer
)
	returns table (
		recibo_producto character varying, 
		recibo_cantidad integer, 
		recibo_precio integer, 
		recibo_subtotal integer
	)
	language plpgsql
	as $$
		declare 
			v_id_producto int;
			v_precio_unitario int;
			v_nombre_producto varchar;
			v_stock_actual int;
		begin
			select 
				p.id, 
				p.precio, 
				p.nombre, 
				p.stock
			into 
				v_id_producto, 
				v_precio_unitario, 
				v_nombre_producto, 
				v_stock_actual 
			from productos p
			where p.codigo_barra = v_codigo_barra;
			if v_id_producto is null then
				raise exception '¡Producto Inexistente! Revisa el codigo de barras';
			end if;
			if (v_stock_actual - v_cantidad) >= 0 then
				insert into detalles_pedido (
					id_pedido, 
					id_producto, 
					cantidad, 
					precio_unitario
				)
				values (
					v_id_pedido, 
					v_id_producto, 
					v_cantidad, 
					v_precio_unitario
				);
				update productos p
					set stock = stock - v_cantidad
					where p.codigo_barra = v_codigo_barra;
			else
				raise exception 'stock insuficiente!! solo quedan % unidades', v_stock_actual;
			end if;
			return query
			select 
				v_nombre_producto, 
				v_cantidad, 
				v_precio_unitario, 
				(v_cantidad * v_precio_unitario);
		end;
	$$
;

create or replace function consultar_stock (
	codigo_barra integer
)
	returns table (
		p_stock integer
	)
	language plpgsql
	as $$
		begin
			return query
			select p.stock
			from productos p
			where p.id = p.codigo_barra;
		end;
	$$
;

create or replace function consultar_stock (
	p_codigo_barra character varying
)
	returns table (
		p_stock integer
	)
	language plpgsql
	as $$
		begin
			return query
			select p.stock 
			from productos p
			where p.codigo_barra = p_codigo_barra;
		end;
	$$
;

create or replace function fn_obtener_ticket_pedido (
	p_id_pedido integer, 
	p_dias_reales integer
)
	returns void
	language plpgsql
	as $$
		declare p_tiempo_estimado_entrega int2;
		begin
			update pedidos
				set tiempo_entrega = p_dias_reales
				where id = p_id_pedido
				returning tiempo_estimado_entrega 
				into p_tiempo_estimado_entrega;
			if p_dias_reales > p_tiempo_estimado_entrega then
				raise notice 'El pedido no llego en el tiempo estimado';
			end if;
		end;
	$$
;

create or replace function fn_obtener_ticket_pedido (
	p_id_pedido integer
)
	returns table (
		p_nombre character varying, 
		dp_cantidad integer, 
		dp_precio_unitario numeric, 
		dp_subtotal numeric
	)
	language plpgsql
	as $$
		begin
			return query
			select 
				p.nombre, 
				dp.cantidad, 
				dp.precio_unitario, 
				sum(dp.cantidad * dp.precio_unitario) as dp_subtotal
			from detalles_pedido dp
			join productos p on p.id = dp.id_producto
			where dp.id_pedido = p_id_pedido
			group by 
				p.nombre, 
				dp.cantidad, 
				dp.precio_unitario;
		end;
	$$
;

create or replace function fn_obtener_ticket_pedido (
	p_id_pedido integer, 
	p_dias_reales smallint
)
	returns void
	language plpgsql
	as $$
		begin
			update pedidos
				set p.tiempo_entrega = p_dias_reales
				where p.id = p_id_pedido;
			if p.tiempo_entrega > p.tiempo_estimado_entrega then
				raise notice 'El pedido no llego en el tiempo estimado';
			end if;
		end;
	$$
;

create or replace function get_all_clientes ()
	returns table (
		id_cliente integer, 
		nombre character varying, 
		email character varying, 
		dni character varying, 
		activo boolean, 
		created_at timestamp without time zone, 
			id_direccion integer, 
			calle character varying, 
			numero integer, 
			barrio character varying, 
			ciudad character varying, 
			provincia character varying
	)
	language plpgsql
	as $$
		begin
			return query
			select
				c.id,
				c.nombre,
				c.email,
				c.dni,
				c.activo,
				c.created_at,
					d.id,
					d.calle,
					d.numero,
					d.barrio,
					d.ciudad,
					d.provincia
			from clientes c
			left join pedidos p on c.id = p.id_cliente
			left join direcciones d on p.id_direccion = d.id;
		end;
	$$
;

create or replace function get_all_historial ()
	returns table (
		id integer, 
		id_producto integer, 
		precio_viejo numeric, 
		precio_nuevo numeric, 
		updated_at timestamp without time zone, 
			nombre character varying, 
			categoria character varying, 
			codigo_barra character varying, 
			activo boolean
	)
	language plpgsql
	as $$
		begin
			return query
			select
				hp.id, 
				hp.id_producto, 
				hp.precio_viejo, 
				hp.precio_nuevo, 
				hp.updated_at,
					p.nombre,
					p.categoria, 
					p.codigo_barra,
					p.activo
			from historial_precios hp
			join productos p on hp.id_producto = p.id;
		end;
	$$
;

create or replace function get_all_productos ()
	returns table (
		id integer, 
		nombre character varying, 
		precio numeric, 
		stock integer, 
		categoria character varying, 
		codigo_barra character varying, 
		created_at timestamp without time zone, 
		updated_at timestamp without time zone, 
		activo boolean, 
			id_imagen integer, 
			s3_key character varying, 
			tipo_contenido character varying, 
			tamanio integer
	)
	language plpgsql
	as $$
		begin
			return query
			select
				p.id,
				p.nombre,
				p.precio,
				p.stock,
				p.categoria,
				p.codigo_barra,
				p.created_at,
				p.updated_at,
				p.activo,
					a.id,
					a.s3_key,
					a.tipo_contenido,
					a.tamanio
			from productos p
			left join archivos a on p.id = a.id_producto
			order by stock desc;
		end;
	$$
;

create or replace function get_all_usuarios ()
	returns table (
		id_usuario integer, 
		nombre character varying, 
		email character varying, 
		dni character varying, 
		id_rol integer, 
		activo boolean, 
		created_at timestamp without time zone
	)
	language plpgsql
	as $$
		begin
			return query
			select
				u.id,
				u.nombre,
				u.email,
				u.dni,
				u.id_rol,
				u.activo,
				u.created_at
			from usuarios u;
		end;
	$$
;

create or replace function get_direcciones (
	p_id_cliente integer
)
	returns setof direcciones
	language plpgsql
	as $$
		begin
			return query
			select d.* 
			from direcciones d
			join pedidos p on d.id = p.id_direccion 
			where p.id_cliente = p_id_cliente;
		end;
	$$
;

create or replace function get_only_clientes ()
	returns table (
		id_cliente integer, 
			id_direccion integer, 
			calle character varying, 
			numero integer, 
			barrio character varying, 
			ciudad character varying, 
			provincia character varying
	)
	language plpgsql
	as $$
		begin
			return query
			select
				c.id,
					d.id,
					d.calle,
					d.numero,
					d.barrio,
					d.ciudad,
					d.provincia
			from clientes c
			left join pedidos p on c.id = p.id_cliente
			left join direcciones d on p.id_direccion = d.id;
		end;
	$$
;

create or replace function obtener_all_pedidos()
	returns table (
		id_pedido integer, 
		id_cliente integer, 
			nombre_cliente character varying, 
		id_direccion integer, 
			calle character varying, 
			numero integer, 
			ciudad character varying, 
			provincia character varying, 
		metodo_pago character varying, 
		estatus integer, 
		tiempo_estimado_entrega smallint, 
		tiempo_entrega smallint, 
		created_at timestamp without time zone, 
		updated_at timestamp without time zone, 
		total numeric, 
			id_detalles_pedido integer, 
			cantidad integer, 
			precio_unitario numeric, 
			dp_subtotal numeric, 
				id_producto integer, 
				nombre character varying, 
				precio numeric, 
				stock integer, 
				categoria character varying, 
				codigo_barra character varying
	)
	language plpgsql
	as $$
		begin
			return query
			select
				p.id,
				p.id_cliente,
					c.nombre,
				p.id_direccion,
					d.calle,
					d.numero,
					d.ciudad,
					d.provincia,
				p.metodo_pago,
				p.estatus,
				p.tiempo_estimado_entrega,
				p.tiempo_entrega,
				p.created_at,
				P.updated_at,
				(sum(dp.cantidad * dp.precio_unitario) over(partition by p.id))::numeric(15,2) as total,
					dp.id,
					dp.cantidad,
					dp.precio_unitario,
					dp.cantidad * dp.precio_unitario as dp_subtotal,
						pr.id,
						pr.nombre,
						pr.precio,
						pr.stock,
						pr.categoria,
						pr.codigo_barra
			from pedidos p
			join clientes c on p.id_cliente = c.id
			join direcciones d on p.id_direccion = d.id
			join detalles_pedido dp on p.id = dp.id_pedido
			join productos pr on dp.id_producto = pr.id;
		end;
	$$
;

create or replace function obtener_clientes_pedidos (
	p_id_cliente integer
)
	returns table (
		id_pedido integer, 
		id_cliente integer, 
		id_direccion integer, 
		calle character varying, 
		numero integer, 
		ciudad character varying, 
		provincia character varying, 
		metodo_pago character varying, 
		estatus integer, 
		tiempo_estimado_entrega smallint, 
		tiempo_entrega smallint, 
		created_at timestamp without time zone, 
		updated_at timestamp without time zone, 
		total numeric, 
		id_detalles_pedido integer, 
		cantidad integer, 
		precio_unitario numeric, 
		subtotal numeric, 
		id_producto integer, 
		nombre character varying, 
		precio numeric, 
		stock integer, 
		categoria character varying
	)
	language plpgsql
	as $$
		begin
			return query
			select
				p.id,
				p.id_cliente,
				p.id_direccion,
					d.calle,
					d.numero,
					d.ciudad,
					d.provincia,
				p.metodo_pago,
				p.estatus,
				p.tiempo_estimado_entrega,
				p.tiempo_entrega,
				p.created_at,
				p.updated_at,
				(sum(dp.cantidad * dp.precio_unitario) over(partition by p.id))::numeric(15,2) as total,
					dp.id,
					dp.cantidad,
					dp.precio_unitario,
					dp.cantidad * dp.precio_unitario as dp_subtotal,
						pr.id,
						pr.nombre,
						pr.precio,
						pr.stock,
						pr.categoria
			from pedidos p
			join direcciones d on p.id_direccion = d.id
			join detalles_pedido dp on p.id = dp.id_pedido
			join productos pr on dp.id_producto = pr.id
			where p.id_cliente  = p_id_cliente;
		end;
	$$
;

create or replace function obtener_id_pedido_pedidos (
	p_id_pedidos integer
)
	returns table (
		id_pedido integer, 
		id_cliente integer, 
			nombre_cliente character varying, 
			apellido_cliente character varying, 
		id_direccion integer, 
			calle character varying, 
			numero integer, 
			ciudad character varying, 
			provincia character varying, 
		metodo_pago character varying, 
		estatus integer, 
		tiempo_estimado_entrega smallint, 
		tiempo_entrega smallint, 
			id_detalles_pedido integer, 
			cantidad integer, 
			precio_unitario numeric, 
				id_producto integer, 
				nombre character varying, 
				precio numeric, 
				stock integer, 
				categoria character varying, 
				codigo_barra character varying
	)
	language plpgsql
	as $$
		begin
			return query
			select
				p.id,
				p.id_cliente,
					c.nombre,
					c.apellido,
				p.id_direccion,
					d.calle,
					d.numero,
					d.ciudad,
					d.provincia,
				p.metodo_pago,
				p.estatus,
				p.tiempo_estimado_entrega,
				p.tiempo_entrega,
					dp.id,
					dp.cantidad,
					dp.precio_unitario,
						pr.id,
						pr.nombre,
						pr.precio,
						pr.stock,
						pr.categoria,
						pr.codigo_barra
			from pedidos p
			join clientes c on p.id_cliente = c.id
			join direcciones d on p.id_direccion = d.id
			join detalles_pedido dp on p.id = dp.id_pedido
			join productos pr on dp.id_producto = pr.id
			where p.id in (
				select dp.id_pedido 
				from detalles_pedido dp 
				where dp.id_pedido = p_id_pedidos
			);
		end;
	$$
;

create or replace function obtener_productos_pedidos (
	p_id_producto integer
)
	returns table (
		id_pedido integer, 
		id_cliente integer, 
		id_direccion integer, 
		metodo_pago character varying, 
		estatus integer, 
		tiempo_estimado_entrega smallint, 
		tiempo_entrega smallint, 
		total numeric, 
			id_detalles_pedido integer, 
			cantidad integer, 
			precio_unitario numeric, 
			subtotal numeric, 
				id_producto integer, 
				nombre character varying, 
				precio numeric, 
				stock integer, 
				categoria character varying, 
				codigo_barra character varying
	)
	language plpgsql
	as $$
		begin
			return query
			select
				p.id,
				p.id_cliente,
				p.id_direccion,
				p.metodo_pago,
				p.estatus,
				p.tiempo_estimado_entrega,
				p.tiempo_entrega,
				(sum(dp.cantidad * dp.precio_unitario) over(partition by p.id))::numeric(10,2) as total,
					dp.id,
					dp.cantidad,
					dp.precio_unitario,
					dp.cantidad * dp.precio_unitario as dp_subtotal,
						pr.id,
						pr.nombre,
						pr.precio,
						pr.stock,
						pr.categoria,
						pr.codigo_barra
			from pedidos p
			join detalles_pedido dp on p.id = dp.id_pedido
			join productos pr on dp.id_producto = pr.id
			where p.id in (
				select dp.id_pedido 
				from detalles_pedido dp 
				where dp.id_producto = p_id_producto
			);
		end;
	$$
;

create or replace function pedidos_por_fecha (
	pedido_inicio date, 
	pedido_fin date
)
	returns table (
		id_pedido integer,
		cliente_id integer,
		metodo_pago character varying,
		tiempo_estimado_entrega smallint, 
		fecha_creacion timestamp without time zone
	)
	language plpgsql
	as $$
		begin
			return query
			select 
				p.id, 
				p.id_cliente, 
				p.metodo_pago, 
				p.tiempo_estimado_entrega, 
				p.created_at
			from pedidos p
			where p.created_at between pedido_inicio and pedido_fin;
		end
	$$
;

create or replace function sp_actualizar_precio_categoria (
	p_categoria character varying, 
	p_porcentaje_aumento integer
)
	returns void
	language plpgsql
	as $$
		begin
			update productos
				set precio = precio + (precio * (p_porcentaje_aumento / 100.0))
				where categoria = p_categoria;
		end;
	$$
;
 
create or replace function sp_actualizar_precio_categoria (
	p_categoria character varying, 
	p_porcentaje_aumento smallint
)
	returns void
	language plpgsql
	as $$
		begin
			update productos
				set precio = precio * (p_porcentaje_aumento / 100)
				where categoria = p_categoria;
		end;
	$$
;

create or replace function validar_precio ()
	returns trigger
	language plpgsql
	as $$
		begin
			if new.precio <= 0 then
				raise exception '¡El precio de un producto no puede ser cero o negativo!';
			end if;
			return new;
		end;
	$$
;

-- 	DROPS

drop procedure actualizar_stock;

drop function actualizar_stock_auto;

drop function almacenar_precios;

drop function caja_rejistradora;

drop function caja_rejistradora;

drop function caja_rejistradora_2;

drop function consultar_stock;

drop function consultar_stock;

drop function fn_obtener_ticket_pedido;

drop function fn_obtener_ticket_pedido;

drop function fn_obtener_ticket_pedido;

drop function get_all_clientes;

drop function get_all_historial;

drop function get_all_productos;

drop function get_all_usuarios;

drop function get_direcciones;

drop function get_only_clientes;

drop function obtener_all_pedidos;

drop function obtener_clientes_pedidos;

drop function obtener_id_pedido_pedidos;

drop function obtener_productos_pedidos;

drop function pedidos_por_fecha;

drop function sp_actualizar_precio_categoria;

drop function sp_actualizar_precio_categoria;

drop function validar_precio;