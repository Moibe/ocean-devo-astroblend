def debita(path):
    path_string = str(path)        
    if "no-source-face" not in path_string:    
        return True
    else:
        return False  