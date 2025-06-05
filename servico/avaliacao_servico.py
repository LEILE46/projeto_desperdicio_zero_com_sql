from servico.database import get_connection
from models.avaliacao import Avaliacao

def avaliar_usuario(usuario, nota, comentario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO avaliacoes (usuario_id, nota, comentario) VALUES (%s, %s, %s)", (usuario.id, nota, comentario))
    conn.commit()
    cursor.close()
    conn.close()
def listar_avaliacoes():
    conn = get_connection()
    cursor = conn.cursor()  # agora já retorna dicionários
    cursor.execute("SELECT id, usuario_id, nota, comentario FROM avaliacoes ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    avaliacoes = [Avaliacao(
        id_=row['id'],
        usuario_id=row['usuario_id'],
        nota=row['nota'],
        comentario=row['comentario']
    ) for row in rows]

    return avaliacoes