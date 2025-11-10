import flet as ft

def main(page: ft.Page):
    page.title = "Catálogo de Moda"
    page.theme_mode = "light"
    page.scroll = "auto"

    # Datos de ejemplo
    prendas = [
        {"nombre": "Camiseta Blanca", "precio": "$20", "img": "https://i.imgur.com/uLQYy8r.png"},
        {"nombre": "Pantalón Jeans", "precio": "$40", "img": "https://i.imgur.com/ZP5kJlx.png"},
    ]

    calzados = [
        {"nombre": "Zapatillas Urbanas", "precio": "$50", "img": "https://i.imgur.com/qI6h0ZT.png"},
        {"nombre": "Botines de Cuero", "precio": "$80", "img": "https://i.imgur.com/0Gx1qfE.png"},
    ]

    # Encabezado
    page.add(ft.Text("🛍️ Catálogo de Moda", size=30, weight="bold", color="purple"))

    # Función para generar tarjetas
    def crear_tarjeta(item):
        return ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Image(src=item["img"], width=150, height=150, fit=ft.ImageFit.CONTAIN),
                    ft.Text(item["nombre"], weight="bold"),
                    ft.Text(item["precio"], color="green"),
                ], horizontal_alignment="center"),
            )
        )

    # Mostrar prendas
    page.add(ft.Text("👕 Prendas", size=20, weight="bold"))
    page.add(ft.Row([crear_tarjeta(p) for p in prendas], wrap=True))

    # Mostrar calzados
    page.add(ft.Text("👟 Calzados", size=20, weight="bold"))
    page.add(ft.Row([crear_tarjeta(c) for c in calzados], wrap=True))

ft.app(target=main)

