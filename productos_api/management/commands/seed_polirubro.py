"""
Carga datos de ejemplo (categorías, marcas, proveedores y productos) para
probar la app con algo parecido a un polirubro real de Argentina, en vez de
tener que cargar todo a mano desde la app. Por ahora solo productos
envasados/paquetes (nada a granel ni pesable).

Uso:
    python manage.py seed_polirubro

Es idempotente: se puede correr varias veces sin duplicar nada (usa
get_or_create por nombre). No borra ni pisa productos que ya hayas cargado
vos a mano.
"""

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Categoria, Marca, Proveedor, Producto


class Command(BaseCommand):
    help = "Carga categorías, marcas, proveedores y productos de ejemplo (polirubro, Argentina)."

    @transaction.atomic
    def handle(self, *args, **options):
        categorias = self._crear_categorias()
        marcas = self._crear_marcas()
        proveedores = self._crear_proveedores()
        creados = self._crear_productos(categorias, marcas, proveedores)

        self.stdout.write(self.style.SUCCESS(
            f"Listo: {len(categorias)} categorías, {len(marcas)} marcas, "
            f"{len(proveedores)} proveedores, {creados} productos nuevos."
        ))

    def _crear_categorias(self):
        nombres = [
            ("Almacén", "Fideos, arroz, aceite, harina, azúcar, conservas"),
            ("Bebidas", "Gaseosas, aguas, jugos, cervezas"),
            ("Lácteos", "Leche, yogures, quesos envasados"),
            ("Panificados y Galletitas", "Galletitas dulces y saladas, pan de molde"),
            ("Golosinas", "Chocolates, caramelos, alfajores, chicles"),
            ("Snacks", "Papas fritas, palitos, snacks salados"),
            ("Limpieza", "Detergentes, lavandina, limpiadores"),
            ("Perfumería e Higiene", "Jabones, shampoo, desodorantes, pañales"),
            ("Fiambres Envasados", "Fiambres y embutidos envasados al vacío"),
            ("Congelados", "Hamburguesas, papas y otros productos congelados envasados"),
        ]
        resultado = {}
        for nombre, descripcion in nombres:
            cat, _ = Categoria.objects.get_or_create(
                nombre=nombre, defaults={"descripcion": descripcion}
            )
            resultado[nombre] = cat
        return resultado

    def _crear_marcas(self):
        nombres = [
            "Arcor", "Bagley", "Terrabusi", "La Serenísima", "Sancor",
            "Coca-Cola", "Pepsi", "Manaos", "Quilmes",
            "Molinos (Lucchetti)", "Molinos (Matarazzo)", "Ledesma",
            "La Virginia", "Cabrales", "Knorr",
            "Ala", "Skip", "Cif", "Ayudín",
            "Sedal", "Dove", "Suavecitos",
            "Marca del Distribuidor",
        ]
        resultado = {}
        for nombre in nombres:
            marca, _ = Marca.objects.get_or_create(nombre=nombre)
            resultado[nombre] = marca
        return resultado

    def _crear_proveedores(self):
        datos = [
            ("Distribuidora San Martín S.R.L.", "Roberto Gómez", "ventas@distsanmartin.com.ar", "011-4555-1023"),
            ("Mayorista El Progreso", "Laura Fernández", "pedidos@elprogresomayorista.com.ar", "011-4667-8890"),
            ("Distribuidora Norte S.A.", "Diego Alvarez", "contacto@distnorte.com.ar", "0341-455-3321"),
            ("Andina Distribuciones", "Marina Suárez", "info@andinadist.com.ar", "0261-420-7744"),
            ("Comercial del Sur S.R.L.", "Pablo Ríos", "comercial@delsursrl.com.ar", "0291-450-6612"),
        ]
        resultado = {}
        for nombre, contacto, email, telefono in datos:
            prov, _ = Proveedor.objects.get_or_create(
                nombre=nombre,
                defaults={"contacto": contacto, "email": email, "telefono": telefono},
            )
            resultado[nombre] = prov
        return resultado

    def _crear_productos(self, categorias, marcas, proveedores):
        # (nombre, categoria, marca, proveedor, precio_unitario, % ganancia, stock)
        productos = [
            # Almacén
            ("Fideos Tallarín 500g", "Almacén", "Molinos (Matarazzo)", "Distribuidora San Martín S.R.L.", "800.00", "35", 120),
            ("Fideos Moñito 500g", "Almacén", "Molinos (Lucchetti)", "Distribuidora San Martín S.R.L.", "820.00", "35", 90),
            ("Arroz Largo Fino 1kg", "Almacén", "Molinos (Matarazzo)", "Mayorista El Progreso", "1450.00", "30", 80),
            ("Aceite de Girasol 900ml", "Almacén", "Marca del Distribuidor", "Mayorista El Progreso", "2200.00", "28", 60),
            ("Azúcar Blanca 1kg", "Almacén", "Ledesma", "Distribuidora Norte S.A.", "1300.00", "25", 100),
            ("Yerba Mate 1kg", "Almacén", "La Virginia", "Distribuidora Norte S.A.", "3600.00", "30", 70),
            ("Café Molido 250g", "Almacén", "La Virginia", "Distribuidora Norte S.A.", "3100.00", "35", 40),
            ("Puré de Tomate 520g", "Almacén", "Marca del Distribuidor", "Andina Distribuciones", "950.00", "30", 110),
            ("Caldo de Verdura x12", "Almacén", "Knorr", "Comercial del Sur S.R.L.", "1600.00", "32", 55),
            ("Harina 000 1kg", "Almacén", "Marca del Distribuidor", "Mayorista El Progreso", "1050.00", "25", 130),

            # Bebidas
            ("Coca-Cola 1.5L", "Bebidas", "Coca-Cola", "Distribuidora San Martín S.R.L.", "1900.00", "22", 150),
            ("Coca-Cola 500ml", "Bebidas", "Coca-Cola", "Distribuidora San Martín S.R.L.", "1100.00", "25", 200),
            ("Pepsi 1.5L", "Bebidas", "Pepsi", "Distribuidora San Martín S.R.L.", "1750.00", "22", 90),
            ("Agua Mineral sin gas 1.5L", "Bebidas", "Manaos", "Distribuidora Norte S.A.", "900.00", "28", 180),
            ("Jugo Manaos Naranja 1L", "Bebidas", "Manaos", "Distribuidora Norte S.A.", "1300.00", "28", 85),
            ("Cerveza Quilmes 1L retornable", "Bebidas", "Quilmes", "Comercial del Sur S.R.L.", "1600.00", "24", 100),
            ("Cerveza Quilmes Lata 473ml", "Bebidas", "Quilmes", "Comercial del Sur S.R.L.", "1400.00", "24", 140),

            # Lácteos
            ("Leche Entera 1L", "Lácteos", "La Serenísima", "Andina Distribuciones", "1250.00", "20", 160),
            ("Yogur Bebible 1L", "Lácteos", "La Serenísima", "Andina Distribuciones", "1800.00", "25", 70),
            ("Leche Entera 1L", "Lácteos", "Sancor", "Andina Distribuciones", "1200.00", "20", 100),
            ("Queso Cremoso 300g", "Lácteos", "Sancor", "Andina Distribuciones", "3200.00", "30", 45),
            ("Manteca 200g", "Lácteos", "La Serenísima", "Andina Distribuciones", "2100.00", "28", 50),

            # Panificados y Galletitas
            ("Galletitas Criollitas 300g", "Panificados y Galletitas", "Bagley", "Mayorista El Progreso", "1400.00", "32", 95),
            ("Galletitas Rex 190g", "Panificados y Galletitas", "Terrabusi", "Mayorista El Progreso", "1100.00", "32", 120),
            ("Galletitas de Agua Express 250g", "Panificados y Galletitas", "Bagley", "Mayorista El Progreso", "1250.00", "32", 80),
            ("Pan Lactal 500g", "Panificados y Galletitas", "Marca del Distribuidor", "Mayorista El Progreso", "1600.00", "22", 60),

            # Golosinas
            ("Alfajor Bon o Bon", "Golosinas", "Arcor", "Distribuidora San Martín S.R.L.", "700.00", "40", 300),
            ("Chocolate Águila 25g", "Golosinas", "Arcor", "Distribuidora San Martín S.R.L.", "650.00", "40", 250),
            ("Caramelos Media Hora x30", "Golosinas", "Arcor", "Distribuidora San Martín S.R.L.", "2100.00", "35", 60),
            ("Chicles Topline", "Golosinas", "Arcor", "Distribuidora San Martín S.R.L.", "500.00", "40", 200),

            # Snacks
            ("Papas Fritas Lays 100g", "Snacks", "Arcor", "Mayorista El Progreso", "1700.00", "30", 90),
            ("Palitos Salados 100g", "Snacks", "Arcor", "Mayorista El Progreso", "1300.00", "30", 110),

            # Limpieza
            ("Jabón en Polvo Ala 800g", "Limpieza", "Ala", "Comercial del Sur S.R.L.", "2400.00", "26", 70),
            ("Jabón en Polvo Skip 800g", "Limpieza", "Skip", "Comercial del Sur S.R.L.", "2600.00", "26", 55),
            ("Lavandina 1L", "Limpieza", "Ayudín", "Comercial del Sur S.R.L.", "900.00", "28", 100),
            ("Limpiador Líquido Cif 500ml", "Limpieza", "Cif", "Comercial del Sur S.R.L.", "1500.00", "28", 65),

            # Perfumería e Higiene
            ("Shampoo Sedal 340ml", "Perfumería e Higiene", "Sedal", "Andina Distribuciones", "2300.00", "30", 80),
            ("Jabón de Tocador Dove 90g", "Perfumería e Higiene", "Dove", "Andina Distribuciones", "1100.00", "32", 130),
            ("Papel Higiénico Suavecitos x4", "Perfumería e Higiene", "Suavecitos", "Andina Distribuciones", "2000.00", "25", 90),

            # Fiambres Envasados
            ("Jamón Cocido Envasado 150g", "Fiambres Envasados", "Marca del Distribuidor", "Comercial del Sur S.R.L.", "1900.00", "30", 40),
            ("Salchichón Envasado 200g", "Fiambres Envasados", "Marca del Distribuidor", "Comercial del Sur S.R.L.", "2200.00", "30", 35),

            # Congelados
            ("Hamburguesas x4 congeladas", "Congelados", "Marca del Distribuidor", "Distribuidora Norte S.A.", "2800.00", "28", 50),
            ("Papas Congeladas Bastón 1kg", "Congelados", "Marca del Distribuidor", "Distribuidora Norte S.A.", "2300.00", "28", 55),
        ]

        creados = 0
        for nombre, cat_nombre, marca_nombre, prov_nombre, precio_unitario, porcentaje, stock in productos:
            _, fue_creado = Producto.objects.get_or_create(
                nombre=nombre,
                marca=marcas[marca_nombre],
                defaults={
                    "categoria": categorias[cat_nombre],
                    "proveedor": proveedores[prov_nombre],
                    "precio_unitario": Decimal(precio_unitario),
                    "porcentaje_ganancia": Decimal(porcentaje),
                    "stock": stock,
                },
            )
            if fue_creado:
                creados += 1
        return creados
