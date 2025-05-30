class Retirada:
    def __init__(self, id_, usuario_id, alimento, data, local):
        self.id = id_
        self.usuario_id = usuario_id
        self.alimento = alimento  # Agora, alimento é um objeto Alimento completo
        self.data = data
        self.local = local

    
