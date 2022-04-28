import math
from multiprocessing.context import set_spawning_popen
from posixpath import split
import re
import socket
import threading
import time, random

mutex = threading.Lock()
def Afficher_liste_comptes(file="histo.txt"):
  f = open(file, "rt")
  tab=[]
  for line in f:
      tab.append(line.split('*'))
  f.close()
  return tab

def Consulter_liste_compte(ref):
  tab=Afficher_liste_comptes()
  compte=""
  for element in tab:
      if(element[0]==ref):
          compte=element
          break
  entete='*'.join(tab[0])
  if(compte==""):
      return(entete+"Compte non existant")
  else:
      compte='*'.join(compte)
      return (entete+compte)
    
def Afficher_facture_compte(file="facture.txt"):
    f = open(file, "rt")
    tab=[]
    for line in f:
        tab.append(line.split('*'))
    f.close()
    return tab

def Consulter_facture_compte(ref):
  tab=Afficher_facture_compte()
  facture=""
  for element in tab:
      if(element[0]==ref):
          facture=element
          break
  entete='*'.join(tab[0])
  if(facture==""):
    return(entete+"#Compte non existant")
  else:
    facture='*'.join(facture)
    return (entete+"#"+facture)

def Afficher_historique_transactions(file="histo.txt"):
  f = open(file, "rt")
  tab=[]
  for line in f:
      tab.append(line.split('*'))
  f.close()
  return tab

def Consulter_historique_transactions(ref):
    tab=Afficher_historique_transactions()
    entete='*'.join(tab[0])
    histo=[]
    for element in tab:
        if(element[0]==ref):
            element='*'.join(element)
            histo.append(element)
    histo='#'.join(histo)
    return (entete+histo)

def entete(file="facture.txt"):
    f = open(file, "rt")
    tab=[]
    for line in f:
        tab.append(line.split("*"))
    f.close()
    return ('*'.join(tab[0]))

def generer_facture(ref,value):
    resultat=""
    accounts=open("comptes.txt","r")
    ac_list_of_lines = accounts.readlines()
    facturedmontant=0
    for i in range(len(ac_list_of_lines)):
        columns=ac_list_of_lines[i].split('*')
        if int(columns[0])==ref:
            if(columns[2]=="Negatif"):
                facturedmontant=value*0.02
            else:
                montant=int(columns[1])
                if ((montant-value)<0 ):
                    facturedmontant=-(montant-value)*0.02

                    print("il faut payer la facture")
                    break
                else:
                    break
    facture=open("facture.txt","r")
    fa_list_of_lines = facture.readlines()

    for i in range(len(fa_list_of_lines)):
        columns=fa_list_of_lines[i].split('*')
        if columns[0]=="\n":
            continue
        if int(columns[0])==ref:
            print(ref,":",facturedmontant)
            columns[1]=math.trunc(facturedmontant + int(columns[1]))
            if (i< len(fa_list_of_lines)-1):
                fa_list_of_lines[i]="{}*{}\n".format(columns[0],columns[1])
                resultat="{}*{}\n".format(columns[0],columns[1])
                facture.close()
            else :
                fa_list_of_lines[i]="{}*{}\n".format(columns[0],columns[1])
                resultat="{}*{}\n".format(columns[0],columns[1])
                facture.close()
            break
    open('facture.txt', 'w').close()
    facture=open("facture.txt","a")
    for i in fa_list_of_lines:
        facture.write(i)
    return resultat

def retrait(ref,montant):
    succes=False
    isNegatife=False
    if montant<0:
        print("echec")
        return False
    if exist_compte(ref):
        resultat=""
        accounts=open("comptes.txt","r")
        ac_list_of_lines = accounts.readlines()
        for i in range(len(ac_list_of_lines)):
            columns=ac_list_of_lines[i].split('*')
            if int(columns[0])==ref:
                if(columns[2]=="Negatif"):
                    isNegatife=True
                    if (int(columns[1])+montant)<=int(columns[3]):
                        resultat=generer_facture(ref,montant)
                        columns[1]=int(columns[1])+montant
                        ac_list_of_lines[i]="{}*{},Negatif,{}".format(columns[0],columns[1],columns[3])
                        accounts.close()
                        succes=True
                        resultat=entete()+resultat
                        break

                        
                if(columns[2]=="Positif"):
                    if (int(columns[1])-montant)>0:
                        columns[1]=int(columns[1])-montant
                        ac_list_of_lines[i]="{}*{},Positif,{}".format(columns[0],columns[1],columns[3])
                        accounts.close()
                        succes=True
                        resultat="succes"
                        break
                    elif abs(int(columns[1])-montant)<= int(columns[3]):
                        resultat=generer_facture(ref,montant)
                        ac_list_of_lines[i]="{}*{},Negatif,{}".format(columns[0],abs(int(columns[1])-montant),columns[3])
                        accounts.close()
                        succes=True
                        isNegatife=True
                        resultat=entete()+resultat
                        break
        open('accounts.txt', 'w').close()  
        accounts=open("comptes.txt","a")
        for i in ac_list_of_lines:
            accounts.write(i)
        history =open("histo.txt",'a') 
        if succes:
            if isNegatife:
                history.write("\n{},retrait,{},succes,Negatif".format(ref,montant))
            else:
                history.write("\n{},retrait,{},succes,Positif".format(ref,montant))
        else:
            resultat="echec"
            if isNegatife:
                history.write("\n{},retrait,{},echec,Negatif".format(ref,montant))
            else:
                history.write("\n{},retrait,{},echec,Positif".format(ref,montant))
        history.close()
        return resultat              
    else:
        return "echec"

