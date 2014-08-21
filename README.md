# Projet Marcus 3

Hey bro, voici quelques instructions, notes et rappel que je prévois surtout utiliser pour dupliquer mon environnement de travail sur ton BBB.

## Prochaines tâches

- Remplacer ttyO0 par un autre et modifier uEnv.txt pour que ce soit activé au démarrage. Ça devrait régler le problème de démarrage avec la CMUCam2+ raccordée (voir plus bas);
- Réduire le seuil de détection des GP2D12 sur les côtés, et l'augmenter ou le garder tel quel en avant. Autrement le robot a de la difficulté à circuler dans un corridor étroit sans être "distrait" par les murs;
- Ajouter une option (argument) pour arrêter l'exécution si un bumper est actionné;
- Remplacer certaines boucles par pyinotify pour réduire le temps de réaction ainsi que la charge sur le CPU;
- Créer un module "mémoire" avec SQLite3;
- Songer à créer un environnement virtuel pour simuler le fonctionnement du robot (probablement lorsque la plateforme de base sera beaucoup plus avancée);
- [Probablement réglé par le premier item de la liste] Le BBB ne démarre pas si la caméra est alimentée. Je crois que la pin Rx est responsable, elle devrait être à zéro au démarrage plutôt qu'à 3.3V (à valider). De toute façon il suffit de monter le circuit de contrôle de l'alimentation de la CMUCam que j'ai développé pour lui donner son alimentation au moment opportun;
- Ajouter une lecture de la tension de la batterie pour faire un historique (l'enregistrer dans la base de données) et soulever une alarme lorsque le niveau est critique. J'ai eu un problème dernièrement, la batterie a duré seulement quelques minutes après une recharge complète et le BBB s'est éteint. Je crois que la batterie est vieille et je vais la remplacer pour une de plus grande capacité mais si le problème se répète je devrai ajouter une batterie indépendante pour l'électronique.

## Guide d'installation BBB - Marcus 3

Faire attention, le guide n'est pas parfaitement chronologique et pourrait être pas mal amélioré, mais c'est #1 pour quelqu'un qui sait ce qu'il fait :)

Ne pas oublier le dépôt (après avoir installé git naturellement). Le virtualenv2 peut être créé après :

        git clone https://github.com/miek770/marcus-base.git /root/marcus

### Installation d'Arch Linux

- Suivre les étapes données sur le site d'ARM Arch Linux pour le BBB

### Préparation de l'environnement

#### Général (Linux)

- Mise à jour d'Arch Linux ARM :

        pacman -Syu i2c-tools

- Pour donner accès à certains fonctions telles que l'ADC :

        pacman -S linux-am33x-legacy

- Régler le temps et le fuseau horaire :

        timedatectl set-timezone Canada/Eastern
        echo <hostname> > /etc/hostname

- Pour eviter un bug avec pacman qui plante pendant la synchronisation :

        echo 120 > /proc/sys/kernel/hung_task_timeout_secs

#### Samba

- Configurer samba :

        pacman -S samba vim
        mv /etc/samba/smb.conf /etc/samba/smb.conf.old
        cp /root/marcus/smb.conf /etc/samba/smb.conf
        testparm /etc/samba/smb.conf
        systemctl start smbd
        systemctl enable smbd

#### ffi.h (pour I2C)

Il y a un bug dans le module Python cffi qui cherche ffi.h dans /usr/include alors qu'il est dans /usr/lib/libffi-3.x/include. Ce fix fonctionne :

        ln -s /usr/lib/libffi-3.0.13/include/ffi.h /usr/include/ffi.h
        ln -s /usr/lib/libffi-3.0.13/include/ffitarget.h /usr/include/ffitarget.h

Ce n'est pas optimal, mais il faudrait patcher le module Python pour bien corriger le problème.

Par contre ça ne règle rien pour le moment, la prochaine étape est d'installer smbus-cffi mais ça ne fonctionne pas sur le BBB (ça a été développé pour le RPi). Ça va peut-être être corrigé dans le futur...

#### Python

- Installer :

        pacman -S git python2-setuptools gcc python2-virtualenv

- Créer un virtualenv et installer les pré-requis :

        virtualenv2 ~/marcus
        source ~/marcus/bin/activate
        pip install -r ~/marcus/requirements.txt

#### bash.bashrc, vimrc

        cp ~/marcus/bash.bashrc /etc/bash.bashrc
        cp ~/vimrc /etc/vimrc

#### Systemctl

- Lier /usr/lib/systemd/system/marcus.service

        ln -s /root/marcus/marcus.service /usr/lib/systemd/system/marcus.service
        systemctl status marcus

#### systemd-getty-generator

Cette section pourrrait être rendue inutile puisque j'ai remplacé ttyO0 par ttyO1. À valider.

Le générateur 'systemd-getty-generator' doit être désactivé pour permettre l'utilisation du port série /dev/ttyO0 (pour communiquer avec la CMUCam2+). Malheureusement la seule façon que j'ai trouvée pour le désactiver est d'effacer le fichier binaire dans /usr/lib/systemd/system-generators et de l'exclure de pacman (NoExtract = usr/lib/systemd/system-generators/systemd-getty-generator dans /etc/pacman.conf).

#### uEnv.txt

Ajouter le texte suivant à la dernière ligne de uEnv.txt (sur la partition de démarrage), après optargs :

        ; capemgr.enable_partno=BB-UART1

