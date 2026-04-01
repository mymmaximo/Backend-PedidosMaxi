INSERT INTO public.clientes (nombre,email,dni,apellido,created_at,updated_at,usuario,contrasena) VALUES
	 ('Lucía','lucia.f@email.com','38987654','Fernández','2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735','f123','f123'),
	 ('Diego','diego.alonso@email.com','40111222','Alonso','2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735','a123','a123'),
	 ('Sofía','smartinez@email.com','39555666','Martínez','2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735','m123','m123'),
	 ('Javier','javi.lopez@email.com','34888999','López','2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735','l123','l123'),
	 ('Camila','cami.garcia@email.com','41222333','García','2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735','g123','g123'),
	 ('Joaquín','joaquin.ruiz@email.com','37444555','Ruiz','2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735','r123','r123'),
	 ('Goku','kakarotto@ccmail.com','8000666','Son','2026-03-18 11:18:25.044441','2026-03-25 09:57:35.714557','son_goku','gohan'),
	 ('Jonny','jonny@sbr.com','777888999','Joestar','2026-03-27 08:42:48.017243',NULL,'jo_jo','zeppeli'),
	 ('Martina','martinajubelie@gmail.com','8523697','Jubelie','2026-03-09 12:42:26.964735','2026-03-30 11:04:12.561931','J123','J123'),
	 ('Maximo','maxgiesenow@gmail.com','42638965','Giesenow','2026-03-31 08:45:33.835518',NULL,'mym_maximo','123');
INSERT INTO public.clientes (nombre,email,dni,apellido,created_at,updated_at,usuario,contrasena) VALUES
	 ('Jodio','jodiojoestar@miami.com','99999999','Joestar','2026-04-01 10:01:43.41078',NULL,'JoJo','$2b$12$PqcK14bDaS2Unhy3DgnEp.UlHBX2eo4CVROfj2W6H3TnX29YDaeLK');
INSERT INTO public.detalles_pedido (id_pedido,id_producto,cantidad,precio_unitario) VALUES
	 (1,10,1,45000.00),
	 (2,5,1,280000.00),
	 (2,8,2,250000.00),
	 (3,3,1,300000.00),
	 (4,6,2,120000.00),
	 (5,4,1,800000.00),
	 (6,7,1,110000.00),
	 (7,2,1,450000.00),
	 (7,1,1,350000.00),
	 (8,9,3,45000.00);
INSERT INTO public.detalles_pedido (id_pedido,id_producto,cantidad,precio_unitario) VALUES
	 (9,6,1,120000.00),
	 (5,10,80,350000.00),
	 (1,5,10,280000.00),
	 (1,2,10,3000.00);
INSERT INTO public.direcciones (calle,numero,barrio,ciudad,provincia,id_cliente) VALUES
	 ('Av. San Martín',150,'Centro','Villa Carlos Paz','Córdoba',4),
	 ('Bv. Illia',250,'Centro','Córdoba','Córdoba',4),
	 ('Av. Fuerza Aérea',2100,'Los Naranjos','Córdoba','Córdoba',5),
	 ('Recta Martinolli',6500,'Argüello','Córdoba','Córdoba',6),
	 ('Av. Sabattini',3200,'Empalme','Córdoba','Córdoba',7),
	 ('kent',1000000,'super','smallville','catamarca',7),
	 ('Av. Hipólito Yrigoyen',400,'Nueva Córdoba','Córdoba','Córdoba',1),
	 ('Av. Colon',3900,'Tejeda','Cordoba','Cordoba',5),
	 ('Rafael Núñez',3500,'Cerro de las Rosas','Córdoba','Córdoba',1),
	 ('24 de Septiembre',1200,'General Paz','Córdoba','Córdoba',1);
