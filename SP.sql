-- DROP PROCEDURE public.actualizar_stock(int4, int4);

CREATE OR REPLACE PROCEDURE public.actualizar_stock(IN p_id_producto integer, IN p_cantidad integer)
 LANGUAGE plpgsql
AS $procedure$
		declare
			v_stock_actual int;
		begin
			select p.stock into v_stock_actual 
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
	$procedure$
;

-- DROP FUNCTION public.actualizar_stock_auto();

CREATE OR REPLACE FUNCTION public.actualizar_stock_auto()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
	begin
		update productos
			set stock = stock - new.cantidad
			where id = new.id_producto;
		return new;
	end;
$function$
;

-- DROP FUNCTION public.almacenar_precios();

CREATE OR REPLACE FUNCTION public.almacenar_precios()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
	begin
		if new.precio <> old.precio then
			insert into historial_precios
				(
				id_producto,
				precio_viejo,
				precio_nuevo,
				updated_at
				)
			values
				(
				new.id,
				old.precio,
				new.precio,
				current_timestamp
				);
		end if;
		return new;
	end;
$function$
;

-- DROP FUNCTION public.caja_rejistradora(varchar, int4);

CREATE OR REPLACE FUNCTION public.caja_rejistradora(p_codigo_barra character varying, caja_cantidad integer)
 RETURNS TABLE(dp_id_pedido integer, dp_id_producto integer, dp_cantidad integer, dp_precio_unitario integer)
 LANGUAGE plpgsql
AS $function$
	begin
		select dp.id_pedido, dp.id_producto, dp.cantidad = dp_cantidad, dp.precio_unitario
		from detalles_pedidos
		join productos on dp.id_producto = p.id
		where p.codigo_barra = p_codigo_barra;
	end;
$function$
;

-- DROP FUNCTION public.caja_rejistradora(varchar, int4, int4);

CREATE OR REPLACE FUNCTION public.caja_rejistradora(v_codigo_barra character varying, v_cantidad integer, v_id_pedido integer)
 RETURNS TABLE(recibo_producto character varying, recibo_cantidad integer, recibo_precio integer, recibo_subtotal integer)
 LANGUAGE plpgsql
