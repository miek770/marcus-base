#-*- coding:utf-8 -*-

# Librairies standard
#=====================
import logging
from random import random, choice

# Librairies spéciales
#======================
from base import Comportement
from peripheriques.gp2d12 import get_dist

# Vecteur moteur
#================
"""Le comportement doit retourner un vecteur (une liste) décrivant les
actions à prendre par le moteur. La liste est une série de tuples avec
la vitesse du moteur droit, la vitesse du moteur gauche et la durée de
l'événement.

Le module de moteurs doit ensuite interpréter cette commande et la
traduire en consigne de moteurs.

Une nouvelle commande doit interrompre une manoeuvre en cours.

[(vitesse_gauche, vitesse_droite, duree), ...]
"""

class EvasionBrusque(Comportement):

    def variables(self):

        self.seuil_avant = 45 # Seuil de détection, en cm
        self.seuil_cote = 20 # Seuil de détection, en cm
        self.duree_rotation_min = 0.5 # en s

    def decision(self):
        av_mi = get_dist('AIN0') # Avant milieu
        av_ga = get_dist('AIN1') # Avant gauche
        av_dr = get_dist('AIN2') # Avant droit

        # Obstacle à gauche (pas à droite)
        if av_ga <= self.seuil_cote and av_dr > self.seuil_cote:

            # Obstacle devant aussi (tourne plus longtemps)
            if av_mi <= self.seuil_avant:
                logging.info("Comportement {} : Obstacle devant et à gauche, tourne à droite".format(self.nom))
                duree_rotation = self.duree_rotation_min + random()/2

            # Sinon (gauche seulement)
            else:
                logging.info("Comportement {} : Obstacle à gauche, tourne à droite".format(self.nom))
                duree_rotation = random()/2

            return [(100, -100, duree_rotation)]

        # Obstacle à droite (pas à gauche)
        elif av_dr <= self.seuil_cote and av_ga > self.seuil_cote:

            # Obstacle devant aussi (tourne plus longtemps)
            if av_mi <= self.seuil_avant:
                logging.info("Comportement {} : Obstacle devant et à droite, tourne à gauche".format(self.nom))
                duree_rotation = self.duree_rotation_min + random()/2

            # Sinon (droite seulement)
            else:
                logging.info("Comportement {} : Obstacle à droite, tourne à gauche".format(self.nom))
                duree_rotation = random()/2

            return [(100, -100, duree_rotation)]

        # Obstacle à gauche et à droite
        elif av_ga <= self.seuil_cote and av_dr <= self.seuil_cote:

            duree_rotation = self.duree_rotation_min + random()/2
            tourne_gauche = choice((True, False))

            if tourne_gauche:
                logging.info("Comportement {} : Obstacle à gauche et à droite, tourne à gauche".format(self.nom))
                return [(-100, 100, duree_rotation)]
            else:
                logging.info("Comportement {} : Obstacle à gauche et à droite, tourne à droite".format(self.nom))
                return [(100, -100, duree_rotation)]

        # Obstacle devant seulement
        elif av_mi <= self.seuil_avant:
            duree_rotation = self.duree_rotation_min + random()/2
            tourne_gauche = choice((True, False))

            if tourne_gauche:
                logging.info("Comportement {} : Obstacle devant, tourne à gauche".format(self.nom))
                return [(-100, 100, duree_rotation)]
            else:
                logging.info("Comportement {} : Obstacle devant, tourne à droite".format(self.nom))
                return [(100, -100, duree_rotation)]

        return None
