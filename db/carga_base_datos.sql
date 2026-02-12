--SELECCIONA LA BASE DE DATOS
use powerlab;

--MUESTRA LAS TABLAS
show TABLES;

--SELECCIONA Y MUESTRA CADA TABLA
select * FROM producto;
select * FROM usuario;
SELECT * FROM pedido;
SELECT * FROM pedido_detalle;


--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------
--CARGA DE USUARIOS NUEVOS
INSERT INTO usuario(id, nombre, apellido, email, telefono, direccion, pass, tipo_usuario) VALUES
(NULL, "Ignacio", "Ledo", "ignacioledo@uca.edu.ar", "1155244402", "Ibera 2865", "1234", "usuario"), 
(NULL, "Alejo", "Pisani", "alejopisani@uca.edu.ar", "112435432", "St.Thomas 111", "4321", "admin"),
(NULL, "Ivan", "Finamore", "ivanfinamore@uca.edu.ar", "1187453782", "Libertador 111", "0987", "usuario");

INSERT INTO usuario VALUES
(4, "Tomás", "Fernández", "tomas.fernandez@uca.edu.ar", "1112345678", "Avenida 742", "6575", "usuario"),
(5, "Julieta", "Gómez", "julieta.gomez@uca.edu.ar", "1122334455", "San Martín 2045", "8345", "usuario"),
(6, "Mateo", "Martínez", "mateo.martinez@uca.edu.ar", "1133445566", "Belgrano 889", "7658", "usuario"),
(7, "Bianca", "Sosa", "bianca.sosa@uca.edu.ar", "1144556677", "Rivadavia 3012", "6759", "usuario"),
(8, "Joaquín", "Herrera", "joaquin.herrera@uca.edu.ar", "1155667788", "Corrientes 1743", "6765", "usuario"),
(9, "Delfina", "Molina", "delfina.molina@uca.edu.ar", "1166778899", "Castelli 501", "8923", "usuario"),
(10, "Nicolás", "Castro", "nicolas.castro@uca.edu.ar", "1177889900", "Mariano Castex 283", "1549", "usuario");
--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------


