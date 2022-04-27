"""3. Le serveur réceptionnera la requête et la traitera pour comprendre la demande du
client.
4. Il effectuera ensuite le traitement associé,
5. Le serveur enverra le résultat de ce traitement au poste client concerné
"""
def requete_traitement(requete=""):
  if (requete[0]=='b'):
      if (requete[1:16]=="consult_compte"):
          return Consulter_liste_comptes(requete[16:])
      elif (requete[1:16]=="consult_factur"):
          return Consulter_facture_compte()
      elif (requete[1:17]=="consult_histor"):
          return Consulter_historique_transactions(requete[16:])
   elif (requete[0]=='c'):
       if (requete[1:8]=="retrait"):
          return Retrait(requete[8:])
      elif (requete[1:6]=="ajout"):
          return Retrait(requete[6:])
      elif (requete[1:17]=="consult_factur"):
          return Consulter_facture(requete[16:])

