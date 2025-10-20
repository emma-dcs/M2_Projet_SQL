# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 16:21:59 2024

@author: abgaa
"""



import pymysql
import pandas as pd
import matplotlib.pyplot as plt

try:

    # Connexion à la base de données
    db = pymysql.connect(
        host="146.59.198.88",
        user="lesage",
        password="Rlesage24",
        db="lesage",
        port=3300
    )
    cursor = db.cursor()
    print("Connexion réussie")
    print ("---------------------------------------------------------")

    def check_proprietaire_existe(nom, prenom):
        try:
            query = "SELECT COUNT(*) FROM `Proprietaires` WHERE nom = %s AND prenom = %s"
            cursor.execute(query, (nom, prenom))
            res = cursor.fetchone()
            return res[0]  # Retourne le compte
        except Exception as e:
            print("Une erreur s'est produite", e)
            print ("---------------------------------------------------------")
            return None

    def check_baladeur_existe(nom, prenom):
        try:
            query = "SELECT COUNT(*) FROM `Baladeurs` WHERE nom = %s AND prenom = %s"
            cursor.execute(query, (nom, prenom))
            res = cursor.fetchone()
            return res[0]  # Retourne le compte
        except Exception as e:
            print("Une erreur s'est produite", e)
            print ("---------------------------------------------------------")
            return None

    def enregistrer_proprietaire(nom, prenom, email, NumTel, ville):
        try:
            query = "INSERT INTO `Proprietaires` (nom, prenom, email, NumTel, ville) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (nom, prenom, email, NumTel, ville))
            db.commit()
            print("Propriétaire enregistré avec succès !")
            print ("---------------------------------------------------------")
        except Exception as e:
            db.rollback()
            print("Une erreur s'est produite lors de l'enregistrement du propriétaire :", e)
            print ("---------------------------------------------------------")

    def enregistrer_animaux(IdProp, nb_ani):
        try:
            for i in range(nb_ani):
                nom = input("Nom de votre animal (répondre en minuscules) :")
                espece = input("Espèce (chien ou chat) :")
                race = input("Race (répondre en minuscules et sans espace) :")
                DateNais = input("Année de naissance :")
                taille = input("Taille (petit, moyen ou grand) :")

                sql = "INSERT INTO `Animaux` (nom, espece, race, DateNais, taille, IdProp) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (nom, espece, race, DateNais, taille, IdProp))
                print ("---------------------------------------------------------")
                
            db.commit()
            print("Animaux enregistrés avec succès !")
            print ("---------------------------------------------------------")
        except Exception as e:
            db.rollback()
            print("Une erreur s'est produite lors de l'enregistrement des animaux :", e)
            print ("---------------------------------------------------------")

    def enregistrer_baladeur(nom, prenom, email, NumTel, ville):
        try:
            query = "INSERT INTO `Baladeurs` (nom, prenom, email, NumTel, ville) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (nom, prenom, email, NumTel, ville))
            db.commit()
            print("Baladeur enregistré avec succès !")
            print ("---------------------------------------------------------")
        except Exception as e:
            db.rollback()
            print("Une erreur s'est produite lors de l'enregistrement du baladeur :", e)
            print ("---------------------------------------------------------")
            
    def enregistrer_activites(nb_act, idBal):
        try:
            for i in range(nb_act):
                type_act = input("Entrez 'balade' ou 'garde' : ")
                maxAnim = input("Entrez le nombre maximum d'animaux pour cette activité : ")
                nbActivite = input("Entrez le moment de l'activité 'matin', 'apres_midi' ou 'journee' : ")
                jour = input("Entrez la date de l'activité sous le format 'aaaa-mm-jj' : ")
                prix = input("Entrez le prix de l'activité : ")
                ville = input("Entrez la ville de l'activité : ")
                
                sql = "INSERT INTO `Activites` (type, maxAnim, nbActivite, jour, prix, ville, idBal) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (type_act, maxAnim, nbActivite, jour, prix, ville, idBal))
                print ("---------------------------------------------------------")

            db.commit()
            print("Activités enregistrées avec succès !")
            print ("---------------------------------------------------------")
        except Exception as e:
            db.rollback()
            print("Une erreur s'est produite lors de l'enregistrement des activités :", e)
            print ("---------------------------------------------------------")
    
    def recherche_IdProp (nom, prenom):
        try:
            cursor = db.cursor()
            query = "SELECT idProp FROM `Proprietaires` WHERE nom =%s AND prenom =%s"
            cursor.execute(query, (nom,prenom))
            res = cursor.fetchone()
            cursor.close()
            if res:
                return res[0]
            else:
                return None
        except pymysql.Error as e:
            print("Erreur lors de l'obtention de l'ID du propriétaire' :", e)
            print ("---------------------------------------------------------")
            return None
            
    def recherche_IdBal (nom, prenom):
        try:
            cursor = db.cursor()
            query = "SELECT idBal FROM `Baladeurs` WHERE nom =%s AND prenom =%s"
            cursor.execute(query, (nom,prenom))
            res = cursor.fetchone()
            cursor.close()
            if res:
                return res[0]
            else:
                return None
        except pymysql.Error as e:
            print("Erreur lors de l'obtention de l'ID du baladeur' :", e)
            print ("---------------------------------------------------------")
            return None
            
    def afficher_ani (IdProp):
        try:
            cursor = db.cursor()
            print ('Affichage de vos animaux :')
            query = """
                SELECT a.idAni, a.nom 
                FROM `Animaux` a 
                JOIN `Proprietaires` p ON a.idProp = p.idProp
                WHERE p.idProp =%s
                """
            cursor.execute(query, (IdProp))
            resultats = cursor.fetchall()
            if resultats:
                for row in resultats:
                    print(f"Id_animal : {row[0]}, Nom : {row[1]}")
            else:
                print("Aucun animal trouvé pour l'ID de propriétaire spécifié.")
            print ("---------------------------------------------------------")
        
        except pymysql.Error as e:
            print("Erreur lors de l'affichage des animaux :", e)
            print ("---------------------------------------------------------")
                  
            
    def reserver_activite():
        try:
            fin_res = input("Voulez-vous effectuer une réservation ? (oui ou non)")
            while fin_res != "non":
                jour = input("Entrez le jour de l'activité recherchée (format AAAA-MM-JJ) : ")
                nbActivite = input("Entrez le moment de l'activité recherchée ('matin', 'apres_midi' ou 'journee') : ")
                type_act = input("Entrez le type d'activité recherchée (balade ou garde) : ")
                ville = input("Entrez le nom de la ville de l'activité recherchée : ")

                query = """
                    SELECT b.nom, b.prenom, a.prix, a.IdAct
                    FROM `Baladeurs` b
                    JOIN `Activites` a ON b.IdBal = a.IdBal
                    WHERE a.jour = %s AND a.nbActivite = %s AND a.ville = %s AND a.type = %s
                    AND a.maxAnim > (
                        SELECT COUNT(*)
                        FROM `Reservations` r
                        WHERE r.IdAct = a.IdAct)
                    """
                cursor.execute(query, (jour, nbActivite, ville, type_act))
                resultats = cursor.fetchall()

                if resultats:
                    activites_dict = {str(row[3]): row for row in resultats}
                    print("---------------------------------------------------------")
                    print("Activités disponibles :")
                    for row in resultats:
                        print(f"Nom: {row[0]}, Prénom: {row[1]}, Prix : {row[2]}, Activité ID: {row[3]}")
                        print("---------------------------------------------------------")

                    idAct = input("Entrez l'ID de l'activité que vous souhaitez réserver : ")
                    if idAct in activites_dict:
                        activite = activites_dict[idAct]
                        nomBal = activite[0]
                        prenomBal = activite[1]
                        idBal = recherche_IdBal(nomBal, prenomBal)
                        if idBal:
                            idAni = int(input("Entrez l'ID de votre animal : "))
                            try:
                                query = "INSERT INTO `Reservations` (confirmation, idBal, idAni, idAct) VALUES (1, %s, %s, %s)"
                                cursor.execute(query, (idBal, idAni, idAct))
                                db.commit()
                                print("Activité réservée avec succès !")
                                print("---------------------------------------------------------")
                            except pymysql.Error as e:
                                db.rollback()
                                print("Erreur lors de la réservation de l'activité:", e)
                                print("---------------------------------------------------------")
                        else:
                            print("Baladeur non trouvé.")
                            print("---------------------------------------------------------")
                    else:
                        print("L'ID d'activité que vous avez entré n'est pas disponible.")
                        print("---------------------------------------------------------")

                else:
                    print("---------------------------------------------------------")
                    print("Aucune activité trouvée pour les critères spécifiés.")
                    print("---------------------------------------------------------")

                fin_res = input("Voulez-vous effectuer une nouvelle réservation ? (oui ou non) ")

        except Exception as e:
            db.rollback()
            print("Une erreur s'est produite lors de la recherche de l'activité :", e)
            print("---------------------------------------------------------")

            
    def somme_gagnee (idBal):
        try:
            pjour = input("entrez le premier jour de la période (aaaa-mm-jj) : ")
            djour = input("entrez le dernier jour de la période (aaaa-mm-jj) : ")
            print ("---------------------------------------------------------")
            
            query = """
            SELECT a.idAct, a.type, a.NbActivite, a.jour, a.prix,
            SUM(a.prix) AS total_revenus
            FROM `Activites` a
            JOIN `Reservations` r ON a.idAct = r.idAct
            WHERE a.idBal = %s AND a.jour BETWEEN %s AND %s
            GROUP BY a.idAct, a.type, a.NbActivite, a.jour, a.prix
            """
            cursor.execute(query, (idBal, pjour, djour))
            resultats = cursor.fetchall()
            if resultats:
                for row in resultats:
                    print(f"Activité ID: {row[0]}, Type: {row[1]}, Moment: {row[2]}, Jour: {row[3]}, Prix: {row[4]}, Total Revenus: {row[5]}")
                    print ("---------------------------------------------------------")
            else:
                print("Aucune activité trouvée pour les critères spécifiés.")
                print ("---------------------------------------------------------")

        except Exception as e:
            db.rollback()
            print("Une erreur s'est produite", e)
            print ("---------------------------------------------------------")
            
    def graphique_activites (idBal):
        try:            
            query = """
            SELECT a.jour, COUNT(r.IdRes) AS nombre_reservations
            FROM `Activites` a
            LEFT JOIN `Reservations` r ON a.IdAct = r.IdAct
            WHERE a.IdBal = %s
            GROUP BY a.jour
            ORDER BY a.jour
            """
            cursor.execute(query, (idBal))
            resultats = cursor.fetchall()
            if resultats:
                
                # Créer un DataFrame à partir des résultats de la requête
                df = pd.DataFrame(resultats, columns=['jour', 'nombre_reservations'])
                
                # la colonne 'jour' est de type datetime
                df['jour'] = pd.to_datetime(df['jour'])

                # Tracer le graphique
                plt.figure(figsize=(10, 5))
                plt.plot(df['jour'], df['nombre_reservations'], marker='o', linestyle='-', color='b')
                plt.title("Évolution des activités d'un baladeur")
                plt.xlabel('Date')
                plt.ylabel("Nombre de réservations")
                plt.grid(True)
                plt.xticks(rotation=45)
                plt.tight_layout()

                # Afficher le graphique
                plt.show()

                print ("---------------------------------------------------------")
            else:
                print("une erreur a été produite")
                print ("---------------------------------------------------------")
        except Exception as e:
            db.rollback()
            print("Une erreur s'est produite", e)  
            print ("---------------------------------------------------------")
    
    def activite_baladeur(idBal):
        try:
            query="""
            SELECT a.IdAct, a.type, a.NbActivite, a.jour, a.prix, a.ville
            FROM `Activites` a
            JOIN `Baladeurs` b ON a.IdBal = b.IdBal
            WHERE b.IdBal = %s
            """
            cursor.execute(query, (idBal))
            resultats = cursor.fetchall()
            if resultats:
                for row in resultats:
                    print(f"Activité ID: {row[0]}, Type: {row[1]}, Moment: {row[2]}, Jour: {row[3]}, Prix: {row[4]}, Ville: {row[5]}")
                    print ("---------------------------------------------------------")
            else:
                print("Aucune activité trouvée pour les critères spécifiés.")
                print ("---------------------------------------------------------")
            
        except Exception as e:
            db.rollback()
            print("Une erreur s'est produite", e) 
            print ("---------------------------------------------------------")
            
    def activites_reservees(idBal):
        try:          
            query="""
            SELECT a.IdAct, a.type, a.NbActivite, a.jour, a.prix, a.ville
            FROM `Activites` a
            JOIN `Reservations` r ON a.IdAct = r.IdAct
            WHERE a.IdBal = %s
            """
    
            cursor.execute(query, (idBal))
            resultats = cursor.fetchall()
            if resultats:
                for row in resultats:
                    print(f"Activité ID: {row[0]}, Type: {row[1]}, Moment: {row[2]}, Jour: {row[3]}, Prix: {row[4]}, Prix: {row[5]}")
                    print ("---------------------------------------------------------")
            else:
                print("vous n'avez aucune activité réservée")
                print ("---------------------------------------------------------")
            
        except Exception as e:
            db.rollback()
            print("Une erreur s'est produite", e) 
            print ("---------------------------------------------------------")
            
    def revenu_baladeur(idBal):
        try:
            query="""
            SELECT a.IdBal, SUM(a.prix) AS total_revenus
            FROM `Activites` a
            JOIN `Reservations` r ON a.IdAct = r.IdAct
            WHERE a.IdBal = %s
            GROUP BY a.IdBal
            """
    
            cursor.execute(query, (idBal))
            resultats = cursor.fetchall()
            if resultats:
                for row in resultats:
                    print(f"Baladeur ID: {row[0]}, Revenu total : {row[1]}")
                    print ("---------------------------------------------------------")
            else:
                print("vous n'avez aucun revenu")
                print ("---------------------------------------------------------")
            
        except Exception as e:
            db.rollback()
            print("Une erreur s'est produite", e) 
            print ("---------------------------------------------------------")


## Programme principal

    x = input("Êtes-vous propriétaire ou baladeur ? (répondre en minuscules et sans espace) : ")
    nom = input("Nom (répondre en minuscules) : ")
    prenom = input("Prénom (répondre en minuscules) : ")
    print ("---------------------------------------------------------")

    if x == "propriétaire":
        res = check_proprietaire_existe(nom, prenom)
        
        ## Enregistrement du nouveau propriétaire
        if res == 0: ## Le propriétaire n'existe pas
            email = input("Email : ")
            NumTel = input("Numéro de téléphone format 0X.XX.XX.XX.XX): ")
            ville = input("Ville en Ille-et-Vilaine (répondre en minuscules): ")
            enregistrer_proprietaire(nom, prenom, email, NumTel, ville)
            nb_ani = int(input("Combien d’animaux avez-vous ? "))
            
            ## Enregistrement des animaux
            enregistrer_animaux(cursor.lastrowid, nb_ani)  # Utilise l'ID du propriétaire nouvellement inséré
            
            ## Affichage des animaux du nouveau propriétaire
            afficher_ani(cursor.lastrowid)
            
            
        else: ## Le propriétaire existe déjà dans la base de données
            ## Affichage des animaux du propriétaire
            id_prop = recherche_IdProp(nom, prenom)
            afficher_ani(id_prop)
            enregistrer_ani = input("Voulez-vous enregistrer un nouvel animal ? (oui ou non) : ")
           
            ## Enregistrement d'un nouvel animal par un propriétaire déjà existant
            if enregistrer_ani == "oui":
                nb_ani = int(input("Combien d’animaux voulez-vous enregistrer ? "))
                id_prop = recherche_IdProp(nom, prenom)
                enregistrer_animaux(id_prop, nb_ani)
                afficher_ani(id_prop)
        
        ## Réservation d'une activité
        reserver_activite()

                
    elif x == "baladeur":
        res = check_baladeur_existe(nom, prenom)
        
        ## Enregistrement du nouveau baladeur
        if res == 0:
            email = input("Email : ")
            NumTel = input("Numéro de téléphone (format 0X.XX.XX.XX.XX) : ")
            ville = input("Ville en Ille-et-Vilaine : ")
            enregistrer_baladeur(nom, prenom, email, NumTel, ville)
            nb_act = int(input("Combien d'activités souhaitez-vous enregistrer ? "))
        
            ## Enregistrement des activités
            enregistrer_activites(nb_act, cursor.lastrowid)  # Utilise l'ID du baladeur nouvellement inséré
        
        ## Le baladeur existe déjà
        else:
            print("Ce baladeur existe déjà dans la base de données")
            
        idBal = recherche_IdBal(nom, prenom)
            
        ## Recherche des activités mise en ligne
        act = input("Voulez-vous connaître vos activités ? (oui ou non) ")
        if act =='oui':
            activite_baladeur(idBal)
        
        ## Enregistrement d'une nouvelle activité
        enregistrer_act = input("Voulez-vous enregistrer une nouvelle activité ? (oui ou non) : ")
        if enregistrer_act == "oui":
            nb_act = int(input("Combien d'activités voulez-vous enregistrer ? "))
            id_bal = recherche_IdBal(nom, prenom)
            enregistrer_activites(nb_act, id_bal)
        else:
            print ("---------------------------------------------------------")
            
        ## Somme gagnée sur une période définie
        somme = input("Voulez-vous connaitre la somme gagnée sur un période définie ? (oui ou non) ")
        if somme == "oui":
            somme_gagnee(idBal)
        else:
            print ("---------------------------------------------------------")
                
        ## Graphique des activités
        graph = input("Voulez-vous obtenir le graphique de vos activités ? (oui ou non) ")
        if graph == "oui":
            graphique_activites(idBal)
        else:
            print ("---------------------------------------------------------")
            
        ## Recherche des réservations
        actres = input("Voulez-vous connaître vos activités reservées ? (oui ou non) ")
        if actres =='oui':
            activites_reservees(idBal)
        else:
            print ("---------------------------------------------------------")
            
        ## Somme des revenus    
        revenu = input("Voulez-vous connaître la somme de vos revenus ? (oui ou non) ")
        if revenu =='oui':
            revenu_baladeur(idBal)
        else:
            print ("---------------------------------------------------------")
        
    else:
        print("Erreur : les mots 'baladeur' ou 'propriétaire' n'ont pas été reconnus")

except Exception as e:
    print("Une erreur s'est produite lors de la connexion à la base de données :", e)
    
finally:
    if db.open:
        db.close()
        print("La connexion à la base de données a été fermée")

