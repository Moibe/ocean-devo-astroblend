import bridges
import globales
import requests
from cryptography.fernet import Fernet

base_url = "https://moibe-sulku-fastapi-docker.hf.space/"
work = globales.work

def encripta(username):
    key = bridges.key
    fernet = Fernet(key)
    string_original = username
    string_encriptado = fernet.encrypt(string_original.encode("utf-8"))
    return string_encriptado

def getData(aplicacion):
    method = "getData/"
    params = aplicacion
    api_url = base_url + method + params
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
    else:
        error = f"Error al obtener el elemento todo: {response.status_code}"
        return error    
    return data

def getNovelty(userfile, aplicacion):
    method = "getUserNovelty/"
    params = userfile + "/" + aplicacion
    api_url = base_url + method + params
    response = requests.get(api_url)

    if response.status_code == 200:
        novelty = response.json()
        return novelty              
    else:
        error = f"Error al obtener el elemento todo: {response.status_code}"
        return error    

def getTokens(userfile, env):
    method = "getTokens/"
    params = userfile + "/" + env    
    api_url = base_url + method + params
    response = requests.get(api_url)

    if response.status_code == 200:
        tokens = response.json()
    else:
        error = f"Error al obtener el elemento todo: {response.status_code}"
        return error
    return tokens

def authorize(tokens, work):
    method = "authorize/"
    params = str(tokens) + "/" + work
    api_url = base_url + method + params
    response = requests.get(api_url)

    if response.status_code == 200:
        autorizacion = response.json()
    else:
        error = f"Error al obtener el elemento todo: {response.status_code}"
        return error
    return autorizacion

def debitTokens(userfile, work, env):
    method = "debitTokens/"
    params = userfile + "/" + work + "/" + env
    api_url = base_url + method + params
    response = requests.get(api_url)

    if response.status_code == 200:
        tokens = response.json()
    else:
        error = f"Error al obtener el elemento todo: {response.status_code}"
        return error
    return tokens

def getQuota():

    method = "getQuota/"
    api_url = base_url + method 
    response = requests.get(api_url)

    if response.status_code == 200:
        quota = response.json()
    else:
        error = f"Error al obtener el elemento todo: {response.status_code}"
        return error

    return quota

def getQuotaQ():

    #debitTokens pero con QueryParams, (los query params sirve para ocasiones en los que usas dos de un mismo query param para obtener el resultado de un AND o rangos como...
    #... clima por ejemplo.)
    method = "getQuota?"

    api_url = base_url + method
    response = requests.get(api_url)

    if response.status_code == 200:
        quota = response.json()
    else:
        error = f"Error al obtener el elemento todo: {response.status_code}"
        return error

    return quota

def updateQuota(costo_proceso):
    method = "updateQuota/"
    params = str(costo_proceso)
    api_url = base_url + method + params
    response = requests.get(api_url)

    if response.status_code == 200:
        quota = response.json()
        print("Quota Updated:", quota)
    else:
        error = f"Error al obtener el elemento todo: {response.status_code}"
        return error

    return quota

def updateQuotaQ(costo_proceso):

    #debitTokens pero con QueryParams, (los query params sirve para ocasiones en los que usas dos de un mismo query param para obtener el resultado de un AND o rangos como...
    #... clima por ejemplo.)
    method = "updateQuota?"
    #Y como puedes ver el armado de sus params es dintinto ya que usa ampersand &
    params = "costo_proceso=" + costo_proceso

    api_url = base_url + method + params
    response = requests.get(api_url)

    if response.status_code == 200:
        quota = response.json()
    else:
        error = f"Error al obtener el elemento todo: {response.status_code}"
        return error

    return quota