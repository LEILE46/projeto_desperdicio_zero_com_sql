
import mysql.connector
from servico.database import get_connection
from models.retirada import Retirada
from servico.alimentos_servicos import buscar_alimento_por_id
def marcar_retirada(usuario, alimento, data, local):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM retiradas WHERE alimento_id = %s AND data = %s", (alimento.id, data))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return None  # já reservado

    cursor.execute(
        "INSERT INTO retiradas (usuario_id, alimento_id, data, local) VALUES (%s, %s, %s, %s)",
        (usuario.id, alimento.id, data, local)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return Retirada(None, usuario.id, alimento.id, data, local)

def listar_retiradas_do_usuario(usuario_logado):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM retiradas WHERE usuario_id = %s", (usuario_logado.id,))
    retiradas_db = cursor.fetchall()

    retiradas = []
    for r in retiradas_db:
        alimento = buscar_alimento_por_id(r[2])  # r[2] é o alimento_id

        # Passando o objeto Alimento completo para a instância de Retirada
        retirada = Retirada(
            id_=r[0],           # id da retirada
            usuario_id=r[1],    # id do usuário
            alimento=alimento,  # Passamos o objeto Alimento completo
            data=r[3],          # data da retirada
            local=r[4]          # local da retirada
        )

        retiradas.append(retirada)

    cursor.close()
    conn.close()

    return retiradas