INSERT INTO public.historial_precios (id_producto,precio_viejo,precio_nuevo,updated_at) VALUES
	 (1,5.00,50000.00,'2026-03-12 11:51:01.439941'),
	 (1,50000.00,5000.00,'2026-03-12 11:51:19.042781'),
	 (3,300000.00,500000.00,'2026-03-12 11:58:04.020623'),
	 (10,45000.00,1500000.00,'2026-03-12 11:58:43.665482'),
	 (10,1500000.00,150000.00,'2026-03-12 11:59:03.881449'),
	 (10,150000.00,1500.00,'2026-03-12 12:14:39.520234'),
	 (5,280000.00,8000.00,'2026-03-18 11:19:51.047676');
INSERT INTO public.pedidos (id_cliente,id_direccion,metodo_pago,tiempo_entrega,tiempo_estimado_entrega,created_at,updated_at) VALUES
	 (2,2,'Transferencia',4,2,'2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735'),
	 (5,5,'Tarjeta de Crédito',NULL,4,'2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735'),
	 (1,1,'Transferencia',2,2,'2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735'),
	 (6,6,'MercadoPago',2,3,'2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735'),
	 (2,2,'Efectivo',1,1,'2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735'),
	 (3,8,'Transferencia',7,7,'2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735'),
	 (4,4,'Efectivo',1,1,'2024-03-09 12:42:26.964','2026-03-09 12:42:26.964735'),
	 (7,7,'Tarjeta de Crédito',NULL,5,'2025-03-09 12:42:26.964','2026-03-09 12:42:26.964735'),
	 (1,2,'MercadoPago',4,0,'2026-03-09 12:42:26.964735','2026-03-17 09:01:02.737864'),
	 (3,3,'MercadoPago',5,1,'2023-03-09 12:42:26.964','2026-03-18 11:25:17.354047');
INSERT INTO public.pedidos (id_cliente,id_direccion,metodo_pago,tiempo_entrega,tiempo_estimado_entrega,created_at,updated_at) VALUES
	 (5,2,'MercadoPago',4,5,'2026-03-25 08:16:53.528514','2026-03-25 08:18:02.251527');
INSERT INTO public.productos (nombre,precio,stock,categoria,codigo_barra,created_at,updated_at) VALUES
	 ('Placa de Video NVIDIA RTX 3050',450000.00,8,'Hardware','HW-NV-3050','2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735'),
	 ('Auriculares Inalámbricos JBL Tune 770NC',120000.00,25,'Audio','AUD-JBL-770','2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735'),
	 ('Zapatillas Vans Knu Skool',110000.00,20,'Indumentaria','IND-VAN-KNU','2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735'),
	 ('Monitor Curvo 27 pulgadas',220000.00,12,'Periféricos','PER-MON-27C','2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735'),
	 ('Teclado Mecánico Redragon',110000.00,30,'Periféricos','PER-TEC-RED','2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735'),
	 ('Base Direct Drive Moza R12',800000.00,99,'SimRacing','SR-MOZ-R12','2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735'),
	 ('Procesador AMD Ryzen 7 5700X',5000.00,95,'Hardware','HW-AMD-5700X','2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735'),
	 ('Volante Logitech G29',500000.00,5,'SimRacing','SR-LOG-G29','2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735'),
	 ('Soporte Riser PCIe 4.0',1500.00,18,'Accesorios','ACC-PCI-40','2026-03-09 12:42:26.964735','2026-03-09 12:42:26.964735'),
	 ('Escritorio Piola',8000.00,10,'Muebleria','1234567','2026-03-09 12:42:26.964735','2026-03-18 11:19:51.047676');
INSERT INTO public.productos (nombre,precio,stock,categoria,codigo_barra,created_at,updated_at) VALUES
	 ('Mousepad Homero',10000.00,50,'Accesorios','ASXD-165-AS','2026-03-31 08:54:42.953551',NULL),
	 ('Juego de Ajedrez',50000.00,4,'','NU OAN U85','2026-03-31 09:18:57.03676',NULL);
