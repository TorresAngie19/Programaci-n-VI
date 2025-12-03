# views/favoritos_view.py
import flet as ft
from data.productos import productos

def favoritos_view(page: ft.Page, item_id=None, favoritos=None, outfits_guardados=None, guardar_persistencia=None, cerrar_sesion=None):
    # Inicializar listas si no vienen del main
    if favoritos is None:
        favoritos = []
    if outfits_guardados is None:
        outfits_guardados = []
    
    # Añadir producto si viene desde catálogo
    if item_id:
        producto_encontrado = None
        for p in productos:
            if str(p["id"]) == str(item_id):
                producto_encontrado = p
                break
        
        if producto_encontrado and producto_encontrado not in favoritos:
            favoritos.append(producto_encontrado)
            # Guardar cambios persistentes
            if guardar_persistencia:
                guardar_persistencia(favoritos, outfits_guardados)

    def handle_cerrar_sesion(e):
        """Manejar el cierre de sesión"""
        page.dialog = None
        cerrar_sesion(e)

    # Función para eliminar un favorito
    def eliminar_favorito(e, producto):
        if producto in favoritos:
            favoritos.remove(producto)
            # Guardar cambios persistentes
            if guardar_persistencia:
                guardar_persistencia(favoritos, outfits_guardados)
        
        # Recargar la vista
        page.views.clear()
        page.views.append(favoritos_view(page, None, favoritos, outfits_guardados, guardar_persistencia, cerrar_sesion))
        page.update()

    # Función para guardar un outfit
    def guardar_outfit(e):
        if favoritos:
            outfits_guardados.append(favoritos.copy())
            # Guardar cambios persistentes
            if guardar_persistencia:
                guardar_persistencia(favoritos, outfits_guardados)
            
            # Mostrar mensaje
            mensaje = "Outfit guardado correctamente 💖"
        else:
            mensaje = "No hay prendas seleccionadas para guardar ❌"
        
        # Mostrar SnackBar
        snack = ft.SnackBar(content=ft.Text(mensaje))
        page.overlay.append(snack)
        page.update()
        snack.open = True
        page.update()

    # Crear tarjetas visuales
    fav_cards = []
    for f in favoritos:
        card = ft.Container(
            width=180,
            height=220,
            margin=5,
            border_radius=ft.border_radius.all(12),
            bgcolor=ft.Colors.PINK_50,
            content=ft.Stack([
                ft.Image(src=f["imagen"], width=180, height=150, fit=ft.ImageFit.COVER),
                ft.Container(
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_color=ft.Colors.RED,
                        on_click=lambda e, f=f: eliminar_favorito(e, f)
                    ),
                    alignment=ft.alignment.top_right
                ),
                ft.Column([
                    ft.Text(f["nombre"], weight="bold", size=14),
                    ft.Text(f"₲{f['precio']:,}", size=12)
                ], alignment=ft.MainAxisAlignment.END, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ])
        )
        fav_cards.append(card)

    return ft.View(
        "/favoritos",
        controls=[
            ft.AppBar(
                title=ft.Text("Mis Favoritos 💖"),
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
                                text="Catálogo",
                                icon=ft.Icons.SHOPPING_BAG,
                                on_click=lambda e: page.go("/catalogo")
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
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Row(fav_cards, wrap=True, alignment=ft.MainAxisAlignment.CENTER, spacing=10)
            ),
            ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Row([
                        ft.ElevatedButton("Guardar Outfit 👚👠", on_click=guardar_outfit),
                        ft.ElevatedButton("Ver Outfits Guardados", on_click=lambda e: page.go("/outfit")),
                        ft.ElevatedButton("Volver al catálogo", on_click=lambda e: page.go("/catalogo"))
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    ft.Container(height=10),
                    ft.Row([
                        ft.ElevatedButton(
                            "Volver al Dashboard",
                            on_click=lambda e: page.go("/dashboard"),
                            icon=ft.Icons.ARROW_BACK,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.PINK_100,
                                color=ft.Colors.PINK_700
                            )
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ])
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )