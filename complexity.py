# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 08:24:56 2024

@author: julia
"""

from itertools import permutations
from math import gcd
from functools import reduce
import matplotlib.pyplot as plt

# fonction pour calculer le PPCM (Hyper-période)
def ppcm(a, b):
    return abs(a * b) // gcd(a, b)  # retourne le plus petit multiple commun de a et b

# fonction pour calculer les temps de réponse
def calculer_temps_de_reponse(ordonnancement, hyper_periode, autoriser_t5_a_manquer=False):
    # création de la liste des jobs en fonction de l'ordonnancement et de la période
    jobs = [{"nom_tache": tache[0], "C_i": tache[1], "T_i": tache[2], "arrivee": j * tache[2], "restant": tache[1]}
            for tache in ordonnancement for j in range(hyper_periode // tache[2])]
    jobs = sorted(jobs, key=lambda x: x["arrivee"])  # tri des jobs par temps d'arrivée

    temps_de_reponse = {tache[0]: [] for tache in ordonnancement}  # dictionnaire des temps de réponse
    temps_courant = 0  # initialisation du temps courant
    deadlines_manquees = 0  # compteur des deadlines manquées
    taches_manquees = set()  # ensemble des tâches ayant manqué leur deadline
    planification = []  # liste de la planification des tâches
    temps_inactivite = 0  # variable pour compter le temps d'inactivité

    print(f"\nCalcul des temps de réponse pour l'ordre : {[tache[0] for tache in ordonnancement]}")

    while jobs:  # tant qu'il reste des jobs à traiter
        jobs_prets = [job for job in jobs if job["arrivee"] <= temps_courant and job["restant"] > 0]  # jobs prêts à être exécutés
        if jobs_prets:  # s'il y a des jobs prêts
            job_courant = jobs_prets[0]  # on prend le premier job prêt
            job_courant["restant"] -= 1  # on diminue le temps restant du job

            if job_courant["restant"] == 0:  # si le job est terminé
                R_ij = temps_courant + 1 - job_courant["arrivee"]  # temps de réponse du job
                temps_de_reponse[job_courant["nom_tache"]].append(R_ij)  # enregistrement du temps de réponse
                planification.append((job_courant["nom_tache"], job_courant["arrivee"], temps_courant + 1, R_ij))  # ajout à la planification
                print(f"  Job {job_courant['nom_tache']} terminé à t={temps_courant+1}, R={R_ij}")

                # Vérification des deadlines
                if temps_courant + 1 > ((job_courant["arrivee"] // job_courant["T_i"]) + 1) * job_courant["T_i"]:
                    taches_manquees.add(job_courant["nom_tache"])  # ajout de la tâche à la liste des tâches manquées
                    if autoriser_t5_a_manquer and job_courant["nom_tache"] == "T5":  # si on autorise T5 à manquer la deadline
                        deadlines_manquees += 1  # on incrémente le compteur des deadlines manquées
                    else:  # si une deadline est manquée et que ce n'est pas T5
                        return None, float('inf'), deadlines_manquees, taches_manquees, temps_inactivite  # on retourne un échec

        else:
            # Si aucun job n'est prêt à être exécuté, on compte cela comme du temps d'inactivité
            temps_inactivite += 1

        temps_courant += 1  # on passe au temps suivant
        jobs = [job for job in jobs if job["restant"] > 0]  # on garde seulement les jobs non terminés

    return temps_de_reponse, deadlines_manquees, planification, taches_manquees, temps_inactivite

# fonction pour calculer les temps de réponse
def calculer_temps_de_reponse2(ordonnancement, hyper_periode, autoriser_t5_a_manquer=False):
    # création de la liste des jobs en fonction de l'ordonnancement et de la période
    jobs = [{"nom_tache": tache[0], "C_i": tache[1], "T_i": tache[2], "arrivee": j * tache[2], "restant": tache[1], "deadline": (j + 1) * tache[2]}
            for tache in ordonnancement for j in range(hyper_periode // tache[2])]
    jobs = sorted(jobs, key=lambda x: x["arrivee"])  # tri des jobs par temps d'arrivée

    temps_de_reponse = {tache[0]: [] for tache in ordonnancement}  # dictionnaire des temps de réponse
    temps_courant = 0  # initialisation du temps courant
    deadlines_manquees = 0  # compteur des deadlines manquées
    taches_manquees = set()  # ensemble des tâches ayant manqué leur deadline
    planification = []  # liste de la planification des tâches
    temps_inactivite = 0  # variable pour compter le temps d'inactivité

    print(f"\nCalcul des temps de réponse pour l'ordre : {[tache[0] for tache in ordonnancement]}")

    while jobs:  # tant qu'il reste des jobs à traiter
        jobs_prets = [job for job in jobs if job["arrivee"] <= temps_courant and job["restant"] > 0]  # jobs prêts à être exécutés
        if jobs_prets:  # s'il y a des jobs prêts
            # tri des jobs prêts par deadline (logique EDF)
            jobs_prets.sort(key=lambda x: x["deadline"])
            job_courant = jobs_prets[0]  # on prend le job avec la deadline la plus proche
            job_courant["restant"] -= 1  # on diminue le temps restant du job

            if job_courant["restant"] == 0:  # si le job est terminé
                R_ij = temps_courant + 1 - job_courant["arrivee"]  # temps de réponse du job
                temps_de_reponse[job_courant["nom_tache"]].append(R_ij)  # enregistrement du temps de réponse
                planification.append((job_courant["nom_tache"], job_courant["arrivee"], temps_courant + 1, R_ij))  # ajout à la planification
                print(f"  Job {job_courant['nom_tache']} terminé à t={temps_courant+1}, R={R_ij}")

                # Vérification des deadlines
                if temps_courant + 1 > job_courant["deadline"]:
                    taches_manquees.add(job_courant["nom_tache"])  # ajout de la tâche à la liste des tâches manquées
                    if autoriser_t5_a_manquer and job_courant["nom_tache"] == "T5":  # si on autorise T5 à manquer la deadline
                        deadlines_manquees += 1  # on incrémente le compteur des deadlines manquées
                    else:  # si une deadline est manquée et que ce n'est pas T5
                        return None, float('inf'), deadlines_manquees, taches_manquees, temps_inactivite  # on retourne un échec

        else:
            # Si aucun job n'est prêt à être exécuté, on compte cela comme du temps d'inactivité
            temps_inactivite += 1

        temps_courant += 1  # on passe au temps suivant
        jobs = [job for job in jobs if job["restant"] > 0]  # on garde seulement les jobs non terminés

    return temps_de_reponse, deadlines_manquees, planification, taches_manquees, temps_inactivite


# définition des tâches : (nom, C_i, T_i)
taches = [
    ("T1", 2, 10),
    ("T2", 2, 10),
    ("T3", 2, 20),
    ("T4", 2, 20),
    ("T5", 2, 40),
    ("T6", 2, 40),
    ("T7", 3, 80)
]
"""
# défintion des tâches avec la nouvelle consigne : (nom, C_i, T_i)
taches = [
    ("T1", 2, 10),
    ("T2", 3, 10),
    ("T3", 2, 20),
    ("T4", 2, 20),
    ("T5", 2, 40),
    ("T6", 2, 40),
    ("T7", 3, 80)
]
"""
# calcul de l'hyper-période
hyper_periode = reduce(ppcm, [tache[2] for tache in taches])  # calcul de l'hyper-période en utilisant le PPCM
print(f"Hyper-période : {hyper_periode}")

# générer toutes les permutations possibles des ordres de tâches
tous_les_ordonnancements = list(permutations(taches))  # toutes les permutations des ordonnancements
nombre_permutations = len(tous_les_ordonnancements)  # nombre total de permutations
print(f"Nombre total de permutations : {nombre_permutations}")

# initialisation des meilleures planifications et des temps d'attente
meilleure_planification_sans_deadline_manquee = None
meilleur_temps_attente_sans_deadline_manquee = float('inf')

meilleure_planification_avec_t5_manquee = None
meilleur_temps_attente_avec_t5_manquee = float('inf')

# test de toutes les permutations
for i, ordonnancement in enumerate(tous_les_ordonnancements, 1):
    print(f"\nTest de l'ordre {i}/{nombre_permutations} : {[tache[0] for tache in ordonnancement]}")

    # calcul des temps de réponse sans permettre à T5 de manquer une deadline
    temps_de_reponse, deadlines_manquees, planification, taches_manquees, temps_inactivite = calculer_temps_de_reponse(ordonnancement, hyper_periode)
    #temps_de_reponse, deadlines_manquees, planification, taches_manquees, temps_inactivite = calculer_temps_de_reponse2(ordonnancement, hyper_periode)
    if temps_de_reponse and deadlines_manquees == 0:  # si aucune deadline n'est manquée
        temps_attente_total = sum(sum(temps) for temps in temps_de_reponse.values())  # calcul du temps d'attente total
        if temps_attente_total < meilleur_temps_attente_sans_deadline_manquee:  # si le temps d'attente est meilleur
            meilleur_temps_attente_sans_deadline_manquee = temps_attente_total
            meilleure_planification_sans_deadline_manquee = planification  # mise à jour de la meilleure planification

    # calcul des temps de réponse en autorisant T5 à manquer sa deadline
    temps_de_reponse, deadlines_manquees, planification, taches_manquees, temps_inactivite = calculer_temps_de_reponse(ordonnancement, hyper_periode, autoriser_t5_a_manquer=True)
    #temps_de_reponse, deadlines_manquees, planification, taches_manquees, temps_inactivite = calculer_temps_de_reponse2(ordonnancement, hyper_periode, autoriser_t5_a_manquer=True)
    if temps_de_reponse:  # si l'ordonnancement est valide
        temps_attente_total = sum(sum(temps) for temps in temps_de_reponse.values())  # calcul du temps d'attente total
        if temps_attente_total < meilleur_temps_attente_avec_t5_manquee:  # si le temps d'attente est meilleur
            meilleur_temps_attente_avec_t5_manquee = temps_attente_total
            meilleure_planification_avec_t5_manquee = planification  # mise à jour de la meilleure planification

# affichage des résultats
if meilleure_planification_sans_deadline_manquee:
    print("\nMeilleur ordonnancement sans deadline manquée :")
    for job_name, arrival, finish, response in meilleure_planification_sans_deadline_manquee:
        print(f"  Job {job_name} - Arrivée : {arrival}, Fin : {finish}, Temps de réponse : {response}")
    print(f"Temps total d'attente : {meilleur_temps_attente_sans_deadline_manquee}")
    print(f"Temps d'inactivité : {temps_inactivite}")
else:
    print("\nAucun ordonnancement valide sans deadline manquée.")
    print(f"Tâches ayant manqué leur deadline : {', '.join(taches_manquees)}")

if meilleure_planification_avec_t5_manquee:
    print("\nMeilleur ordonnancement en autorisant T5 à manquer une deadline :")
    for job_name, arrival, finish, response in meilleure_planification_avec_t5_manquee:
        print(f"  Job {job_name} - Arrivée : {arrival}, Fin : {finish}, Temps de réponse : {response}")
    print(f"Temps total d'attente : {meilleur_temps_attente_avec_t5_manquee}")
    print(f"Temps d'inactivité : {temps_inactivite}")
else:
    print("\nAucun ordonnancement valide même en autorisant T5 à manquer une deadline.")
    print(f"Tâches ayant manqué leur deadline : {', '.join(taches_manquees)}")
    

# tracé du diagramme de Gantt pour la meilleure planification
if meilleure_planification_sans_deadline_manquee:
    plt.figure(figsize=(10, 6))
    
    # tracer chaque tâche sur le diagramme de Gantt
    for i, item in enumerate(meilleure_planification_sans_deadline_manquee):
        nom_tache, debut, fin, _ = item
        plt.barh(nom_tache, fin - debut, left=debut, color='pink', edgecolor='black')

    plt.xlabel("Temps")
    plt.ylabel("Tâches")
    plt.title("Diagramme de Gantt pour la meilleure planification")
    plt.grid(True, axis='x')
    plt.show()

