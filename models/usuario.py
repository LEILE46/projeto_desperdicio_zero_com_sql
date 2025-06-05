class Usuario:
    def __init__(self, id, nome, email, tipo_perfil, localizacao, bloqueado):
        self.id = id
        self.nome = nome
        self.email = email
        self.tipo_perfil = tipo_perfil
        self.localizacao = localizacao
        self.bloqueado = bloqueado