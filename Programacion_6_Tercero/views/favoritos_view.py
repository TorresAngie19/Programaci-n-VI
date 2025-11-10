import flet as ft
from data.productos import productos

# Listas globales
favoritos = []
outfits_guardados = []  # Nueva lista global

def favoritos_view(page: ft.Page, item_id=None):
    # Añadir producto si viene desde catálogo
    if item_id:
        for p in productos:
            if str(p["id"]) == str(item_id):
                if p not in favoritos:
                    favoritos.append(p)
                break

    # Función para eliminar un favorito
    def eliminar_favorito(e, producto):
        if producto in favoritos:
            favoritos.remove(producto)
        page.views.clear()
        page.views.append(favoritos_view(page))
        page.update()

    # Función para guardar un outfit
    def guardar_outfit(e):
        if favoritos:
            outfits_guardados.append(favoritos.copy())
            mensaje = "Outfit guardado correctamente 💖"
        else:
            mensaje = "No hay prendas seleccionadas para guardar ❌"
        
        # Solución simple y efectiva
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
            ft.AppBar(title=ft.Text("Mis Favoritos 💖"), bgcolor=ft.Colors.PINK_100),
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Row(fav_cards, wrap=True, alignment=ft.MainAxisAlignment.CENTER, spacing=10)
            ),
            ft.Row([
                ft.ElevatedButton("Guardar Outfit 👚👠", on_click=guardar_outfit),
                ft.ElevatedButton("Ver Outfits Guardados", on_click=lambda e: page.go("/outfit")),
                ft.ElevatedButton("Volver al catálogo", on_click=lambda e: page.go("/catalogo"))
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        ],
        scroll=ft.ScrollMode.AUTO
    )