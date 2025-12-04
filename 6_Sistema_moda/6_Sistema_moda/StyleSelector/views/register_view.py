# views/register_view.py
import flet as ft
import threading
import time
from database import crear_usuario

def register_view(page: ft.Page, on_registro_exitoso):
    """Vista para registrar nueva cuenta"""
    
    # Campos del formulario
    username_field = ft.TextField(
        label="Nombre de usuario",
        hint_text="Mínimo 3 caracteres",
        prefix_icon=ft.Icons.PERSON_ADD,
        width=300,
        autofocus=True,
        on_submit=lambda e: crear_cuenta(e)  # Enter en campo de usuario
    )
    
    password_field = ft.TextField(
        label="Contraseña",
        hint_text="Mínimo 6 caracteres",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
        width=300,
        on_submit=lambda e: crear_cuenta(e)  # Enter en campo de contraseña
    )
    
    confirm_field = ft.TextField(
        label="Confirmar contraseña",
        hint_text="Repite la contraseña",
        prefix_icon=ft.Icons.LOCK_RESET,
        password=True,
        can_reveal_password=True,
        width=300,
        on_submit=lambda e: crear_cuenta(e)  # Enter en campo de confirmación
    )
    
    mensaje_text = ft.Text("", color=ft.Colors.RED, size=12)
    
    def crear_cuenta(e=None):
        """Función para crear nueva cuenta"""
        username = username_field.value.strip()
        password = password_field.value.strip()
        confirm = confirm_field.value.strip()
        
        # Validaciones
        if not username:
            mensaje_text.value = "Por favor, ingresa un nombre de usuario"
            mensaje_text.color = ft.Colors.RED
            page.update()
            return
            
        if len(username) < 3:
            mensaje_text.value = "El usuario debe tener al menos 3 caracteres"
            mensaje_text.color = ft.Colors.RED
            page.update()
            return
        
        if not password:
            mensaje_text.value = "Por favor, ingresa una contraseña"
            mensaje_text.color = ft.Colors.RED
            page.update()
            return
        
        if len(password) < 6:
            mensaje_text.value = "La contraseña debe tener al menos 6 caracteres"
            mensaje_text.color = ft.Colors.RED
            page.update()
            return
        
        if not confirm:
            mensaje_text.value = "Por favor, confirma tu contraseña"
            mensaje_text.color = ft.Colors.RED
            page.update()
            return
        
        if password != confirm:
            mensaje_text.value = "Las contraseñas no coinciden"
            mensaje_text.color =ft.Colors.RED
            page.update()
            return
        
        # Crear usuario en la base de datos
        exito, mensaje = crear_usuario(username, password)
        
        if exito:
            # Mostrar mensaje de éxito
            mensaje_text.value = "¡Cuenta creada exitosamente! ✅"
            mensaje_text.color = ft.Colors.GREEN
            page.update()
            
            # Esperar 2 segundos y volver al login
            def volver_a_login():
                time.sleep(2)
                on_registro_exitoso(username)
            
            threading.Thread(target=volver_a_login, daemon=True).start()
            
        else:
            mensaje_text.value = mensaje
            mensaje_text.color = ft.Colors.RED
            page.update()
    
    def volver_al_login(e):
        """Volver a la vista de login"""
        page.go("/login")
    
    # Crear la vista
    return ft.View(
        "/register",
        [
            ft.AppBar(
                title=ft.Text("Crear Nueva Cuenta 💖"),
                bgcolor=ft.Colors.PINK_100,
                center_title=True
            ),
            ft.Container(
                expand=True,
                padding=40,
                content=ft.Column([
                    ft.Container(
                        content=ft.Image(
                            src="https://cdn-icons-png.flaticon.com/512/3079/3079165.png",
                            width=120,
                            height=120,
                            fit=ft.ImageFit.CONTAIN
                        ),
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(bottom=30)
                    ),
                    ft.Text(
                        "Crear tu cuenta en StyleSelector",
                        size=24,
                        weight="bold",
                        color=ft.Colors.PINK_700,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Únete a nuestra comunidad de moda ✨",
                        size=14,
                        color=ft.Colors.PINK_500,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=30),
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
                                content=confirm_field,
                                alignment=ft.alignment.center
                            ),
                            ft.Container(
                                content=mensaje_text,
                                alignment=ft.alignment.center
                            ),
                            ft.Container(height=25),
                            ft.Container(
                                content=ft.ElevatedButton(
                                    "Crear Cuenta",
                                    on_click=crear_cuenta,
                                    icon=ft.Icons.CHECK_CIRCLE,
                                    width=300,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.PINK_400,
                                        color=ft.Colors.WHITE,
                                        padding=ft.padding.symmetric(vertical=15)
                                    )
                                ),
                                alignment=ft.alignment.center
                            ),
                            ft.Container(height=15),
                            ft.Container(
                                content=ft.TextButton(
                                    "← Volver al inicio de sesión",
                                    on_click=volver_al_login,
                                    icon=ft.Icons.ARROW_BACK
                                ),
                                alignment=ft.alignment.center
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
                        "Tu información está segura con nosotros 🔒",
                        size=11,
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