from models.usuario import Usuario
from servico.database import get_connection


def cadastrar_usuario(nome, email, tipo_perfil, localizacao):
  
    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = %s", (email,))
    if cursor.fetchone()[0] > 0:
        cursor.close()
        conn.close()
        return False  


    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, tipo_perfil, localizacao, bloqueado) VALUES (%s, %s, %s, %s, %s)", 
            (nome, email, tipo_perfil, localizacao, False)
        )
        conn.commit()
    except Exception as e:
        cursor.close()
        conn.close()
        print(f"Erro ao cadastrar usuário: {e}")
        return False
    
    cursor.close()
    conn.close()
    return True 

def buscar_usuario_por_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, tipo_perfil, localizacao, bloqueado FROM usuarios WHERE email = %s", (email,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return Usuario(*row)
    return None

def verificar_bloqueio(usuario):
    return usuario.bloqueado