--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------
--CARGA DE PRODUCTOS BASE
INSERT INTO producto(id, nombre, marca, descripcion, precio, stock, imagen, categoria, sabor) VALUES
(NULL, "Whey Protein", "Ena", "Whey protein concentrate (WPC): perfil completo de aminoácidos esenciales, brindando la mejor calidad de proteínas para aumentar la energía durante el entrenamiento.", 38900, 50, "https://www.enasport.com/cdn/shop/files/TM_WP_2lbCh.jpg?v=1738759187&width=1200", "proteina", "vainilla"),
(NULL, "Whey Protein", "Ena", "Whey protein concentrate (WPC): perfil completo de aminoácidos esenciales, brindando la mejor calidad de proteínas para aumentar la energía durante el entrenamiento.", 38900, 50, "https://www.enasport.com/cdn/shop/files/TM_WP_2lbCh.jpg?v=1738759187&width=1200", "proteina", "chocolate"),
(NULL, "Whey Protein", "Ena", "Whey protein concentrate (WPC): perfil completo de aminoácidos esenciales, brindando la mejor calidad de proteínas para aumentar la energía durante el entrenamiento.", 38900, 50, "https://www.enasport.com/cdn/shop/files/TM_WP_2lbCh.jpg?v=1738759187&width=1200", "proteina", "cookiescream"),
(NULL, "Whey Protein", "Ena", "Whey protein concentrate (WPC): perfil completo de aminoácidos esenciales, brindando la mejor calidad de proteínas para aumentar la energía durante el entrenamiento.", 38900, 50, "https://www.enasport.com/cdn/shop/files/TM_WP_2lbCh.jpg?v=1738759187&width=1200", "proteina", "strawberry"),
(NULL, "Whey X Pro", "Ena", "Whey X Pro Complex Protein aporta una combinación explosiva de proteínas, creatina, aminoácidos, vitaminas, minerales y antioxidantes, en una nueva fórmula mejorada. Aporta más sabor y una máxima disolución para lograr mejores resultados y la podés consumir antes o después del entrenamiento. Es la proteína de suero más avanzada del mercado.", 45900, 60, "https://www.enasport.com/cdn/shop/files/Whey_xpro_chocolate_d95c5819-be8d-4194-be91-cf9423baaca9.jpg?v=1739376616&width=600", "proteina", "chocolate"),
(NULL, "Whey X Pro", "Ena", "Whey X Pro Complex Protein aporta una combinación explosiva de proteínas, creatina, aminoácidos, vitaminas, minerales y antioxidantes, en una nueva fórmula mejorada. Aporta más sabor y una máxima disolución para lograr mejores resultados y la podés consumir antes o después del entrenamiento. Es la proteína de suero más avanzada del mercado.", 45900, 60, "https://www.enasport.com/cdn/shop/files/Whey_xpro_chocolate_d95c5819-be8d-4194-be91-cf9423baaca9.jpg?v=1739376616&width=600", "proteina", "vainilla"),
(NULL, "Creatina Micronizada", "Ena", "Ena	Desata tu máximo potencial con nuestra Creatina Monohidrato Creapure. Un producto de alta calidad diseñado para optimizar el rendimiento físico de atletas y profesionales del deporte. Con una pureza del 100%, Creapure es reconocida por su excepcional concentración y efectividad. Este suplemento potencia la capacidad muscular, facilitando el desarrollo de fuerza y resistencia.", 38000, 80, "https://www.enasport.com/cdn/shop/files/Creapure200g.png?v=1739376497&width=600", "creatina", "neutro"),
(NULL, "Creatina Micronizada", "Ena", "Ena	Desata tu máximo potencial con nuestra Creatina Monohidrato Creapure. Un producto de alta calidad diseñado para optimizar el rendimiento físico de atletas y profesionales del deporte. Con una pureza del 100%, Creapure es reconocida por su excepcional concentración y efectividad. Este suplemento potencia la capacidad muscular, facilitando el desarrollo de fuerza y resistencia.", 38000, 80, "https://www.enasport.com/cdn/shop/files/Creapure200g.png?v=1739376497&width=600", "creatina", "fruitpunch"),
(NULL, "Enargy Gel + Cafeína (x12)", "Ena", "Ena Energy Gel es un repositor energético con sales de rehidratación creado para el entrenamiento diario y la competencia. Es rico en carbohidratos en un paquete portátil para mejorar resistencia y potencia. Es un suplemento dietario a base de carbohidratos, vitamina C, E y minerales, sin cafeína, que aportan energía en movimiento, ideal para todo trabajo aeróbico.", 13000, 100, "https://www.enasport.com/cdn/shop/files/EnargyGel12V.jpg?v=1731094879&width=600", "energia", "citrus"),
(NULL, "Enargy Gel + Cafeína (x12)", "Ena", "Ena Energy Gel es un repositor energético con sales de rehidratación creado para el entrenamiento diario y la competencia. Es rico en carbohidratos en un paquete portátil para mejorar resistencia y potencia. Es un suplemento dietario a base de carbohidratos, vitamina C, E y minerales, sin cafeína, que aportan energía en movimiento, ideal para todo trabajo aeróbico.", 13000, 100, "https://www.enasport.com/cdn/shop/files/EnargyGel12V.jpg?v=1731094879&width=600", "energia", "uva"),
(NULL, "Enargy Gel + Cafeína (x12)", "Ena", "Ena Energy Gel es un repositor energético con sales de rehidratación creado para el entrenamiento diario y la competencia. Es rico en carbohidratos en un paquete portátil para mejorar resistencia y potencia. Es un suplemento dietario a base de carbohidratos, vitamina C, E y minerales, sin cafeína, que aportan energía en movimiento, ideal para todo trabajo aeróbico.", 13000, 100, "https://www.enasport.com/cdn/shop/files/EnargyGel12V.jpg?v=1731094879&width=600", "energia", "vainilla"),
(NULL, "Pre War", "Ena", "PRE WAR es la siguiente evolución en pre entrenamientos. Diseñado con precisión para desafiar tus límites, favorece la concentración, el aumento de energía, la fuerza, el tamaño muscular y la recuperación. Entrena con nuestro Pre work más completo y con fórmula mejorada con 200mg de cafeína por ingesta.", 28500, 50, "https://www.enasport.com/cdn/shop/products/Prewar_Fruit.jpg?v=1738843059&width=600", "preentreno", "lemonade"),
(NULL, "Pre War", "Ena", "PRE WAR es la siguiente evolución en pre entrenamientos. Diseñado con precisión para desafiar tus límites, favorece la concentración, el aumento de energía, la fuerza, el tamaño muscular y la recuperación. Entrena con nuestro Pre work más completo y con fórmula mejorada con 200mg de cafeína por ingesta.", 28500, 50, "https://www.enasport.com/cdn/shop/products/Prewar_Fruit.jpg?v=1738843059&width=600", "preentreno", "fruitpunch"),
(NULL, "Ultra Mass", "Ena", "Ultra Mass es un alimento natural a base de proteínas de alto valor biológico, carbohidratos, vitaminas, minerales y grasas esenciales. Aumentar el tamaño de la masa muscular requiere del balance entre un entrenamiento duro y una nutrición de calidad.", 30100, 50, "https://www.enasport.com/cdn/shop/files/UltraMass_kilo_vainilla_0f4b58d3-442a-4d75-a89c-fd5a569897b3.jpg?v=1739193562&width=600", "preparacion_peso", "chocolate"),
(NULL, "Ultra Mass", "Ena", "Ultra Mass es un alimento natural a base de proteínas de alto valor biológico, carbohidratos, vitaminas, minerales y grasas esenciales. Aumentar el tamaño de la masa muscular requiere del balance entre un entrenamiento duro y una nutrición de calidad.", 30100, 50, "https://www.enasport.com/cdn/shop/files/UltraMass_kilo_vainilla_0f4b58d3-442a-4d75-a89c-fd5a569897b3.jpg?v=1739193562&width=600", "preparacion_peso", "vainilla"),
(NULL, "Pancakes", "Granger", "15g de proteina por porcion, ricos en proteina de huevo conocida por sus beneficios para la salud. Con un perfil completo de aminoacidos, efectivos en el crecimiento y mantenimiento saludable de la masa muscular.", 12000, 120, "https://acdn-us.mitiendanube.com/stores/001/681/926/products/pancakes-chocolate-1-5c5f11af80cba7564617163828431483-480-0.png", "recetas", "chocolate"),
(NULL, "Pancakes", "Granger", "15g de proteina por porcion, ricos en proteina de huevo conocida por sus beneficios para la salud. Con un perfil completo de aminoacidos, efectivos en el crecimiento y mantenimiento saludable de la masa muscular.", 12000, 120, "https://acdn-us.mitiendanube.com/stores/001/681/926/products/pancakes-chocolate-1-5c5f11af80cba7564617163828431483-480-0.png", "recetas", "vainilla"),
(NULL, "Keto Pancakes", "Granger", "4g de carbohidratos por porción, siendo muy efectivo en mantener tus objetivos nutricionales. Además son una fuente excelente de proteínas y son aptos para dieta cetogenica.", 12000, 120, "https://acdn-us.mitiendanube.com/stores/001/681/926/products/ketopancakes-vainilla200g-1-6e2bd4f0d7c1adf8d217506903942213-480-0.jpg", "recetas", "vainilla"),
(NULL, "Cupcakes", "Granger", "15g de proteína por porción con un perfil completo de aminoácidos. Forma practica y rápida de ingerir proteínas, no contiene azucares agregados ni grasas, por lo que no solo te ayuda a crear musculo y a mantenerlo, si no también a quemar grasas gracias a su bajo contenido energético.", 11500, 120, "https://acdn-us.mitiendanube.com/stores/001/681/926/products/cupcakes-31d6919edf69b450f917163829823000-480-0.png", "recetas", "chocolate"),
(NULL, "Creatina Monohidratada", "Star Nutrition", "La creatina micronizada es la unión de tres aminoácidos que ofrece mayores ventajas que la creatina normal, mejorando su asimilación. La creatina monohidrato es recomendada durante un plan de entrenamiento para aumentar la fuerza, resistencia y recuperación.", 31800, 70, "https://starnutrition.com.ar/cdn/shop/files/CreatineM-300g.png?v=1718218487&width=750", "creatina", "neutro");
--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------


