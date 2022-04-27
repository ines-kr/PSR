
from importlib.util import set_loader
from weakref import ref


class Compte :
    def __init__ (self ,reference,valeur,etat,plafond):
        self.refernece=reference
        self.valeur=valeur
        self.etat=etat 
        self.plafond=plafond
    
    def write_file(self,file) :
        try:
            f=open(file,"a")
            f.write(str(self.refernece)+"."+str(self.valeur)+"."+self.etat+"."+str(self.plafond)+"\n")
        except IOError:
            print("file not found or path is incorrect") 
        f.close() 
def read_comptes(ref): #consulter la liste des comptes 
        f=open("comptes.txt","r")
        l=f.readlines()
        for line in l:
            L=list(line.split("."))
            if (ref==int(L[0])):
                print(line)
                break
            else :
                print("Not found")

def consulter_facture(ref): #consulter la facture d'un compte 
        f=open("facture.txt","r")
        l=f.readlines()
        for line in l:
            L=list(line.split("."))
            if (ref==int(L[0])):
                print(line)
                break
            else :
                print("not found")

def consulter_historique(): #consulter la facture d'un compte 
        f=open("facture.txt","r")
        l=f.readlines()
        if(len(l)!=0):
            for line in l:
                L=list(line.split("."))
                print(L)
        else :
            print("Not found")

def transaction(ref,type,val):
    liste=[]
    bien=open("comptes.txt", 'r+')
    histo=open("histo.txt",'a+')
    facture=open("facture.txt",'a+')
    l=bien.readlines()
    for line in l:
         L=list(line.split("."))
         if (ref==int(L[0])):
             liste.append(L[0])
             liste.append(L[1])
             liste.append(L[2])
             liste.append(L[3])

    if type == 'ajout':
        if liste[2] == 'Negatif':
            liste[1] = str(val - int(liste[1]))
            if int(liste[1]) >= 0:
                liste[2] = 'Positif'
                ligne_bien = L[0] + "." + liste[1] + "." + liste[2] + "." + L[3]+"\n"
                bien.write(ligne_bien)
                ligne_histo = L[0] + "." + "ajout" + "." + str(val) + "." + "succes" + "." + liste[2]+"\n"
                histo.write(ligne_histo)

            else:

                ligne_bien = L[0] + "." + liste[1] + "." + "Negatif" + "." + L[3]+"\n"
                bien.write(ligne_bien)
                ligne_histo = L[0] +"." + "ajout" + "." + str(val) + "." + "succes" + "." + "Negatif  \n"
                histo.write(ligne_histo)
        else:

            liste[1] = str(val + int(liste[1]))
            ligne_bien = L[0] + "." + liste[1] +  "." + "Positif" + "."+ L[3]+"\n"
            bien.write(ligne_bien)
            ligne_histo = L[0] + "." + "ajout" + "." + str(val) + "."+ "succes" +"." + "Positif  \n"
            histo.write(ligne_histo)

    if type == 'retrait':

        if liste[2] == 'Positif':
            # max_retrait = int(liste[1]) + int(liste[3])
            if int(liste[1]) >= val:
                # retrait positif
                liste[1] = str(int(liste[1]) - val)
                resultat = 'succes'

                ligne_bien = L[0] + "."+ liste[1] + "."+ "Positif" +  "." + L[3]+"\n"
                bien.write(ligne_bien)
                ligne_histo = L[0] + "."+ "retrait" +  "." + str(val) + "."+ resultat + "."+ "Positif  \n"
                histo.write(ligne_histo)
                ligne_fact = L[0] + "." + "0"   #fonction recvoir_facture
                facture.write(ligne_fact)

            elif (int(liste[1]) - val) <= int(liste[3]):
                # retrait négatif ( enter rouge)
                nv_etat = 'Negatif'
                nv_solde = abs(int(liste[1]) - val)
                fact = nv_solde * 2 / 100
                resultat = 'succes'
                ligne_bien = L[0] + "."+ nv_solde + "." + nv_etat + "." + L[3]+"\n"
                bien.write(ligne_bien)
                ligne_histo = L[0] + "."+ "retrait" + "."+ str(val) + "."+ resultat +"."+ nv_etat+"\n"
                histo.write(ligne_histo)
                ligne_fact = L[0] +"."+ str(fact)+"\n"
                facture.write(ligne_fact)

            else:
                # limite rouge dépassé  
                resultat = 'echec'
                ligne_histo = L[0] + "." + "retrait" + "."+ str(val) + "."+ resultat + "."+ "Negatif \n"
                histo.write(ligne_histo)

        else:
            if (int(liste[3]) - int(liste[1])) >= val:
                # retrait rouge possible exemple ligne 1 table bien.txt
                resultat = 'succes'
                nv_solde = val + int(liste[1])
                fact = val * 2 / 100
                ligne_bien = L[0] + "." + str(nv_solde) + "." + "Negatif" + "." + L[3]+"\n"
                bien.write(ligne_bien)
                ligne_histo = L[0] + "." +"retrait"+ "." + str(val) + "." + resultat + "." + "Negatif \n"
                histo.write(ligne_histo)
                ligne_fact = L[0] + "." + str(fact)+"\n"
                facture.write(ligne_fact)
            else:
                # limite rouge dépassé ligne 4 
                resultat = 'echec'
                ligne_histo = L[0] + "." + "retrait" + "." + str(val) + "." + resultat + "." + "Negatif \n"
                histo.write(ligne_histo)

    bien.close()
    histo.close()
    facture.close()

    
transaction(2000,'retrait',100)
#Compte(2000,500,"Negatif",700).write_file("comptes.txt")
#consulter_facture(1000)    
#ReadComptes(1000)
#Consulterhistorique() 