def depot(ref,montant):
    result=""
    if(exist_compte(ref)):
        facture=open("facture.txt","r") 
        fa_list_of_lines=facture.readlines()
        facture.close()
        accounts=open("comptes.txt","r")
        ac_list_of_lines=accounts.readlines()
        accounts.close()
        history=open("histo.txt","a")
        for i in range(len(fa_list_of_lines)):
            columns=fa_list_of_lines[i].split('*')
            if int(columns[0])==ref:
                if(int(columns[1])>=montant):
                    columns[1]=int(columns[1])-montant
                    montant=0
                    fa_list_of_lines[i]="{}*{}".format(columns[0],columns[1])
                    result=entete()+columns[0]+"*"+columns[1]
                else:
                    montant-=int(columns[1])
                    columns[1]=0
                    if(i!=len(fa_list_of_lines)-1):
                        fa_list_of_lines[i]="{}*{}\n".format(columns[0],columns[1])
                    else:
                        fa_list_of_lines[i]="{}*{}".format(columns[0],columns[1])
                    result="succes"

                for i in range(len(ac_list_of_lines)):
                    columns=ac_list_of_lines[i].split('*')
                    if int(columns[0])==ref:
                        if(columns[2]=="Negatif"):
                            if  int(columns[1])>montant:
                                columns[1]= int(columns[1])-montant
                                history.write("\n{},depot,{},succes,Negatif".format(columns[0],montant)) 
                                result="succes "+result
                            else:
                                history.write("\n{},depot,{},succes,Positif".format(columns[0],montant)) 
                                columns[1]= montant-int(columns[1])
                                columns[2]=="Positif"
                            
                        else:
                            columns[1]= int(columns[1])+montant
                            history.write("\n{},depot,{},succes,Positif".format(columns[0],montant)) 
                        ac_list_of_lines[i]="{}*{}*{}*{}".format(columns[0],columns[1],columns[2],columns[3])     
        history.close()
        open("comptes.txt",'w').close()  
        open("facture.txt",'w').close() 
        accounts=open("comptes.txt","a")
        factures=open("facture.txt","a")
        for i in ac_list_of_lines:
            accounts.write(i)        
        for i in fa_list_of_lines:
            factures.write(i)
        accounts.close()
        factures.close() 
        return result
    else:
        result="echec d'operation"
        return result

def transaction(tab):
    ref=tab[1]
    type=tab[0]
    val=int(tab[2])
    resultat=""
    if type == 'depot':
        resultat=depot(int(ref),val)
    elif type == 'retrait':
        resultat=retrait(int(ref),val)
    return resultat

def exist_compte(ref):
        text=str(ref)
        text=text[2:-1]
        print(text)
        f=open("comptes.txt","r")
        l=f.readlines()
        exist=False
        for line in l:
            L=list(line.split("*"))
            if (text==L[0]):
                exist=True
        return(exist)
tab=["retrait","1000","10"]
print(transaction(tab))
class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))

    def run(self): 
        print("Connexion de %s %s" % (self.ip, self.port, ))
        r = self.clientsocket.recv(2048)
        print("client de reference", r, "est connecte")
        global mutex
        mutex.acquire()
        time.sleep(random.randint(0, 1))
        if (r[:4]==b"auth"):
            if(r[4:]==b"banque"):
                self.clientsocket.send(b"bank authorized")
            else:
                res=exist_compte(r[4:])
                print(res)
                if(res):
                    self.clientsocket.send(b"exist")
                else:
                    self.clientsocket.send(b"not exist")
        
        elif (r[:5]==b"depot"):
            text=str(r)
            print(r)
            text=text[2:-1]
            text=text.split('*')
            print(text)
            string=text[0]+text[1]+text[2]
            print(string)
            result=transaction(text)
            print(result)
            self.clientsocket.send(result.encode())
        elif (r[:5]==b"liste"):
            text=str(r)
            print("r",r)
            text=text[2:-1]
            text=text.split('*')
            print("text",text)
            string=text[0]+text[1]
            print(string)
            result=Consulter_liste_compte(text[1])
            print(result)
            self.clientsocket.send(result.encode())
        elif (r[:7]==b"facture"):
            text=str(r)
            print("r",r)
            text=text[2:-1]
            text=text.split('*')
            print("text",text)
            string=text[0]+text[1]
            print(string)
            result=Consulter_facture_compte(text[1])
            print(result)
            self.clientsocket.send(result.encode())
        elif (r[:5]==b"histo"):
            text=str(r)
            print("r",r)
            text=text[2:-1]
            text=text.split('*')
            print("text",text)
            string=text[0]+text[1]
            print(string)
            result=Consulter_historique_transactions(text[1])
            print(result)
            self.clientsocket.send(result.encode())
        elif (r[:7]==b"retrait"):
            text=str(r)
            print("r",r)
            text=text[2:-1]
            text=text.split('*')
            print("text",text)
            string=text[0]+text[1]+text[2]
            print(string)
            result=transaction(text)
            print(result)
            self.clientsocket.send(result.encode())
        mutex.release()
        print("Operation terminee...")

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",1111))

while True:
    tcpsock.listen(10)
    print( "En attente...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()