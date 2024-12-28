import ast 
import globales
import sulkuPypi
import tools

def authenticate(username, password):    
    cadena_usuarios = sulkuPypi.getData(globales.aplicacion)    
    lista_usuarios = ast.literal_eval(cadena_usuarios)
    
    for u, p in lista_usuarios:
        if username == u and password == p:
            api, tipo_api = tools.eligeAPI(globales.seleccion_api)                                                                
            return True 
    return False