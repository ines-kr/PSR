import socket

def main_authentification():
    print("Donner la reference de votre compte")
    ref = input(">> ") # utilisez raw_input() pour les anciennes versions python
    s.send(b"auth"+ref.encode())
    r = s.recv(9999999)
    print(r)
    return(r,ref)

def main_client(ref):
    print("choisissez l'operation a executer")
    print("1. operation de depot")
    print("2. operation de retrait")
    choix=input("valeur de choix")
    if (choix=="1"):
        montant=input("saisir le montant a deposer")
        return("depot,"+ref+","+montant)
    
    elif(choix=="2"):
        montant=input("saisir le montant a retirer")
        return("retrait,"+ref+","+montant)
    else: return(-1)

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.1.102", 1111))
    rm=main_authentification()
    print(rm)
    if(rm[0]==b"exist"):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.1.102", 1111))
        request=main_client(rm[1])
        s.send(request.encode())
        result = s.recv(9999999)
        print(result)
    else:
        print("non existant")