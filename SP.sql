-- Funcion Base de Datos. {Actualizar Stock luego de Compra}
create or replace function public.actualizar_stock_auto()
	returns trigger
	language plpgsql
	as $function$
		begin
			update productos
				set stock = stock - new.cantidad
				where id = new.id_producto;
			return new;
		end;
	$function$
;

-- Funcion Base de Datos. {Registrar Cambio de Precio Fijo}
create or replace function public.almacenar_precios()
	returns trigger
	language plpgsql
	as $function$
		begin
			if new.precio <> old.precio then
				insert into registro_precios (
					id_producto,
					precio_anterior,
					precio_nuevo,
					fecha_inicio,
					es_promocion,
					activa,
					motivo
				) 
				values (
					new.id,
					old.precio,
					new.precio,
					current_timestamp,
					FALSE,
					FALSE,
					'Cambio de precio fijo'
				);
			end if;
			return new;
		end;
	$function$
;

-- Funcion Base de Datos. {Realizar Compra (Version Vieja)}
create or replace function public.caja_rejistradora(
	v_codigo_barra character varying, 
	v_cantidad integer, 
	v_id_pedido integer
	)
	returns table(
		recibo_producto character varying, 
		recibo_cantidad integer, 
		recibo_precio integer, 
		recibo_subtotal integer
		)
	language plpgsql
	as $function$
		declare 
			v_id_producto int;
			v_precio_unitario int;
			v_nombre_producto varchar;
			v_stock_actual int;
		begin
			select 
				p.id, 
				coalesce(
					rp.precio_nuevo, 
					p.precio
					),
				p.precio, 
				p.nombre, 
				p.stock
			into 
				v_id_producto, 
				v_precio_unitario, 
				v_nombre_producto, 
				v_stock_actual 
			from productos p
			left join registro_precios rp on p.id = rp.id_producto 
		        and rp.es_promocion = true 
		        and rp.activa = true 
		        and current_timestamp between rp.fecha_inicio and rp.fecha_fin
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
	$function$
;

-- Funcion Base de Datos. {Realizar Compra (Version Vieja 2)}
create or replace function public.caja_rejistradora_2(
	v_codigo_barra character varying, 
	v_cantidad integer, 
	v_id_pedido integer
	)
	returns table(
		recibo_producto character varying, 
		recibo_cantidad integer, 
		recibo_precio integer, 
		recibo_subtotal integer
		)
	language plpgsql
	as $function$
		declare 
			v_id_producto int;
			v_precio_unitario int;
			v_nombre_producto varchar;
			v_stock_actual int;
		begin
			select 
				p.id, 
				coalesce(
					rp.precio_nuevo, 
					p.precio
					),
				p.nombre, 
				p.stock
			into 
				v_id_producto, 
				v_precio_unitario, 
				v_nombre_producto, 
				v_stock_actual 
			from productos p
			left join registro_precios rp on p.id = rp.id_producto 
		        and rp.es_promocion = true 
		        and rp.activa = true 
		        and current_timestamp between rp.fecha_inicio and rp.fecha_fin
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
	$function$
;

-- Funcion Base de Datos. {Consultar Stock atravez de Codigo de Barras}
create or replace function public.consultar_stock(
	p_codigo_barra character varying
	)
	returns table(
		p_stock integer
		)
	language plpgsql
	as $function$
		begin
			return query
			select p.stock 
			from productos p
			where p.codigo_barra = p_codigo_barra;
		end;
	$function$
;

-- Funcion Base de Datos. {Leer Pedido atravez de ID de Pedido}
create or replace function public.fn_obtener_ticket_pedido(
	p_id_pedido integer
	)
	returns table(
		p_nombre character varying, 
		dp_cantidad integer, 
		dp_precio_unitario numeric, 
		dp_subtotal numeric
		)
	language plpgsql
	as $function$
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
	$function$
;

