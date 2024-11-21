import random
import gradio as gr

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

def apicomProcessor(e):    
    #Ésto es como maneja la exepción que recibe:
    print("Except recibido por apicom: ", e)
    if "RUNTIME_ERROR" in str(e):
        resultado = "RUNTIME_ERROR" #api mal construida tiene error.
    elif "PAUSED" in str(e):
        resultado = "PAUSED" 
    elif "The read operation timed out" in str(e): #IMPORTANTE, ESTO TAMBIËN SUCEDE CUANDO LA DESPIERTAS Y ES INSTANTANEO.
        resultado = "STARTING"
    else: 
        resultado = "GENERAL"

    return resultado

def manejadorExcepciones(excepcion):
    #Ésto es que texto despliega ante determinada excepción:
    if excepcion == "PAUSED": 
        info_window = "AI Engine Paused, ready soon."
    elif excepcion == "RUNTIME_ERROR":
        info_window = "Error in AI, please contact Moibe."
    elif excepcion == "STARTING":
        info_window = "Server Powering UP, wait a few seconds and try again."
    else:
        info_window = "Error. No credits were debited."

        return info_window