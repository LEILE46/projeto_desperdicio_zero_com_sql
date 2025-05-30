def verificar_bloqueio(usuario):

    return getattr(usuario, 'bloqueado', False)