import globales
import sulkuPypi
import gradio as gr
import gradio_client
import bridges
import tools
import threading


result_from_displayTokens = None

def initAPI():
    #PROCESO1
    print("Estoy en turn on API.")
    try: #No usar si siempre estará prendida.
        client = gradio_client.Client(globales.api, hf_token=bridges.hug)
        terminal = "AI engine ready."
        client = None
    except Exception as e:
        print("No api, encendiendo: ", e)  

def displayTokens(request: gr.Request):
    #PROCESO2
    print("Estoy en displayTokens...")
    novelty = sulkuPypi.getNovelty(sulkuPypi.encripta(request.username).decode("utf-8"), globales.aplicacion)    
    if novelty == "new_user": 
        display = gr.Textbox(visible=False)
    else: 
        tokens = sulkuPypi.getTokens(sulkuPypi.encripta(request.username).decode("utf-8"), globales.env)
        display = visualizar_creditos(tokens, request.username) 

    global result_from_displayTokens
    result_from_displayTokens = display 

    return display

def precarga(request: gr.Request):
    global result_from_displayTokens

    thread1 = threading.Thread(target=initAPI)
    thread2 = threading.Thread(target=displayTokens, args=(request,))

    thread1.start()
    thread2.start()

    thread1.join()  # Espera a que el hilo 1 termine
    thread2.join()  # Espera a que el hilo 2 termine

    return result_from_displayTokens  
  

def visualizar_creditos(nuevos_creditos, usuario):

    html_credits = f"""
    <div>
    <div style="text-align: left;">👤<b>Username: </b> {usuario}</div><div style="text-align: right;">💶<b>Credits Available: </b> {nuevos_creditos}</div>
    </div>
                    """    
     
    return html_credits

#Controla lo que se depliega en el frontend y que tiene que ver con llamados a Sulku.
def noCredit(usuario):
    info_window = "Out of credits..."
    path = 'images/no-credits.png'
    tokens = 0
    html_credits = visualizar_creditos(tokens, usuario)   

    return info_window, path, html_credits

def aError(usuario, tokens, excepcion):
    info_window = tools.manejadorExcepciones(excepcion)
    path = 'images/error.png'
    tokens = tokens
    html_credits = visualizar_creditos(tokens, usuario)   
    return info_window, path, html_credits

def presentacionFinal(usuario, accion):
        
    capsule = sulkuPypi.encripta(usuario).decode("utf-8") #decode es para quitarle el 'b
    
    if accion == "debita":        
        tokens = sulkuPypi.debitTokens(capsule, globales.work, globales.env)
        info_window = "Image ready!"        
    else: 
        info_window = "No face in source path detected."
        tokens = sulkuPypi.getTokens(capsule, globales.env)
    
    html_credits = visualizar_creditos(tokens, usuario)       
    
    return html_credits, info_window