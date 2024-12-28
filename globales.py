import gradio as gr

version = "5.3.6"
env = "dev"
aplicacion = "astroblend-dev"
seleccion_api = "eligeAOB" #eligeGratisOCosto , eligeAOB o eligeGratisOCosto
max_size = 20
#Quota o Costo
api_zero = ("Moibe/image-blend", "gratis")
api_cost = ("Moibe/image-blend", "costo")
#A o B
api_a = ("Moibe/image-blend", "gratis")
api_b = ("Moibe/image-blend", "gratis")
#Gratis o Costo
api_gratis = ("Moibe/image-blend", "gratis")
api_costo = ("Moibe/image-blend", "costo")
process_cost = 0


seto = "image-blend"
work = "picswap"
app_path = "/astroblend-dev"
server_port=7870
tema = gr.themes.Base()
flag = "auto"
