# main.py
import flet as ft
from views.login_view import login_view
from views.register_view import register_view
from views.dashboard_view import dashboard_view
from views.catalog_view import catalog_view
from views.favoritos_view import favoritos_view
from views.outfit_view import outfit_view
from database import init_database

def main(page: ft.Page):
    page.title = "StyleSelector"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    
    # Inicializar base de datos
    init_database()
    
    # Verificar si hay usuario logueado
    usuario_actual = page.client_storage.get("usuario_actual")
    
    # Cargar datos persistentes al iniciar
    def cargar_datos_persistentes():
        favoritos = page.client_storage.get("favoritos")
        outfits_guardados = page.client_storage.get("outfits_guardados")
        return favoritos or [], outfits_guardados or []
    
    # Guardar datos persistentes
    def guardar_datos_persistentes(favoritos, outfits_guardados):
        page.client_storage.set("favoritos", favoritos)
        page.client_storage.set("outfits_guardados", outfits_guardados)
    
    # Cargar datos al iniciar la aplicación
    favoritos, outfits_guardados = cargar_datos_persistentes()
    
    def on_login_success(username):
        """Callback cuando el login es exitoso"""
        nonlocal usuario_actual
        usuario_actual = username
        page.go("/dashboard")
    
    def on_registro_exitoso(username):
        """Callback cuando el registro es exitoso"""
        # Volver al login
        page.go("/login")
    
    def cerrar_sesion(e=None):
        """Cerrar sesión del usuario"""
        page.client_storage.remove("usuario_actual")
        page.views.clear()
        page.go("/login")
    
    def route_change(e):
        page.views.clear()
        
        # Rutas públicas (sin necesidad de login)
        if page.route == "/login":
            page.views.append(login_view(page, on_login_success))
            
        elif page.route == "/register":
            page.views.append(register_view(page, on_registro_exitoso))
            
        # Rutas protegidas (requieren login)
        elif page.route == "/dashboard":
            if usuario_actual:
                page.views.append(dashboard_view(page, usuario_actual, cerrar_sesion))
            else:
                page.go("/login")
                
        elif page.route.startswith("/catalogo"):
            if usuario_actual:
                page.views.append(catalog_view(page, cerrar_sesion))
            else:
                page.go("/login")
                
        elif page.route.startswith("/favoritos"):
            if usuario_actual:
                item_id = None
                if "?" in page.route:
                    item_id = page.route.split("=")[-1]
                page.views.append(favoritos_view(page, item_id, favoritos, outfits_guardados, guardar_datos_persistentes, cerrar_sesion))
            else:
                page.go("/login")
                
        elif page.route.startswith("/outfit"):
            if usuario_actual:
                page.views.append(outfit_view(page, outfits_guardados, guardar_datos_persistentes, cerrar_sesion))
            else:
                page.go("/login")
        
        else:
            # Ruta por defecto
            page.go("/login")
        
        page.update()
    
    page.on_route_change = route_change
    
    # Determinar a dónde ir al iniciar
    if usuario_actual:
        page.go("/dashboard")
    else:
        page.go("/login")

ft.app(target=main)