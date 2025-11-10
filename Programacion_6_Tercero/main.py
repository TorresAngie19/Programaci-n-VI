# Login, Base de datos, categoria
import flet as ft
from views.home_view import home_view
from views.catalog_view import catalog_view
from views.favoritos_view import favoritos_view
from views.outfit_view import outfit_view

def main(page: ft.Page):
    page.title = "StyleSelector"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(home_view(page))
        elif page.route.startswith("/catalogo"):
            page.views.append(catalog_view(page))
        elif page.route.startswith("/favoritos"):
            # Captura del parámetro ?item=id
            item_id = None
            if "?" in page.route:
                item_id = page.route.split("=")[-1]
            page.views.append(favoritos_view(page, item_id))
        elif page.route.startswith("/outfit"):
            page.views.append(outfit_view(page))

        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
