import random
import gradio as gr
import globales
from huggingface_hub import HfApi
import bridges

def theme_selector():
    temas_posibles = [
        gr.themes.Base(),
        gr.themes.Default(),
        gr.themes.Glass(),
        gr.themes.Monochrome(),
        gr.themes.Soft()
    ]
    tema = random.choice(temas_posibles)
    return tema

def initAPI():
    
    global result_from_initAPI

    try:
        repo_id = globales.api
        api = HfApi(token=bridges.hug)
        runtime = api.get_space_runtime(repo_id=repo_id)
        print("Stage: ", runtime.stage)
        #"RUNNING_BUILDING", "APP_STARTING", "SLEEPING", "RUNNING", "PAUSED", "RUNTIME_ERROR"
        if runtime.stage == "SLEEPING":
            api.restart_space(repo_id=repo_id)
            print("Desperando")
        print("Hardware: ", runtime.hardware)
        result_from_initAPI = runtime.stage

    except Exception as e:
        #Creo que ya no debería de llegar aquí.
        print("No api, encendiendo: ", e)
        result_from_initAPI = str(e)    
    
    return result_from_initAPI

def titulizaExcepDeAPI(e):   
    print("El e recibido por tituliza es: ", e) 
     #Resume una excepción a un título manejable.
    if "RUNTIME_ERROR" in str(e):
        resultado = "RUNTIME_ERROR" #api mal construida tiene error.
    elif "PAUSED" in str(e):
        resultado = "PAUSED" 
    elif "The read operation timed out" in str(e): #IMPORTANTE, ESTO TAMBIÉN SUCEDE CUANDO LA DESPIERTAS Y ES INSTANTÁNEO.
        resultado = "STARTING"
    elif "GPU quota" in str(e): 
        resultado = recortadorQuota(str(e)) #Cuando se trata de quota regresa el resultado completo convertido a string.
    elif "handshake operation timed out" in str(e):
        resultado = "HANDSHAKE_ERROR"
    elif "File None does not exist on local filesystem and is not a valid URL." in str(e):
        resultado = "NO_FILE"
    #A partir de aquí son casos propios de cada aplicación.
    #image-blend
    elif "no-source-face" in str(e):
        resultado = "NO_FACE"
    #splashmix
    elif "Unable to detect a face" in str(e):
        resultado = "NO_FACE"
    else: 
        resultado = "GENERAL"

    return resultado

def recortadorQuota(texto_quota):
    # Encontrar el índice de inicio (después de "exception:")
    indice_inicio = texto_quota.find("exception:") + len("exception:")
    # Encontrar el índice de final (antes de "<a")
    indice_final = texto_quota.find("<a")
    
    if indice_final == -1: #Significa que no encontró el texto "<a" entonces buscará Sign-Up.
        indice_final = texto_quota.find("Sign-up")
    
    #Extraer la subcadena
    subcadena = texto_quota[indice_inicio:indice_final]

    #Y si el objetivo es nunca desplegar el texto Hugging Face, éste es el plan de escape final.
    if "Hugging" in subcadena: 
        nuevo_mensaje = "Your quota is exceeded, try again in few hours please."
        return nuevo_mensaje
    else:
        print("El recorte quedó: ")
        print(subcadena)
    
    return subcadena