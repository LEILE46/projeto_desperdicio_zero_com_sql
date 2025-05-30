class Usuario:
    def __init__(self, id_, nome, email, tipo_perfil, localizacao, bloqueado=False):
        self.id = id_
        self.nome = nome
        self.email = email
        self.tipo_perfil = tipo_perfil
        self.localizacao = localizacao
        self.bloqueado = bloqueado