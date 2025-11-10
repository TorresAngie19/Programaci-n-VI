import flet as ft
from data.productos import productos

def catalog_view(page: ft.Page):
    items = []
    for p in productos:
        card = ft.Card(
            content=ft.Container(
                padding=10,
                width=180,
                content=ft.Column([
                    ft.Image(src=p["imagen"], width=150, height=150),
                    ft.Text(p["nombre"], weight="bold"),
                    ft.Text(f"₲{p['precio']:,}"),
                    ft.ElevatedButton(
                        "❤ Favorito", 
                        on_click=lambda e, p=p: page.go(f"/favoritos?item={p['id']}")
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            )
        )
        items.append(card)

    return ft.View(
        "/catalogo",
        controls=[
            ft.AppBar(title=ft.Text("Catálogo"), bgcolor=ft.Colors.PINK_100),
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    [
                        ft.Row(
                            items,
                            wrap=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,  # Desplazamiento vertical si hay overflow
                )
            ),
            ft.ElevatedButton("Volver al inicio", on_click=lambda e: page.go("/"))
        ],
        scroll=ft.ScrollMode.AUTO  # Scroll general también
    )
