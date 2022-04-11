"""Pour la banque :
● Consulter la liste des comptes : en donnant la référence d’un compte, on doit
pouvoir récupérer les informations le concernant (valeur, état et plafond) ;
● Consulter la facture d’un compte : il doit être possible de voir la facture
correspondant à un compte en précisant sa référence.
● Consulter l’historique des transactions : il doit être possible de voir le contenu de
l’historique des transactions.
"""
def Afficher_liste_comptes():
  f = open("comptes.txt", "rt")
  tab=[]
  for line in f:
      tab.append(line.split('\t'))
  f.close()
  return tab

def Consulter_liste_comptes(ref):
  f = open("comptes.txt", "rt")
  tab=[]
  for line in f:
      tab.append(line.split('\t'))
  f.close()
  compte=""
  for element in tab:
      if(element[0]==ref):
          compte=element
          break;
  if(compte==""):
      return("","Compte non existant")
  else:
      entete='    '.join(tab[0])
      compte='    '.join(compte)
      return (entete,compte)
    
def Consulter_facture_compte(ref):
    f = open("factures.txt", "rt")
    tab=[]
    for line in f:
        tab.append(line.split('\t'))
    f.close()
