# views/login_view.py
import flet as ft
from database import verificar_usuario, init_database

def login_view(page: ft.Page, on_login_success):
    """Vista de login"""
    
    # Inicializar base de datos
    init_database()
    
    # Campos para login
    username_field = ft.TextField(
        label="Usuario",
        prefix_icon=ft.Icons.PERSON,
        width=300,
        autofocus=True
    )
    
    password_field = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
        width=300
    )
    
    mensaje_text = ft.Text("", color=ft.Colors.RED, size=12)
    
    # Función para iniciar sesión
    def iniciar_sesion(e):
        username = username_field.value.strip()
        password = password_field.value.strip()
        
        if not username or not password:
            mensaje_text.value = "Por favor, completa todos los campos"
            mensaje_text.color = ft.Colors.RED
            page.update()
            return
        
        # Verificar credenciales
        es_valido, mensaje = verificar_usuario(username, password)
        
        if es_valido:
            # Guardar sesión
            page.client_storage.set("usuario_actual", username)
            mensaje_text.value = f"¡Bienvenida {username}! 💖"
            mensaje_text.color = ft.Colors.GREEN
            page.update()
            
            # Redirigir después de un breve momento
            def redirigir():
                import time
                time.sleep(0.5)
                on_login_success(username)
            
            import threading
            threading.Thread(target=redirigir, daemon=True).start()
            
        else:
            mensaje_text.value = mensaje
            mensaje_text.color = ft.Colors.RED
            page.update()
    
    def ir_a_registro(e):
        """Ir a la vista de registro"""
        page.go("/register")
    
    # Crear la vista principal
    return ft.View(
        "/login",
        [
            ft.AppBar(
                title=ft.Text("StyleSelector 👗"),
                bgcolor=ft.Colors.PINK_100,
                center_title=True
            ),
            ft.Container(
                expand=True,
                content=ft.Column([
                    ft.Container(
                        content=ft.Image(
                            src="https://cdn-icons-png.flaticon.com/512/3079/3079165.png",
                            width=150,
                            height=150,
                            fit=ft.ImageFit.CONTAIN
                        ),
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(bottom=20, top=50)
                    ),
                    ft.Text(
                        "Bienvenida a StyleSelector",
                        size=28,
                        weight="bold",
                        color=ft.Colors.PINK_700,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Tu asistente personal de moda 💫",
                        size=16,
                        color=ft.Colors.PINK_500,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=40),
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=username_field,
                                alignment=ft.alignment.center
                            ),
                            ft.Container(
                                content=password_field,
                                alignment=ft.alignment.center
                            ),
                            ft.Container(
                                content=mensaje_text,
                                alignment=ft.alignment.center
                            ),
                            ft.Container(height=20),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    "Iniciar Sesión",
                                    on_click=iniciar_sesion,
                                    icon=ft.Icons.LOGIN,
                                    width=300,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.PINK_300,
                                        color=ft.Colors.WHITE,
                                        padding=ft.padding.symmetric(vertical=15)
                                    )
                                ),
                                alignment=ft.alignment.center
                            ),
                            ft.Container(height=10),
                            ft.TextButton(
                                "¿No tienes cuenta? Regístrate aquí",
                                on_click=ir_a_registro,
                                icon=ft.Icons.PERSON_ADD
                            )
                        ]),
                        padding=30,
                        border_radius=ft.border_radius.all(20),
                        bgcolor=ft.Colors.PINK_50,
                        width=400,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(height=30),
                    ft.Text(
                        "Conéctate para descubrir tu estilo único",
                        size=12,
                        color=ft.Colors.GREY_600,
                        italic=True,
                        text_align=ft.TextAlign.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
                )
            )
        ],
        scroll=ft.ScrollMode.AUTO,
        bgcolor=ft.Colors.WHITE
    )