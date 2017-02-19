def index():
    return dict()

def about():
    return dict()


def postularse():
    return dict()


def user():
    return dict(login=auth.login())

def register():
    return dict(form=auth.register())


