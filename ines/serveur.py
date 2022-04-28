from posixpath import split
import socket
import threading

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
  entete='\t'.join(tab[0])
  if(compte==""):
      return(entete+"Compte non existant")
  else:
      compte='\t'.join(compte)
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
  entete='\t'.join(tab[0])
  if(facture==""):
    return(entete,"Compte non existant")
  else:
    facture='\t'.join(facture)
    return (entete+facture)

def Afficher_historique_transactions(file="histo.txt"):
  f = open(file, "rt")
  tab=[]
  for line in f:
      tab.append(line.split('*'))
  f.close()
  return tab

def Consulter_historique_transactions(ref):
    tab=Afficher_historique_transactions()
    entete='\t'.join(tab[0])
    histo=[]
    for element in tab:
        if(element[0]==ref):
            element='\t'.join(element)
            histo.append(element)
    histo='\n'.join(histo)
    return (entete+histo)

def entete(file="facture.txt"):
    f = open(file, "rt")
    tab=[]
    for line in f:
        tab.append(line.split("*"))
    f.close()
    return ("*".join(tab[0]))

def transaction(tab):
    ref=tab[1]
    type=tab[0]
    val=int(tab[2])
    liste=[]
    
    comptes=open("comptes.txt", 'r+')
    histo=open("histo.txt",'a+')
    facture=open("facture.txt",'a+')
    l=comptes.readlines()
    for line in l:
        L=list(line.split("*"))
        if (L[0]!=""):
            if (ref==L[0]):
                liste.append(L[0])
                liste.append(L[1])
                liste.append(L[2])
                liste.append(L[3])
             
    if type == 'depot':
        if liste[2] == 'Negatif':
            liste[1] = int(val) - int(liste[1].strip())
            if (liste[1] >= 0):
                liste[1]=str(liste[1])
                liste[2] = 'Positif'
                ligne_comptes ="\n"+ liste[0] + "*" + liste[1] + "*" + liste[2] + "*" + liste[3]

                comptes.write(ligne_comptes)
                ligne_histo = "\n"+liste[0] + "*" + "depot" + "*" + str(val) + "*" + "succes" + "*" + liste[2]
                histo.write(ligne_histo)
                print(ligne_comptes)
                print(ligne_histo)
                return("succes")
            else:
                liste[1] =str(abs(liste[1]))
                ligne_comptes ="\n"+ liste[0] + "*" + liste[1] + "*" + "Negatif" + "*" + liste[3]
                comptes.write(ligne_comptes)
                ligne_histo = "\n"+liste[0] +"*" + "depot" + "*" + str(val) + "*" + "succes" + "*" + "Negatif"
                histo.write(ligne_histo)
                print(ligne_comptes)
                print(ligne_histo)
                ligne_fact ="\n"+ liste[0] + "*" + "0"   #fonction recvoir_facture
                facture.write(ligne_fact)
                return(entete()+ligne_fact)
        else:
            liste[1] = str(val + int(liste[1]))
            ligne_comptes = "\n"+liste[0] + "*" + liste[1] +  "*" + "Positif" + "*"+ liste[3]
            comptes.write(ligne_comptes)
            ligne_histo ="\n"+ liste[0] + "*" + "depot" + "*" + str(val) + "*"+ "succes" +"*" + "Positif"
            histo.write(ligne_histo)
            print(ligne_comptes)
            print(ligne_histo)
            return("succes")

    if type == 'retrait':

        if liste[2] == 'Positif':
            # max_retrait = int(liste[1]) + int(liste[3])
            if int(liste[1]) >= val:
                # retrait positif
                liste[1] = str(int(liste[1]) - val)
                resultat = 'succes'

                ligne_comptes = "\n"+liste[0] + "*"+ liste[1] + "*"+ "Positif" +  "*" + liste[3]
                comptes.write(ligne_comptes)
                ligne_histo = "\n"+liste[0] + "*"+ "retrait" +  "*" + str(val) + "*"+ resultat + "*"+ "Positif"
                histo.write(ligne_histo)
                ligne_fact ="\n"+ liste[0] + "*" + "0"   #fonction recvoir_facture
                facture.write(ligne_fact)
                return(entete()+ligne_fact)

            elif (int(liste[1]) - val) <= int(liste[3]):
                # retrait négatif ( enter rouge)
                nv_etat = "Negatif"
                nv_solde = abs(int(liste[1]) - val)
                fact = nv_solde * 2 / 100
                resultat ="succes"
                ligne_comptes ="\n"+ liste[0] + "*"+ nv_solde + "*" + nv_etat + "*" + liste[3]
                comptes.write(ligne_comptes)
                ligne_histo ="\n"+ liste[0] + "*"+ "retrait" + "*"+ str(val) + "*"+ resultat +"*"+ nv_etat
                histo.write(ligne_histo)
                ligne_fact ="\n"+ liste[0] +"*"+ str(fact)
                facture.write(ligne_fact)
                return(entete()+ligne_fact)
            else:
                # limite rouge dépassé  
                resultat = "echec"
                ligne_histo ="\n"+ liste[0] + "*" + "retrait" + "*"+ str(val) + "*"+ resultat + "*"+ "Negatif"
                histo.write(ligne_histo)
                return(resultat)

        else:
            if (int(liste[3]) - int(liste[1])) >= val:
                # retrait rouge possible exemple ligne 1 table comptes.txt
                resultat = "succes"
                nv_solde = val + int(liste[1])
                fact = val * 2 / 100
                ligne_comptes ="\n"+ liste[0] + "*" + str(nv_solde) + "*" + "Negatif" + "*" + liste[3]
                comptes.write(ligne_comptes)
                ligne_histo = "\n"+liste[0] + "*" +"retrait"+ "*" + str(val) + "*" + resultat + "*" + "Negatif"
                histo.write(ligne_histo)
                ligne_fact ="\n"+ liste[0] + "*" + str(fact)
                facture.write(ligne_fact)
                return(entete()+ligne_fact)
            else:
                # limite rouge dépassé ligne 4 
                resultat = "echec"
                ligne_histo ="\n"+ liste[0] + "*" + "retrait" + "*" + str(val) + "*" + resultat + "*" + "Negatif"
                histo.write(ligne_histo)
                return(resultat)

    comptes.close()
    histo.close()
    facture.close()

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
            text=text.split(',')
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
            text=text.split(',')
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
            text=text.split(',')
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
            text=text.split(',')
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
            text=text.split(',')
            print("text",text)
            string=text[0]+text[1]+text[2]
            print(string)
            result=transaction(text)
            print(result)
            self.clientsocket.send(result.encode())

        print("Client déconnecté...")

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",1111))

while True:
    tcpsock.listen(10)
    print( "En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()