-- Funcion Base de Datos. {Leer Todos los Clientes}
create or replace function public.get_all_clientes()
	returns table(
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
	as $function$
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
	$function$
;

-- Funcion Base de Datos. {Leer Todo el Historial de Precios}
create or replace function public.get_all_historial()
	returns table(
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
	as $function$
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
	$function$
;

-- Funcion Base de Datos. {Leer Todos los Productos}
create or replace function public.get_all_productos()
	returns table(
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
			tamanio integer, 
				es_promocion boolean, 
				precio_nuevo numeric, 
				motivo character varying, 
				porcentaje_descuento integer
		)
	language plpgsql
	as $function$
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
					a.tamanio,
						CASE WHEN rp.id IS not null THEN true ELSE FALSE end as en_promocion,
					    rp.precio_nuevo,
					    rp.motivo,
					    rp.porcentaje_descuento
			from productos p
			left join archivos a on p.id = a.id_producto
		    left join registro_precios rp on p.id = rp.id_producto 
		        and current_timestamp between rp.fecha_inicio and rp.fecha_fin
				and rp.activa = true
			order by stock desc;
		end;
	$function$
;

-- Funcion Base de Datos. {Leer Todos los Registros de Precios}
create or replace function public.get_all_promociones()
	returns table(
		id integer, 
		id_producto integer, 
		motivo character varying, 
		precio_nuevo numeric, 
		precio_anterior numeric, 
		porcentaje_descuento integer, 
		fecha_inicio timestamp with time zone, 
		fecha_fin timestamp with time zone, 
		es_promocion boolean, 
		activa boolean, 
		created_at timestamp with time zone, 
			nombre character varying, 
			categoria character varying, 
			codigo_barra character varying, 
			activo boolean
		)
	language plpgsql
	as $function$
		begin
			return query
			select
				rp.id, 
				rp.id_producto, 
				rp.motivo, 
				rp.precio_nuevo, 
				rp.precio_anterior, 
				rp.porcentaje_descuento, 
				rp.fecha_inicio, 
				rp.fecha_fin, 
				rp.es_promocion,
				rp.activa,
				rp.created_at,
					p.nombre,
					p.categoria, 
					p.codigo_barra,
					p.activo
			from registro_precios rp
			join productos p on rp.id_producto = p.id;
		end;
	$function$
;

-- Funcion Base de Datos. {Leer Todos los Registros de Precios (Version Vieja)}
create or replace function public.get_all_registros()
	returns table(
		id integer, 
		id_producto integer, 
		precio_anterior numeric, 
		precio_nuevo numeric, 
		fecha_inicio timestamp without time zone, 
		fecha_fin timestamp without time zone, 
		es_promocion boolean, 
			nombre character varying, 
			categoria character varying, 
			codigo_barra character varying, 
			activo boolean
		)
	language plpgsql
	as $function$
		begin
			return query
			select
				rp.id, 
				rp.id_producto, 
				rp.precio_anterior, 
				rp.precio_nuevo, 
				rp.fecha_inicio,
				rp.fecha_fin,
				rp.es_promocion,
					p.nombre,
					p.categoria, 
					p.codigo_barra,
					p.activo
			from registro_precios rp
			join productos p on rp.id_producto = p.id;
		end;
	$function$
;

-- Funcion Base de Datos. {Leer Todos los Usuarios}
create or replace function public.get_all_usuarios()
	returns table(
		id_usuario integer, 
		nombre character varying, 
		email character varying, 
		dni character varying, 
		id_rol integer[], 
		activo boolean, 
		created_at timestamp without time zone
		)
	language plpgsql
	as $function$
		begin
			return query
			select
				u.id,
				u.nombre,
				u.email,
				u.dni,
				array_agg(ur.id_rol) as id_rol,
				u.activo,
				u.created_at
			from usuarios u
			left join usuarios_roles ur on u.id = ur.id_usuario
				group by 
					u.id, 
					u.nombre, 
					u.email, 
					u.dni, 
					u.activo, 
					u.created_at;
		end;
	$function$
;

-- Funcion Base de Datos. {Leer Todas las Direcciones atravez del ID del Cliente}
create or replace function public.get_direcciones(
	p_id_cliente integer
	)
	returns SETOF direcciones
	language plpgsql
	as $function$
		begin
			return query
			select d.* 
			from direcciones d
			join pedidos p on d.id = p.id_direccion 
			where p.id_cliente = p_id_cliente;
		end;
	$function$
;

-- Funcion Base de Datos. {Leer Clientes}
create or replace function public.get_only_clientes()
	returns table(
		id_cliente integer, 
			id_direccion integer, 
			calle character varying, 
			numero integer, 
			barrio character varying, 
			ciudad character varying, 
			provincia character varying
		)
	language plpgsql
	as $function$
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

-- Funcion Base de Datos. {Leer Todos los Pedidos}
create or replace function public.obtener_all_pedidos()
	returns table(
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
				codigo_barra character varying, 
					es_promocion boolean, 
					motivo character varying, 
					precio_anterior numeric, 
					precio_nuevo numeric, 
					porcentaje_descuento integer
		)
	language plpgsql
	as $function$
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
						pr.codigo_barra,
							(rp.id IS not null) as es_promocion,
        					rp.motivo,
                            rp.precio_anterior,
                            rp.precio_nuevo,
                            rp.porcentaje_descuento
			from pedidos p
			join clientes c on p.id_cliente = c.id
			join direcciones d on p.id_direccion = d.id
			join detalles_pedido dp on p.id = dp.id_pedido
			join productos pr on dp.id_producto = pr.id
			left join registro_precios rp 
		        on rp.id_producto = pr.id 
		        and rp.es_promocion = true 
		        and p.created_at >= rp.fecha_inicio 
		        and p.created_at <= rp.fecha_fin;
		end;
	$function$
;

-- Funcion Base de Datos. {Leer Pedido atravez de ID de Cliente}
create or replace function public.obtener_clientes_pedidos(
	p_id_cliente integer
	)
	returns table(
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
				categoria character varying, 
					es_promocion boolean, 
					motivo character varying, 
					precio_anterior numeric, 
					precio_nuevo numeric, 
					porcentaje_descuento integer
		)
	language plpgsql
	as $function$
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
						pr.categoria,
							(rp.id IS not null) as es_promocion,
        					rp.motivo,
                            rp.precio_anterior,
                            rp.precio_nuevo,
                            rp.porcentaje_descuento
			from pedidos p
			join direcciones d on p.id_direccion = d.id
			join detalles_pedido dp on p.id = dp.id_pedido
			join productos pr on dp.id_producto = pr.id
			left join registro_precios rp 
		         on rp.id_producto = pr.id 
		         and rp.es_promocion = true 
		         and p.created_at >= rp.fecha_inicio 
		         and p.created_at <= rp.fecha_fin
			where p.id_cliente  = p_id_cliente;
		end;
	$function$
;

-- Funcion Base de Datos. {Leer Favoritos atravez de ID de Cliente}
create or replace function public.obtener_favoritos_cliente(
	cliente_id integer
	)
	returns table(
		fav_created_at timestamp without time zone, 
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
	as $function$
		begin
			return QUERY
			select 
				f.created_at as fav_created_at, 
					p.id, 
					p.nombre, 
					p.precio, 
					p.stock, 
					p.categoria, 
					p.codigo_barra, 
					p.created_at, 
					p.updated_at, 
					p.activo,
						a.id as id_imagen, 
						a.s3_key, 
						a.tipo_contenido, 
						a.tamanio
			from favoritos f
			join productos p on f.id_producto = p.id
			left join archivos a on p.id = a.id_producto
			where f.id_cliente = cliente_id;
		end;
	$function$
;

-- Funcion Base de Datos. {Leer Pedido atravez de ID de Pedido}
create or replace function public.obtener_id_pedido_pedidos(
	p_id_pedidos integer
	)
	returns table(
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
	as $function$
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

-- Funcion Base de Datos. {Leer Pedido atravez de ID de Producto}
create or replace function public.obtener_productos_pedidos(
	p_id_producto integer
	)
	returns table(
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
	as $function$
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

-- Funcion Base de Datos. {Leer Pedidos atravez de Fecha de Pedido}
create or replace function public.pedidos_por_fecha(
	pedido_inicio date, 
	pedido_fin date
	)
	returns table(
		id_pedido integer, 
		cliente_id integer, 
		metodo_pago character varying, 
		tiempo_estimado_entrega smallint, 
		fecha_creacion timestamp without time zone
		)
	language plpgsql
	as $function$
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
	$function$
;

-- Funcion Base de Datos. {Actualizar Precio de una Categoria}
create or replace function public.sp_actualizar_precio_categoria(
	p_categoria character varying, 
	p_porcentaje_aumento smallint
	)
	returns void
	language plpgsql
	as $function$
		begin
			update productos
				set precio = precio * (p_porcentaje_aumento / 100)
				where categoria = p_categoria;
		end;
	$function$
;

-- Funcion Base de Datos. {Verificar Precio Superior a 0}
create or replace function public.validar_precio()
	returns trigger
	language plpgsql
	as $function$
		begin
			if new.precio <= 0 then
				raise exception '¡El precio de un producto no puede ser cero o negativo!';
			end if;
			return new;
		end;
	$function$
;

#Borrar Funciones de Base de Datos

drop function public.actualizar_stock_auto();

drop function public.almacenar_precios();

drop function public.caja_rejistradora(varchar, int4, int4);

drop function public.caja_rejistradora_2(varchar, int4, int4);

drop function public.consultar_stock(varchar);

drop function public.fn_obtener_ticket_pedido(int4);

drop function public.get_all_clientes();

drop function public.get_all_historial();

drop function public.get_all_productos();

drop function public.get_all_promociones();

drop function public.get_all_registros();

drop function public.get_all_usuarios();

drop function public.get_direcciones(int4);

drop function public.get_only_clientes();

drop function public.obtener_all_pedidos();

drop function public.obtener_clientes_pedidos(int4);

drop function public.obtener_favoritos_cliente(int4);

drop function public.obtener_id_pedido_pedidos(int4);

drop function public.obtener_productos_pedidos(int4);

drop function public.pedidos_por_fecha(date, date);

drop function public.sp_actualizar_precio_categoria(varchar, int2);

drop function public.validar_precio();