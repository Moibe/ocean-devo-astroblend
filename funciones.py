import bridges
import globales
import sulkuPypi
import sulkuFront
import gradio as gr
import gradio_client
import tools

btn_buy = gr.Button("Get Credits", visible=False, size='lg')

#PERFORM es la app INTERNA que llamará a la app externa.
def perform(input1, input2, request: gr.Request):

    tokens = sulkuPypi.getTokens(sulkuPypi.encripta(request.username).decode("utf-8"), globales.env)
    
    #1: Reglas sobre autorización si se tiene el crédito suficiente.
    autorizacion = sulkuPypi.authorize(tokens, globales.work)
    if autorizacion is True:
        try: 
            resultado = mass(input1, input2)
        except Exception as e:            
            info_window, resultado, html_credits = sulkuFront.aError(request.username, tokens, excepcion = tools.titulizaExcepDeAPI(e))
            return resultado, info_window, html_credits, btn_buy       
    else:
        info_window, resultado, html_credits = sulkuFront.noCredit(request.username)
        return resultado, info_window, html_credits, btn_buy
    
    #Primero revisa si es imagen!: 
    if "result.png" in resultado:
        #Si es imagen, debitarás.
        html_credits, info_window = sulkuFront.presentacionFinal(request.username, "debita")
    else: 
        #Si no es imagen es un texto que nos dice algo.
        info_window, resultado, html_credits = sulkuFront.aError(request.username, tokens, excepcion = tools.titulizaExcepDeAPI(resultado))
        return resultado, info_window, html_credits, btn_buy   
    
    # #2: ¿El resultado es debitable?
    # if debit_rules.debita(resultado) == True:
    #     html_credits, info_window = sulkuFront.presentacionFinal(request.username, "debita")
    # else:
    #     html_credits, info_window = sulkuFront.presentacionFinal(request.username, "no debita") 
            
    #Lo que se le regresa oficialmente al entorno.
    return resultado, info_window, html_credits, btn_buy

#MASS es la que ejecuta la aplicación EXTERNA
def mass(input1, input2):

    api, tipo_api = tools.eligeAPI(globales.seleccion_api)
    print("Una vez elegido API, el tipo api es: ", tipo_api)
    
    client = gradio_client.Client(api, hf_token=bridges.hug)
    imagenSource = gradio_client.handle_file(input1) 
    imagenDestiny = gradio_client.handle_file(input2)

    try:
        
        result = client.predict(imagenSource, imagenDestiny, api_name="/predict")
    
        #(Si llega aquí, debes debitar de la quota, incluso si detecto no-face o algo.)
        if tipo_api == "gratis":
            print("Como el tipo api fue gratis, si debitaremos la quota.")
            sulkuPypi.updateQuota(globales.process_cost)
        #No debitas la cuota si no era gratis, solo aplica para Zero.  

    except Exception as e:
        print("Hubo un errora al ejecutar MASS:", e)
        #Errores al correr la API.
        #La no detección de un rostro es mandado aquí?! Siempre?
        mensaje = tools.titulizaExcepDeAPI(e)        
        return mensaje   
    
    return result