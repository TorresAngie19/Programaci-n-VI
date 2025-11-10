import flet as ft
from views.favoritos_view import outfits_guardados

def outfit_view(page: ft.Page):
    outfit_cards = []

    if not outfits_guardados:
        return ft.View(
            "/outfit",
            [
                ft.AppBar(title=ft.Text("Outfits Guardados 👗"), bgcolor=ft.Colors.PINK_100),
                ft.Text("Aún no tienes outfits guardados 💬", size=18),
                ft.ElevatedButton("Volver a Favoritos", on_click=lambda e: page.go("/favoritos"))
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

    # Mostrar cada outfit guardado
    for idx, outfit in enumerate(outfits_guardados, start=1):
        outfit_cards.append(
            ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Column([
                        ft.Text(f"Outfit #{idx}", weight="bold", size=16),
                        ft.Row([
                            ft.Image(src=p["imagen"], width=100, height=100) for p in outfit
                        ], wrap=True, alignment=ft.MainAxisAlignment.CENTER)
                    ])
                )
            )
        )

    return ft.View(
        "/outfit",
        [
            ft.AppBar(title=ft.Text("Outfits Guardados 👗"), bgcolor=ft.Colors.PINK_100),
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(outfit_cards, alignment=ft.MainAxisAlignment.START)
            ),
            ft.ElevatedButton("Volver a Favoritos", on_click=lambda e: page.go("/favoritos"))
        ],
        scroll=ft.ScrollMode.AUTO
    )
