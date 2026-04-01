create or replace function obtener_productos_pedidos
(
p_id_producto int
)
	returns table(
	id_pedido int,
	id_cliente int,
	id_direccion int,
	metodo_pago varchar(50),
	tiempo_estimado_entrega smallint,
	tiempo_entrega smallint,
		id_detalles_pedido int,
		cantidad int,
		precio_unitario numeric(10,2),
			id_producto int,
			nombre varchar(50),
			precio numeric(10,2),
			stock int,
			categoria varchar(50),
			codigo_barra varchar(50)
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
	$$;

DROP FUNCTION obtener_productos_pedidos(integer)

select * from obtener_productos_pedidos(5)