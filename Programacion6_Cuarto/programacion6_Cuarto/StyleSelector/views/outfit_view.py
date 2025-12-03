# views/outfit_view.py
import flet as ft

def outfit_view(page: ft.Page, outfits_guardados=None, guardar_persistencia=None, cerrar_sesion=None):
    if outfits_guardados is None:
        outfits_guardados = []
    
    def handle_cerrar_sesion(e):
        """Manejar el cierre de sesión"""
        page.dialog = None
        cerrar_sesion(e)
    
    # Función para eliminar outfit directamente
    def eliminar_outfit(e, outfit_index):
        print(f"Intentando eliminar outfit {outfit_index}")
        
        if 0 <= outfit_index < len(outfits_guardados):
            # Eliminar el outfit
            outfits_guardados.pop(outfit_index)
            
            # Guardar cambios
            if guardar_persistencia:
                favoritos_actuales = page.client_storage.get("favoritos") or []
                guardar_persistencia(favoritos_actuales, outfits_guardados)
            
            # Mostrar mensaje
            snack = ft.SnackBar(
                content=ft.Text("Outfit eliminado correctamente 🗑️"),
                duration=2000,
                bgcolor=ft.Colors.PINK_800
            )
            page.overlay.append(snack)
            page.update()
            snack.open = True
            page.update()
            
            # Recargar vista
            page.views.clear()
            page.views.append(outfit_view(page, outfits_guardados, guardar_persistencia, cerrar_sesion))
            page.update()
        else:
            print(f"Índice inválido: {outfit_index}")

    # Si no hay outfits
    if not outfits_guardados:
        return ft.View(
            "/outfit",
            [
                ft.AppBar(
                    title=ft.Text("Outfits Guardados 👗"),
                    bgcolor=ft.Colors.PINK_100,
                    center_title=True,
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
                                    text="Favoritos",
                                    icon=ft.Icons.FAVORITE,
                                    on_click=lambda e: page.go("/favoritos")
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
                    content=ft.Column([
                        ft.Icon(
                            ft.Icons.SENTIMENT_DISSATISFIED, 
                            size=80, 
                            color=ft.Colors.PINK_300
                        ),
                        ft.Text(
                            "Aún no tienes outfits guardados 💬", 
                            size=20, 
                            text_align=ft.TextAlign.CENTER,
                            weight="bold",
                            color=ft.Colors.PINK_700
                        ),
                        ft.Text(
                            "Ve a favoritos y guarda tu primer outfit!",
                            size=14,
                            color=ft.Colors.PINK_500,
                            text_align=ft.TextAlign.CENTER
                        )
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                    spacing=25,
                    alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=40,
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton(
                            "Volver a Favoritos", 
                            on_click=lambda e: page.go("/favoritos"),
                            icon=ft.Icons.ARROW_BACK,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.PINK_100,
                                color=ft.Colors.PINK_700,
                                padding=ft.padding.symmetric(horizontal=25, vertical=12)
                            )
                        ),
                        ft.ElevatedButton(
                            "Volver al Dashboard", 
                            on_click=lambda e: page.go("/dashboard"),
                            icon=ft.Icons.HOME,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.PINK_300,
                                color=ft.Colors.WHITE,
                                padding=ft.padding.symmetric(horizontal=25, vertical=12)
                            )
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                    padding=20
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

    # Crear tarjetas de outfits
    outfit_cards = []
    
    for idx, outfit in enumerate(outfits_guardados):
        # Crear la tarjeta
        tarjeta = ft.Card(
            elevation=8,
            content=ft.Container(
                padding=20,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[ft.Colors.PINK_50, ft.Colors.PINK_100]
                ),
                border_radius=ft.border_radius.all(15),
                content=ft.Column([
                    # Header con título y botón de eliminar
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    f"Outfit #{idx + 1}", 
                                    weight="bold", 
                                    size=18,
                                    color=ft.Colors.PINK_800
                                ),
                                ft.Text(
                                    f"{len(outfit)} prendas · ₲{sum(p['precio'] for p in outfit):,}",
                                    size=12,
                                    color=ft.Colors.PINK_600
                                )
                            ], spacing=2),
                            expand=True
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINED,
                            icon_color=ft.Colors.RED,
                            icon_size=24,
                            tooltip="Eliminar outfit",
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            on_click=lambda e, index=idx: eliminar_outfit(e, index)
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    
                    # Línea divisoria
                    ft.Divider(height=1, color=ft.Colors.PINK_200),
                    
                    # Imágenes de las prendas
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Card(
                                    elevation=4,
                                    content=ft.Container(
                                        width=95,
                                        padding=8,
                                        border_radius=ft.border_radius.all(10),
                                        bgcolor=ft.Colors.WHITE,
                                        content=ft.Column([
                                            ft.Image(
                                                src=p["imagen"], 
                                                width=80, 
                                                height=80, 
                                                fit=ft.ImageFit.COVER,
                                                border_radius=ft.border_radius.all(8)
                                            ),
                                            ft.Container(height=5),
                                            ft.Text(
                                                p["nombre"], 
                                                size=10, 
                                                text_align=ft.TextAlign.CENTER,
                                                weight="bold",
                                                color=ft.Colors.PINK_800
                                            ),
                                            ft.Text(
                                                f"₲{p['precio']:,}", 
                                                size=9, 
                                                color=ft.Colors.PINK_600,
                                                text_align=ft.TextAlign.CENTER
                                            )
                                        ], 
                                        spacing=3, 
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        alignment=ft.MainAxisAlignment.CENTER
                                        )
                                    )
                                )
                            ) for p in outfit
                        ], 
                        wrap=True, 
                        alignment=ft.MainAxisAlignment.CENTER,
                        scroll=ft.ScrollMode.AUTO
                        ),
                        padding=ft.padding.only(top=15)
                    )
                ], spacing=12)
            ),
            margin=ft.margin.only(bottom=20)
        )
        
        outfit_cards.append(tarjeta)

    return ft.View(
        "/outfit",
        [
            ft.AppBar(
                title=ft.Text("Outfits Guardados 👗"),
                bgcolor=ft.Colors.PINK_100,
                center_title=True,
                actions=[
                    ft.Container(
                        content=ft.Container(
                            content=ft.Text(
                                f"{len(outfits_guardados)}", 
                                size=14, 
                                weight="bold",
                                color=ft.Colors.WHITE
                            ),
                            bgcolor=ft.Colors.PINK_500,
                            border_radius=ft.border_radius.all(10),
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            alignment=ft.alignment.center
                        ),
                        padding=15
                    ),
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
                                text="Favoritos",
                                icon=ft.Icons.FAVORITE,
                                on_click=lambda e: page.go("/favoritos")
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
                padding=ft.padding.symmetric(horizontal=20, vertical=15),
                content=ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                "Tus Outfits Guardados 💖", 
                                size=22, 
                                weight="bold",
                                color=ft.Colors.PINK_700,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Text(
                                "Todos tus conjuntos favoritos en un solo lugar",
                                size=14,
                                color=ft.Colors.PINK_500,
                                text_align=ft.TextAlign.CENTER
                            )
                        ], spacing=5),
                        padding=ft.padding.only(bottom=20)
                    ),
                    *outfit_cards
                ], 
                scroll=ft.ScrollMode.AUTO,
                spacing=10
                )
            ),
            ft.Container(
                content=ft.Row([
                    ft.ElevatedButton(
                        "Volver a Favoritos", 
                        on_click=lambda e: page.go("/favoritos"),
                        icon=ft.Icons.ARROW_BACK,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.PINK_100,
                            color=ft.Colors.PINK_700,
                            padding=ft.padding.symmetric(horizontal=25, vertical=12)
                        )
                    ),
                    ft.ElevatedButton(
                        "Volver al Dashboard", 
                        on_click=lambda e: page.go("/dashboard"),
                        icon=ft.Icons.HOME,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.PINK_300,
                            color=ft.Colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=25, vertical=12)
                        )
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                padding=20,
                bgcolor=ft.Colors.PINK_50
            )
        ],
        bgcolor=ft.Colors.WHITE
    )