AS $function$
	declare 
		v_id_producto int;
		v_precio_unitario int;
		v_nombre_producto varchar;
		v_stock_actual int;
	begin
		select p.id, p.precio, p.nombre, p.stock
			into v_id_producto, v_precio_unitario, v_nombre_producto, v_stock_actual 
			from productos p
			where p.codigo_barra = v_codigo_barra;
		if (v_stock_actual + v_cantidad) >= 0 then
			insert into detalles_pedido
				(
				id_pedido, 
				id_producto, 
				cantidad, 
				precio_unitario
				)
			values
				(
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
			select v_nombre_producto, v_cantidad, v_precio_unitario, (v_cantidad * v_precio_unitario);
	end;
$function$
;

-- DROP FUNCTION public.caja_rejistradora_2(varchar, int4, int4);

CREATE OR REPLACE FUNCTION public.caja_rejistradora_2(v_codigo_barra character varying, v_cantidad integer, v_id_pedido integer)
 RETURNS TABLE(recibo_producto character varying, recibo_cantidad integer, recibo_precio integer, recibo_subtotal integer)
 LANGUAGE plpgsql
AS $function$
	declare 
		v_id_producto int;
		v_precio_unitario int;
		v_nombre_producto varchar;
		v_stock_actual int;
	begin
		select p.id, p.precio, p.nombre, p.stock
			into v_id_producto, v_precio_unitario, v_nombre_producto, v_stock_actual 
			from productos p
			where p.codigo_barra = v_codigo_barra;
		if v_id_producto is null then
			raise exception '¡Producto Inexistente! Revisa el codigo de barras';
		end if;
		if (v_stock_actual - v_cantidad) >= 0 then
			insert into detalles_pedido
				(
				id_pedido, 
				id_producto, 
				cantidad, 
				precio_unitario
				)
			values
				(
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
			select v_nombre_producto, v_cantidad, v_precio_unitario, (v_cantidad * v_precio_unitario);
	end;
$function$
;

-- DROP FUNCTION public.consultar_stock(varchar);

CREATE OR REPLACE FUNCTION public.consultar_stock(p_codigo_barra character varying)
 RETURNS TABLE(p_stock integer)
 LANGUAGE plpgsql
AS $function$
	begin
		return query
			select p.stock 
				from productos p
				where p.codigo_barra = p_codigo_barra;
	end;
$function$
;

-- DROP FUNCTION public.consultar_stock(int4);

CREATE OR REPLACE FUNCTION public.consultar_stock(codigo_barra integer)
 RETURNS TABLE(p_stock integer)
 LANGUAGE plpgsql
AS $function$
	begin
		return query
			select p.stock
				from productos p
				where p.id = p.codigo_barra;
	end;
$function$
;

-- DROP FUNCTION public.fn_obtener_ticket_pedido(int4, int2);

CREATE OR REPLACE FUNCTION public.fn_obtener_ticket_pedido(p_id_pedido integer, p_dias_reales smallint)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
		begin
			update pedidos
				set p.tiempo_entrega = p_dias_reales
				where p.id = p_id_pedido;
			if p.tiempo_entrega > p.tiempo_estimado_entrega then
				raise notice 'El pedido no llego en el tiempo estimado';
			end if;
		end;
	$function$
;

-- DROP FUNCTION public.fn_obtener_ticket_pedido(int4);

CREATE OR REPLACE FUNCTION public.fn_obtener_ticket_pedido(p_id_pedido integer)
 RETURNS TABLE(p_nombre character varying, dp_cantidad integer, dp_precio_unitario numeric, dp_subtotal numeric)
 LANGUAGE plpgsql
AS $function$
	begin
		return query
			select p.nombre, dp.cantidad, dp.precio_unitario, sum(dp.cantidad * dp.precio_unitario) as dp_subtotal
				from detalles_pedido dp
				join productos p on p.id = dp.id_producto
				where dp.id_pedido = p_id_pedido
			group by p.nombre, dp.cantidad, dp.precio_unitario;
	end;
$function$
;

-- DROP FUNCTION public.fn_obtener_ticket_pedido(int4, int4);

CREATE OR REPLACE FUNCTION public.fn_obtener_ticket_pedido(p_id_pedido integer, p_dias_reales integer)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
		declare p_tiempo_estimado_entrega int2;
		begin
			update pedidos
				set tiempo_entrega = p_dias_reales
				where id = p_id_pedido
				returning tiempo_estimado_entrega into p_tiempo_estimado_entrega;
			if p_dias_reales > p_tiempo_estimado_entrega then
				raise notice 'El pedido no llego en el tiempo estimado';
			end if;
		end;
	$function$
;

-- DROP FUNCTION public.get_all_clientes();

CREATE OR REPLACE FUNCTION public.get_all_clientes()
 RETURNS TABLE(id_cliente integer, nombre character varying, email character varying, dni character varying, apellido character varying, usuario character varying, id_rol integer, id_direccion integer, calle character varying, numero integer, barrio character varying, ciudad character varying, provincia character varying)
 LANGUAGE plpgsql
AS $function$
begin
	return query
	select
		c.id,
		c.nombre,
		c.email,
		c.dni,
		c.apellido,
		c.usuario,
		c.id_rol,
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
$function$
;

-- DROP FUNCTION public.get_direcciones(int4);

CREATE OR REPLACE FUNCTION public.get_direcciones(p_id_cliente integer)
 RETURNS SETOF direcciones
 LANGUAGE plpgsql
AS $function$
begin
	return query
	select d.* 
	from direcciones d
	join pedidos p on d.id = p.id_direccion 
	where p.id_cliente = p_id_cliente;
end;
$function$
;

-- DROP FUNCTION public.get_only_clientes();

CREATE OR REPLACE FUNCTION public.get_only_clientes()
 RETURNS TABLE(id_cliente integer, id_direccion integer, calle character varying, numero integer, barrio character varying, ciudad character varying, provincia character varying)
 LANGUAGE plpgsql
AS $function$
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
$function$
;

-- DROP FUNCTION public.obtener_all_pedidos();

CREATE OR REPLACE FUNCTION public.obtener_all_pedidos()
 RETURNS TABLE(id_pedido integer, id_cliente integer, nombre_cliente character varying, apellido_cliente character varying, id_direccion integer, calle character varying, numero integer, ciudad character varying, provincia character varying, metodo_pago character varying, estatus integer, tiempo_estimado_entrega smallint, tiempo_entrega smallint, id_detalles_pedido integer, cantidad integer, precio_unitario numeric, id_producto integer, nombre character varying, precio numeric, stock integer, categoria character varying, codigo_barra character varying)
 LANGUAGE plpgsql
AS $function$
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
					join productos pr on dp.id_producto = pr.id;
		end;
	$function$
;

-- DROP FUNCTION public.obtener_id_pedido_pedidos(int4);

CREATE OR REPLACE FUNCTION public.obtener_id_pedido_pedidos(p_id_pedidos integer)
 RETURNS TABLE(id_pedido integer, id_cliente integer, nombre_cliente character varying, apellido_cliente character varying, id_direccion integer, calle character varying, numero integer, ciudad character varying, provincia character varying, metodo_pago character varying, estatus integer, tiempo_estimado_entrega smallint, tiempo_entrega smallint, id_detalles_pedido integer, cantidad integer, precio_unitario numeric, id_producto integer, nombre character varying, precio numeric, stock integer, categoria character varying, codigo_barra character varying)
 LANGUAGE plpgsql
AS $function$
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
	$function$
;

-- DROP FUNCTION public.obtener_productos_pedidos(int4);

CREATE OR REPLACE FUNCTION public.obtener_productos_pedidos(p_id_producto integer)
 RETURNS TABLE(id_pedido integer, id_cliente integer, id_direccion integer, metodo_pago character varying, estatus integer, tiempo_estimado_entrega smallint, tiempo_entrega smallint, total numeric, id_detalles_pedido integer, cantidad integer, precio_unitario numeric, subtotal numeric, id_producto integer, nombre character varying, precio numeric, stock integer, categoria character varying, codigo_barra character varying)
 LANGUAGE plpgsql
AS $function$
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
	$function$
;

-- DROP FUNCTION public.pedidos_por_fecha(date, date);

CREATE OR REPLACE FUNCTION public.pedidos_por_fecha(pedido_inicio date, pedido_fin date)
 RETURNS TABLE(id_pedido integer, cliente_id integer, metodo_pago character varying, tiempo_estimado_entrega smallint, fecha_creacion timestamp without time zone)
 LANGUAGE plpgsql
AS $function$
		begin
			return query
				select p.id, p.id_cliente, p.metodo_pago, p.tiempo_estimado_entrega, p.created_at
					from pedidos p
					where p.created_at between pedido_inicio and pedido_fin;
		end
	$function$
;

-- DROP FUNCTION public.sp_actualizar_precio_categoria(varchar, int4);

CREATE OR REPLACE FUNCTION public.sp_actualizar_precio_categoria(p_categoria character varying, p_porcentaje_aumento integer)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
	begin
		update productos
			set precio = precio + (precio * (p_porcentaje_aumento / 100.0))
			where categoria = p_categoria;
	end;
$function$
;

-- DROP FUNCTION public.sp_actualizar_precio_categoria(varchar, int2);

CREATE OR REPLACE FUNCTION public.sp_actualizar_precio_categoria(p_categoria character varying, p_porcentaje_aumento smallint)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
	begin
		update productos
			set precio = precio * (p_porcentaje_aumento / 100)
			where categoria = p_categoria;
	end;
$function$
;

-- DROP FUNCTION public.validar_precio();

CREATE OR REPLACE FUNCTION public.validar_precio()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
	begin
		if new.precio <= 0 then
			raise exception '¡El precio de un producto no puede ser cero o negativo!';
		end if;
		return new;
	end;
$function$
;