--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------
--CARGA DE PEDIDOS
INSERT INTO pedido(id, id_usuario, fecha_hora, estado, total) VALUES
(NULL, 1, '2025-01-04 14:30:00', "entregado", 200000),
(NULL, 2, '2025-06-06 16:30:00', "en_proceso", 56500),
(NULL, 3, '2025-8-05 22:30:00', "carrito", 13000);

INSERT INTO pedido(id, id_usuario, fecha_hora, estado, total) VALUES
(4, 4, '2025-01-15 10:23:45', "no_pagado", 84000),
(5, 5, '2025-02-28 19:05:10', "entregado", 95400),
(6, 6, '2025-03-12 08:45:00', "carrito", 78000),
(7, 7, '2025-04-01 14:55:30', "en_proceso", 28500),
(8, 8, '2025-05-09 22:10:00', "en_proceso", 60200),
(9, 9, '2025-06-01 16:30:25', "carrito", 137700),
(10, 10, '2025-06-20 07:50:55', "carrito", 46000);

UPDATE pedido SET total = 183600 WHERE id = 1;
UPDATE pedido SET total = 76000 WHERE id = 2;
UPDATE pedido SET total = 194500 WHERE id = 3;
--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------


--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------
--CARGA DE DETALLES DE PEDIDO
INSERT INTO pedido_detalle(id, id_pedido, id_producto, cantidad, precio_uni) VALUES
(NULL, 1, 5, 4, 45900),
(NULL, 2, 8, 2, 38000),
(NULL, 3, 2, 5, 38900);

INSERT INTO pedido_detalle(id, id_pedido, id_producto, cantidad, precio_uni) VALUES
(4, 4, 17, 7, 12000),
(5, 5, 20, 3, 31800),
(6, 6, 11, 6, 13000),
(7, 7, 12, 1, 28500),
(8, 8, 14, 2, 30100),
(9, 9, 5, 3, 45900),
(10, 10, 19, 4, 11500);
--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------

SELECT usuario.nombre, 
usuario.apellido, 
pedido.fecha_hora
FROM pedido
INNER JOIN usuario ON pedido.id_usuario = usuario.id;
