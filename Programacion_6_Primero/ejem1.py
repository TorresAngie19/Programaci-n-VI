import flet as ft

def main(page: ft.Page):
    page.title = "Creador de Outfits"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Datos de ropa
    tops = ["Camisa blanca", "Blusa azul", "Chaqueta negra", "Camiseta roja"]
    bottoms = ["Jeans", "Falda", "Pantalón formal", "Shorts"]
    shoes = ["Zapatillas", "Botas", "Sandalias", "Tacones"]

    # Elementos seleccionados
    selected_top = ft.Text("")
    selected_bottom = ft.Text("")
    selected_shoes = ft.Text("")

    # Imagen o texto de outfit final
    outfit_result = ft.Text("", size=20, weight=ft.FontWeight.BOLD)

    def update_outfit(e):
        outfit_result.value = (
            f"Tu outfit elegido:\n👕 {selected_top.value}\n👖 {selected_bottom.value}\n👟 {selected_shoes.value}"
        )
        page.update()

    # Funciones para selección
    def select_top(e):
        selected_top.value = e.control.value
        update_outfit(e)

    def select_bottom(e):
        selected_bottom.value = e.control.value
        update_outfit(e)

    def select_shoes(e):
        selected_shoes.value = e.control.value
        update_outfit(e)

    # Dropdowns para elegir ropa
    top_dropdown = ft.Dropdown(
        label="Parte superior",
        options=[ft.dropdown.Option(t) for t in tops],
        on_change=select_top
    )

    bottom_dropdown = ft.Dropdown(
        label="Parte inferior",
        options=[ft.dropdown.Option(b) for b in bottoms],
        on_change=select_bottom
    )

    shoes_dropdown = ft.Dropdown(
        label="Calzado",
        options=[ft.dropdown.Option(s) for s in shoes],
        on_change=select_shoes
    )

    # Agregar todos los elementos a la página
    page.add(
        ft.Text("👗 Creador de Outfits", size=30, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        top_dropdown,
        bottom_dropdown,
        shoes_dropdown,
        ft.Divider(),
        outfit_result
    )

ft.app(target=main)
