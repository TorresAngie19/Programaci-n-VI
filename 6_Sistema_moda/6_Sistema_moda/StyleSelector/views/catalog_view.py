# views/catalog_view.py
import flet as ft
from data.productos import productos

def catalog_view(page: ft.Page, cerrar_sesion):
    
    # Variables de estado
    categoria_seleccionada = "Todas"
    productos_filtrados = productos.copy()
    
    # Obtener todas las categorías únicas
    todas_categorias = ["Todas"] + sorted(list(set(p["categoria"] for p in productos)))
    
    # Mapeo de EMOJIS
    emojis_categorias = {
        "Todas": "📦",
        "Pantalón": "👖",
        "Vestidos": "👗",
        "Blusas": "👚",
        "Camisas": "👔",
        "Shorts": "🩳",
        "Faldas": "👗",
        "Abrigos": "🧥",
        "Calzado": "👠",
        "Bolsos": "👜",
        "Mochilas": "🎒",
        "Sombreros": "👒",
        "Accesorios": "💎"
    }
    
    # Referencias para componentes dinámicos
    contenedor_productos = ft.Ref[ft.Container]()
    contador_categoria = ft.Ref[ft.Text]()
    
    def handle_cerrar_sesion(e):
        """Manejar el cierre de sesión"""
        page.dialog = None
        cerrar_sesion(e)
    
    def filtrar_por_categoria(categoria):
        """Filtrar productos por categoría"""
        nonlocal categoria_seleccionada, productos_filtrados
        
        categoria_seleccionada = categoria
        
        if categoria == "Todas":
            productos_filtrados = productos.copy()
        else:
            productos_filtrados = [p for p in productos if p["categoria"] == categoria]
        
        # Actualizar contador
        if contador_categoria.current:
            contador_categoria.current.value = f"{emojis_categorias.get(categoria, '👗')} {categoria}: {len(productos_filtrados)} productos"
        
        # Actualizar productos
        if contenedor_productos.current:
            contenedor_productos.current.content = crear_tarjetas_productos()
        
        page.update()
    
    def crear_filtro_rapido():
        """Crear filtro rápido de categorías VISIBLE AL ENTRAR"""
        # Crear botones para TODAS las categorías en un grid
        botones_categorias = []
        for categoria in todas_categorias:
            emoji = emojis_categorias.get(categoria, "📁")
            botones_categorias.append(
                ft.Container(
                    content=ft.ElevatedButton(
                        f"{emoji} {categoria}",
                        on_click=lambda e, cat=categoria: filtrar_por_categoria(cat),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.PINK_500 if categoria == categoria_seleccionada else ft.Colors.PINK_100,
                            color=ft.Colors.WHITE if categoria == categoria_seleccionada else ft.Colors.PINK_700,
                            padding=ft.padding.symmetric(horizontal=15, vertical=10),
                            shape=ft.RoundedRectangleBorder(radius=10)
                        )
                    ),
                    margin=ft.margin.all(3)
                )
            )
        
        return ft.Container(
            content=ft.Column([
                # Título del filtro
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.FILTER_ALT, color=ft.Colors.PINK_500),
                        ft.Text(
                            "Filtrar por categoría",
                            size=16,
                            weight="bold",
                            color=ft.Colors.PINK_700
                        )
                    ], spacing=10),
                    padding=ft.padding.only(bottom=10)
                ),
                
                # Botones de categorías en grid
                ft.Container(
                    content=ft.Row(
                        botones_categorias,
                        wrap=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=5,
                        run_spacing=5
                    ),
                    padding=ft.padding.symmetric(vertical=5)
                ),
                
                # Línea divisoria
                ft.Divider(height=1, color=ft.Colors.PINK_200),
            ]),
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
            bgcolor=ft.Colors.WHITE
        )
    
    def crear_tarjeta_producto(producto):
        """Crear una tarjeta individual para un producto"""
        # Color diferente para cada categoría
        colores_categoria = {
            "Vestidos": ft.Colors.PINK_100,
            "Blusas": ft.Colors.PINK_50,
            "Camisas": ft.Colors.PINK_100,
            "Pantalón": ft.Colors.PINK_50,
            "Shorts": ft.Colors.PINK_100,
            "Faldas": ft.Colors.PINK_50,
            "Abrigos": ft.Colors.PINK_100,
            "Calzado": ft.Colors.PINK_100,
            "Bolsos": ft.Colors.PINK_50,
            "Mochilas": ft.Colors.PINK_100,
            "Sombreros": ft.Colors.PINK_50,
            "Accesorios": ft.Colors.PINK_100
        }
        
        color_fondo = colores_categoria.get(producto["categoria"], ft.Colors.PINK_50)
        
        return ft.Card(
            elevation=5,
            content=ft.Container(
                width=190,
                height=300,
                bgcolor=color_fondo,
                border_radius=ft.border_radius.all(12),
                content=ft.Column([
                    # Imagen del producto
                    ft.Container(
                        content=ft.Image(
                            src=producto["imagen"],
                            width=170,
                            height=140,
                            fit=ft.ImageFit.COVER,
                            border_radius=ft.border_radius.all(10)
                        ),
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(top=10, bottom=5)
                    ),
                    
                    # Información del producto
                    ft.Container(
                        content=ft.Column([
                            # Nombre
                            ft.Text(
                                producto["nombre"],
                                weight="bold",
                                size=13,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                text_align=ft.TextAlign.CENTER,
                                color=ft.Colors.PINK_800
                            ),
                            
                            # Categoría
                            ft.Container(
                                content=ft.Text(
                                    producto["categoria"],
                                    size=11,
                                    color=ft.Colors.PINK_600,
                                    weight="bold"
                                ),
                                bgcolor=ft.Colors.WHITE,
                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                border_radius=ft.border_radius.all(15),
                                margin=ft.margin.symmetric(vertical=5)
                            ),
                            
                            # Precio
                            ft.Text(
                                f"₲{producto['precio']:,}",
                                size=14,
                                weight="bold",
                                color=ft.Colors.PINK_700
                            ),
                        ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=ft.padding.symmetric(horizontal=10),
                        expand=True
                    ),
                    
                    # Botón de favorito
                    ft.Container(
                        content=ft.ElevatedButton(
                            "❤️ Agregar",
                            on_click=lambda e, p=producto: page.go(f"/favoritos?item={p['id']}"),
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.PINK_300,
                                color=ft.Colors.WHITE,
                                padding=ft.padding.symmetric(horizontal=15, vertical=8),
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            icon=ft.Icons.FAVORITE_BORDER,
                            icon_color=ft.Colors.WHITE
                        ),
                        padding=ft.padding.only(bottom=10)
                    )
                ], 
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            )
        )
    
    def crear_tarjetas_productos():
        """Crear todas las tarjetas de productos filtrados"""
        if not productos_filtrados:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.SEARCH_OFF, size=60, color=ft.Colors.PINK_300),
                    ft.Text(
                        "No hay productos en esta categoría",
                        size=16,
                        color=ft.Colors.PINK_600,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Prueba con otra categoría",
                        size=14,
                        color=ft.Colors.PINK_500,
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
                padding=50,
                alignment=ft.alignment.center
            )
        
        items = []
        for producto in productos_filtrados:
            items.append(crear_tarjeta_producto(producto))
        
        return ft.Container(
            content=ft.Row(
                items,
                wrap=True,
                alignment=ft.MainAxisAlignment.START,
                spacing=15,
                run_spacing=15
            ),
            padding=ft.padding.only(left=20)
        )
    
    # Crear componentes iniciales
    filtro_rapido = crear_filtro_rapido()
    tarjetas_iniciales = crear_tarjetas_productos()
    
    # Crear la vista con FILTRO ARRIBA VISIBLE
    return ft.View(
        "/catalogo",
        controls=[
            ft.AppBar(
                title=ft.Text("Catálogo de Moda 👗"),
                bgcolor=ft.Colors.PINK_100,
                actions=[
                    ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                text="Dashboard",
                                icon=ft.Icons.HOME,
                                on_click=lambda e: page.go("/dashboard")
                            ),
                            ft.PopupMenuItem(
                                text="Favoritos",
                                icon=ft.Icons.FAVORITE,
                                on_click=lambda e: page.go("/favoritos")
                            ),
                            ft.PopupMenuItem(
                                text="Outfits",
                                icon=ft.Icons.STYLE,
                                on_click=lambda e: page.go("/outfit")
                            ),
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem(
                                text="Cerrar Sesión",
                                icon=ft.Icons.LOGOUT,
                                on_click=handle_cerrar_sesion
                            )
                        ]
                    )
                ]
            ),
            
            # FILTRO VISIBLE INMEDIATAMENTE - SIN DESPLAZAR
            filtro_rapido,
            
            # Contador de productos
            ft.Container(
                content=ft.Text(
                    ref=contador_categoria,
                    value=f"📦 Todas: {len(productos_filtrados)} productos",
                    size=14,
                    weight="bold",
                    color=ft.Colors.PINK_700,
                    text_align=ft.TextAlign.CENTER
                ),
                padding=ft.padding.symmetric(vertical=5),
                alignment=ft.alignment.center
            ),
            
            # Productos - COMENZAN INMEDIATAMENTE DESPUÉS DEL FILTRO
            ft.Container(
                expand=True,
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                content=ft.Column([
                    ft.Container(
                        ref=contenedor_productos,
                        expand=True,
                        content=tarjetas_iniciales,
                        padding=10
                    ),
                    
                    # Pie de página
                    ft.Container(
                        content=ft.Row([
                            ft.ElevatedButton(
                                "🏠 Dashboard",
                                on_click=lambda e: page.go("/dashboard"),
                                icon=ft.Icons.HOME,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.PINK_100,
                                    color=ft.Colors.PINK_700,
                                    padding=ft.padding.symmetric(horizontal=20, vertical=12)
                                )
                            ),
                            ft.ElevatedButton(
                                "❤️ Mis Favoritos",
                                on_click=lambda e: page.go("/favoritos"),
                                icon=ft.Icons.FAVORITE,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.PINK_300,
                                    color=ft.Colors.WHITE,
                                    padding=ft.padding.symmetric(horizontal=20, vertical=12)
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                        padding=ft.padding.only(top=20),
                        alignment=ft.alignment.center
                    )
                ])
            )
        ],
        scroll=ft.ScrollMode.AUTO,
        bgcolor=ft.Colors.WHITE
    )