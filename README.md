# Projet Marcus 3

Hey bro, voici quelques instructions, notes et rappel que je prévois surtout utiliser pour dupliquer mon environnement de travail sur ton BBB.

## Prochaines tâches

1. Déterminer de quelle façon inclure le "raisonnement" du robot au programme de base (main.py);
2. Il y a actuellement un bug avec la librairie ADC qui créée une "Segmentation Fault". Ç'aurait dû avoir été réglé il y a longtemps selon Adafruit (j'utilise la version 0.0.18);
3. Développer le module CMUCam2+ (sur I2C si possible);

    - Actuellement j'ai quelques problèmes avec i2c, plus particulièrement le module smbus-cffi qui refuse de s'installer avec PIP. Je vais plutôt débugger avec i2cget, i2cdetect, i2cset, etc. qui sont accessibles en CLI. Au pire je pourrai me développer un module Python i2c qui va appeler ces programmes. Par contre pour tout ça il serait préférable d'attendre d'avoir mon oscilloscope.

4. Créer un module "mémoire" avec SQLite3;
5. Développer les autres modules en fonction de mon programme précédent (Marcus 2).

## Guide d'installation BBB - Marcus 3

### Installation d'Arch Linux

- Suivre les étapes données sur le site d'ARM Arch Linux pour le BBB
- Dans les étapes il manque :

        pacman -Syy dostools wget i2c-tools

### Préparation de l'environnement

#### Général (Linux)

- Mise à jour d'Arch Linux ARM :

        pacman -Syu

- Régler le temps et le fuseau horaire :

        timedatectl set-timezone Canada/Eastern
        echo <hostname> > /etc/hostname

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
