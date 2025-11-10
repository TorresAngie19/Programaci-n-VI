import flet as ft

def home_view(page: ft.Page):
    return ft.View(
        "/",
        [
            ft.Text("👗 Bienvenida a StyleSelector", size=25, weight="bold"),
            ft.Text("Descubre tu estilo y crea tus combinaciones favoritas 💫"),
            ft.ElevatedButton("Ver catálogo", on_click=lambda e: page.go("/catalogo")),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER
    )
