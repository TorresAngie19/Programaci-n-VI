# views/catalog_view.py
import flet as ft
from data.productos import productos

def catalog_view(page: ft.Page, cerrar_sesion):
    
    def handle_cerrar_sesion(e):
        """Manejar el cierre de sesión"""
        page.dialog = None
        cerrar_sesion(e)
    
    items = []
    for p in productos:
        card = ft.Card(
            content=ft.Container(
                padding=10,
                width=180,
                content=ft.Column([
                    ft.Image(src=p["imagen"], width=150, height=150),
                    ft.Text(p["nombre"], weight="bold", size=12),
                    ft.Text(f"₲{p['precio']:,}", size=11),
                    ft.ElevatedButton(
                        "❤ Favorito", 
                        on_click=lambda e, p=p: page.go(f"/favoritos?item={p['id']}"),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.PINK_200,
                            padding=ft.padding.symmetric(horizontal=10, vertical=5)
                        )
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5)
            )
        )
        items.append(card)

    return ft.View(
        "/catalogo",
        controls=[
            ft.AppBar(
                title=ft.Text("Catálogo de Productos"),
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
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    [
                        ft.Row(
                            items,
                            wrap=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=15
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                )
            ),
            ft.Container(
                padding=10,
                content=ft.Row([
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
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )