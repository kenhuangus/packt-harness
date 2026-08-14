import packt_jwt_runtime

def validate(token):
    return packt_jwt_runtime.decode(token)
