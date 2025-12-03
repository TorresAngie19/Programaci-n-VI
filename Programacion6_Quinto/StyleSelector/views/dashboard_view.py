# views/dashboard_view.py
import flet as ft

def dashboard_view(page: ft.Page, usuario_actual, cerrar_sesion):
    
    def handle_cerrar_sesion(e):
        """Manejar el cierre de sesión"""
        # Limpiar cualquier diálogo abierto
        page.dialog = None
        # Llamar a la función de cerrar sesión
        cerrar_sesion(e)
    
    return ft.View(
        "/dashboard",
        [
            ft.AppBar(
                title=ft.Text(f"StyleSelector 👗"),
                bgcolor=ft.Colors.PINK_100,
                actions=[
                    ft.Row([
                        ft.Text(f"Hola, {usuario_actual}!", size=14, color=ft.Colors.PINK_700),
                        ft.IconButton(
                            icon=ft.Icons.LOGOUT,
                            icon_color=ft.Colors.PINK_700,
                            tooltip="Cerrar Sesión",
                            on_click=handle_cerrar_sesion
                        )
                    ], spacing=5)
                ]
            ),
            ft.Container(
                expand=True,
                padding=40,
                content=ft.Column([
                    ft.Text(
                        "👗 Bienvenida a StyleSelector",
                        size=28,
                        weight="bold",
                        color=ft.Colors.PINK_700,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Descubre tu estilo y crea tus combinaciones favoritas 💫",
                        size=16,
                        color=ft.Colors.PINK_500,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=40),
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.SHOPPING_BAG, size=50, color=ft.Colors.PINK_300),
                                ft.Text("Catálogo", weight="bold", size=16),
                                ft.ElevatedButton(
                                    "Explorar",
                                    on_click=lambda e: page.go("/catalogo"),
                                    icon=ft.Icons.ARROW_FORWARD,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.PINK_200,
                                        padding=ft.padding.symmetric(horizontal=20, vertical=10)
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=20,
                            border_radius=ft.border_radius.all(15),
                            bgcolor=ft.Colors.PINK_50,
                            width=200
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.FAVORITE, size=50, color=ft.Colors.PINK_300),
                                ft.Text("Favoritos", weight="bold", size=16),
                                ft.ElevatedButton(
                                    "Ver",
                                    on_click=lambda e: page.go("/favoritos"),
                                    icon=ft.Icons.ARROW_FORWARD,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.PINK_200,
                                        padding=ft.padding.symmetric(horizontal=20, vertical=10)
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=20,
                            border_radius=ft.border_radius.all(15),
                            bgcolor=ft.Colors.PINK_50,
                            width=200
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=30),
                    ft.Container(height=30),
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.STYLE, size=50, color=ft.Colors.PINK_300),
                                ft.Text("Outfits", weight="bold", size=16),
                                ft.ElevatedButton(
                                    "Ver guardados",
                                    on_click=lambda e: page.go("/outfit"),
                                    icon=ft.Icons.ARROW_FORWARD,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.PINK_200,
                                        padding=ft.padding.symmetric(horizontal=20, vertical=10)
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=20,
                            border_radius=ft.border_radius.all(15),
                            bgcolor=ft.Colors.PINK_50,
                            width=200
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
                )
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        bgcolor=ft.Colors.WHITE
    )