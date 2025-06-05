from models.usuario import Usuario
from servico.database import get_connection

def cadastrar_usuario(nome, email, tipo_perfil, localizacao):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) AS total FROM usuarios WHERE email = %s", (email,))
        resultado = cursor.fetchone()
        if resultado['total'] > 0:
            return False  # usuário já existe

        cursor.execute(
            "INSERT INTO usuarios (nome, email, tipo_perfil, localizacao,bloqueado) VALUES (%s, %s, %s, %s, %s)", 
            (nome, email, tipo_perfil, localizacao, False)
        )
        conn.commit()
        return True

    except:
        return False

    finally:
        cursor.close()
        conn.close()
def buscar_usuario_por_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nome, email, tipo_perfil, localizacao, bloqueado FROM usuarios WHERE email = %s", (email,))
        row = cursor.fetchone()
        if row:
            return Usuario(*row)
        return None
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

