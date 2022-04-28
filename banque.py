"""Pour la banque :
● Consulter la liste des comptes : en donnant la référence d’un compte, on doit
pouvoir récupérer les informations le concernant (valeur, état et plafond) ;
● Consulter la facture d’un compte : il doit être possible de voir la facture
correspondant à un compte en précisant sa référence.
● Consulter l’historique des transactions : il doit être possible de voir le contenu de
l’historique des transactions.
"""
def Afficher_liste_comptes(file="histo.txt"):
  f = open(file, "rt")
  tab=[]
  for line in f:
      tab.append(line.split('\t'))
  f.close()
  return tab

def Consulter_liste_comptes(ref):
  tab=Afficher_liste_comptes()
  compte=""
  for element in tab:
      if(element[0]==ref):
          compte=element
          break;
  entete='\t'.join(tab[0])
  if(compte==""):
      return(entete,"Compte non existant")
  else:
      compte='\t'.join(compte)
      print(entete)
      print(compte)
      return (entete,compte)
    
def Afficher_facture_compte(file="histo.txt"):
    f = open(file, "rt")
    tab=[]
    for line in f:
        tab.append(line.split('\t'))
    f.close()
    return tab

def Consulter_facture_compte(ref):
  tab=Afficher_facture_compte()
  facture=""
  for element in tab:
      if(element[0]==ref):
          facture=element
          break;
  entete='\t'.join(tab[0])
  if(facture==""):
    return(entete,"Compte non existant")
  else:
    compte='\t'.join(compte)
    print(entete)
    print(facture)
    return (entete,facture)

def Afficher_historique_transactions(file="histo.txt"):
  f = open(file, "rt")
  tab=[]
  for line in f:
      tab.append(line.split('\t'))
  f.close()
  print(tab)
  return tab

def Consulter_historique_transactions(ref):
  tab=Afficher_historique_transactions()
  entete=tab[0]
  histo=[]
  for element in tab:
      if(element[0]==ref):
          histo.append(element)
  print(histo)
  return (entete,histo)

Consulter_historique_transactions("1000")
