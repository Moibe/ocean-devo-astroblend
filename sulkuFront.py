import globales
import sulkuPypi
import gradio as gr

def display_tokens(request: gr.Request):
   
    novelty = sulkuPypi.getNovelty(sulkuPypi.encripta(request.username).decode("utf-8"), globales.aplicacion)
    
    if novelty == "new_user": 
        display = gr.Textbox(visible=False)
    else: 
        tokens = sulkuPypi.getTokens(sulkuPypi.encripta(request.username).decode("utf-8"), globales.env)
        display = visualizar_creditos(tokens, request.username)      
    
    return display

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

def presentacionFinal(usuario, accion):
        
    capsule = sulkuPypi.encripta(usuario).decode("utf-8")
    
    if accion == "debita":        
        tokens = sulkuPypi.debitTokens(capsule, globales.work, globales.env)
        info_window = "Image ready!"        
    else: 
        info_window = "No face in source path detected."
        tokens = sulkuPypi.getTokens(capsule)
    
    html_credits = visualizar_creditos(tokens, usuario)       
    
    return html_credits, info_window