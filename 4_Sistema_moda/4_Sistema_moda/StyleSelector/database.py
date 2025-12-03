# database.py
import sqlite3
import hashlib
import os

def init_database():
    """Inicializar la base de datos y crear tabla de usuarios si no existe"""
    try:
        # Asegurarse de que la base de datos existe
        db_exists = os.path.exists('fashion_app.db')
        
        conn = sqlite3.connect('fashion_app.db')
        cursor = conn.cursor()
        
        # Crear tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear usuario por defecto si no existe
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE username = 'angie'")
        if cursor.fetchone()[0] == 0:
            hashed_password = hashlib.sha256('000111'.encode()).hexdigest()
            cursor.execute(
                "INSERT INTO usuarios (username, password) VALUES (?, ?)",
                ('angie', hashed_password)
            )
            print("✅ Usuario por defecto creado: angie / 000111")
        
        conn.commit()
        conn.close()
        
        if not db_exists:
            print("✅ Base de datos creada exitosamente")
        else:
            print("✅ Base de datos conectada correctamente")
        
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")

def crear_usuario(username, password):
    """Crear un nuevo usuario en la base de datos"""
    try:
        conn = sqlite3.connect('fashion_app.db')
        cursor = conn.cursor()
        
        # Verificar si el usuario ya existe
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE username = ?", (username,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return False, "El usuario ya existe"
        
        # Hash de la contraseña
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Insertar nuevo usuario
        cursor.execute(
            "INSERT INTO usuarios (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        
        conn.commit()
        conn.close()
        return True, "Usuario creado exitosamente"
        
    except sqlite3.IntegrityError:
        return False, "El usuario ya existe"
    except Exception as e:
        return False, f"Error: {str(e)}"

def verificar_usuario(username, password):
    """Verificar credenciales de usuario"""
    try:
        conn = sqlite3.connect('fashion_app.db')
        cursor = conn.cursor()
        
        # Obtener usuario
        cursor.execute("SELECT password FROM usuarios WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        if result is None:
            conn.close()
            return False, "Usuario no encontrado"
        
        # Verificar contraseña
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        if hashed_input == result[0]:
            conn.close()
            return True, "Credenciales válidas"
        else:
            conn.close()
            return False, "Contraseña incorrecta"
            
    except Exception as e:
        return False, f"Error: {str(e)}"