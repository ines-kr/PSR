from posixpath import split
import socket
def main_authentification():
    print("Donner la cle du banque")
    ref = input(">> ") # utilisez raw_input() pour les anciennes versions python
    s.send(b"auth"+ref.encode())
    r = s.recv(9999999)
    print(r)
    return(r,ref)
def main_banque():
    print("choisissez l'operation a executer")
    print("1.consulter la liste des comptes")
    print("2.consulter la facture d'un compte")
    print("3.consulter l'historique des transactions")

    choix=input("valeur de choix")
    if (choix=="1"):
        print("Donner la reference du compte a lister")
        ref = input(">> ") # utilisez raw_input() pour les anciennes versions python
        
        return("liste,"+ref)
    
    elif(choix=="2"):
        ref=input("Donner la reference du compte a afficher la facture")
        return("facture,"+ref)

    elif(choix=="3"):
        ref=input("Donner la reference du compte a afficher l'historique des transactions")
        return("histo,"+ref)
    else: return(-1)
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.1.141", 1111))
    rm=main_authentification()
    print(rm)
    if(rm[0]==b'bank authorized'):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.1.141", 1111))
        request=main_banque()
        s.send(request.encode())
        result = s.recv(9999999)
        text=str(result)
        print(text)
        text=text[2:-1]
        ltext='#'.split(text)
        for i in ltext:
            i='*'.split(i)
        for i in ltext:
            for j in i :
                print(j+"\t")
        
    else:
        print("not authorized")