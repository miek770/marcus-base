# -*- coding: utf-8 -*-

# Librairies standards
#======================
import argparse, logging, sys
from time import sleep
from multiprocessing import Process, Pipe

# Librairies spéciales
#======================
from peripheriques.pins import set_input, get_input
from comportements import memoire, collision, evasionbrusque, evasiondouce, viser, approche, statisme, exploration
from comportements import agressif, paisible
from peripheriques import cmucam
from arbitres import moteurs, modes
import config

class Marcus:
    """Classe d'application générale. Comprend l'activation des sous-
    routines et des arbitres, ainsi que la boucle principale du robot.
    """

    def __init__(self, args):
        self.args = args

        # Initialisation du journal d'événements
        log_frmt = "%(asctime)s[%(levelname)s] %(message)s"
        date_frmt = "%Y-%m-%d %H:%M:%S "
        if self.args.verbose:
            log_lvl = logging.DEBUG
        else:
            log_lvl = logging.INFO

        logging.basicConfig(filename=self.args.logfile,
                            format=log_frmt,
                            datefmt=date_frmt,
                            level=log_lvl)

        logging.info("Logger initié : {}".format(self.args.logfile))
        logging.info("Programme lancé")

        # Initialisation des pare-chocs
        set_input('P8_7') # Avant droit
        set_input('P8_8') # Avant gauche
        set_input('P8_9') # Arrière droit
        set_input('P8_10') # Arrière gauche

        # Initialisation de la CMUCam2+
        if not self.args.nocam:
            self.cmucam_parent_conn, self.cmucam_child_conn = Pipe()
            self.cmucam_sub = Process(target=cmucam.cam, args=(self.cmucam_child_conn, self.args))
            self.cmucam_sub.start()
            message = self.cmucam_parent_conn.recv()

            if message:
                logging.info("Sous-routine lancée : cmucam_sub")

        # Initialisation des arbitres
        self.arbitres = dict()

        # Arbitre moteurs
        m = moteurs.Moteurs()
        self.arbitres[m.nom] = m
        self.arbitres[m.nom].active(memoire.Memoire(nom="memoire"), 1)
        self.arbitres[m.nom].active(collision.Collision(nom="collision"), 2)
        if not self.args.nocam:
            self.arbitres[m.nom].active(viser.Viser(nom="viser"), 3)
            self.arbitres[m.nom].active(approche.Approche(nom="approche"), 4)
        self.arbitres[m.nom].active(evasiondouce.EvasionDouce(nom="evasion douce"), 5)
        self.arbitres[m.nom].active(evasionbrusque.EvasionBrusque(nom="evasion brusque"), 6)
        self.arbitres[m.nom].active(statisme.Statisme(nom="statisme"), 8)
        self.arbitres[m.nom].active(exploration.Exploration(nom="exploration", priorite=9), 9)

        # Arbitre modes
        if not self.args.nomode:
            m = modes.Modes()
            self.arbitres[m.nom] = m
            self.arbitres[m.nom].active(agressif.Agressif(nom="agressif"), 1)
            self.arbitres[m.nom].active(paisible.Paisible(nom="paisible"), 9)

    def quit(self):
        """Arrêt du programme complet.
        """

        logging.info("Arrêt du programme.")
        for key in self.arbitres.keys():
            self.arbitres[key].arret()
        if not self.args.nocam:
            self.cmucam_sub.terminate()
        sys.exit()

    def loop(self):
        """Boucle principale.
        """

        while True:
            sleep(config.periode)

            # Mise à jour de config.track
            if not self.args.nocam and self.cmucam_parent_conn.poll():
                try:
                    config.track = self.cmucam_parent_conn.recv()
                except EOFError:
                    logging.error("La sous-routine cmucam ne répond plus")
                    self.quit()

            # Arrêt du programme principal
            if self.args.stop:
                if not get_input("P8_7") or not get_input("P8_8") or not get_input("P8_9") or not get_input("P8_10"):
                    self.quit()

            # Interrogation des arbitres
            for key in self.arbitres.keys():
                self.arbitres[key].evalue()

            # Mise à jour de la période
            if not self.args.nomode:
                if not self.args.nocam and config.periode_change:
                    config.periode_change = False
                    self.cmucam_parent_conn.send("periode={}".format(config.periode))

def main():
    """Routine principale. Traitement des arguments et création de
    l'objet d'application général Marcus.
    """

    parser = argparse.ArgumentParser(description='Robot Marcus (BBB) - Michel')

    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help="Augmente la verbosité du programme.")
    parser.add_argument('-l',
                        '--logfile',
                        action='store',
                        default=None,
                        help="Spécifie le chemin du journal d'événement.")
    parser.add_argument('-s',
                        '--stop',
                        action='store_true',
                        help="Arrête l'exécution lorsqu'un impact est détecté.")

    parser.add_argument('--nocam',
                        action='store_true',
                        help="Lance le programme sans la caméra et les comportements qui en dépendent.")
    parser.add_argument('--nomode',
                        action='store_true',
                        help="Lance le programme sans l'arbitre de modes et ses comportements.")
    parser.add_argument('--scan',
                        action='store_true',
                        help="Scanne la couleur devant la caméra au démarrage. Sinon la dernière couleur sauvegardée est chargée.")

    marcus = Marcus(args=parser.parse_args())

    try:
        marcus.loop()

    # Lorsque CTRL-C est reçu...
    except KeyboardInterrupt:
        marcus.quit()

if __name__ == '__main__':
    main()
