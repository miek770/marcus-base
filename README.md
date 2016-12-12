# Projet Marcus 3

Je désigne cette version comme étant la 3e à cause des changements de contrôleur. Le projet a débuté avec un Brainstem d'Acroname, qui a été remplacé brièvement par un MAKE Controller, puis finalement par un Beaglebone Black.

La principale différence, cependant, est que chaque robot utilise maintenant le même contrôleur et une base commune. Ça facilite beaucoup l'intégration de modules essentiels, comme la CMUCam2+, pour tous les participants.

## Prochaines tâches

- Utiliser les bornes 7 et 8 plutôt que 5 et 6 sur le P9 pour mon 5V. Le SYS_5V est coupé lorsque le BBB est fermé, ce qui va éviter de présenter une tension aux bornes. 250mA max, à tester;
- Créer de nouveaux tests pour le module de CMUCam2+;
- Remplacer certaines boucles par pyinotify pour réduire le temps de réaction ainsi que la charge sur le CPU;
- Créer un module "mémoire" avec SQLite3;
- Créer un module de supervision de batterie. Je pourrais m'en servir dans le journal et peut-être même adapter le comportement du robot.

## Notes

### Alimentation

Avec la batterie actuelle rechargée le robot se promène sans problème pendant plus de 10 minutes. J'ai fait un test et après 14 minutes il s'est mis à hésiter énormément à cause des GP2D12 qui détectaient constamment des obstacles là où il n'y en avait pas. C'est probablement dû à une baisse de tension.

J'ai arrêté le test après environ 17 minutes. Ça fait maintenant une vingtaine de minutes au moins que la batterie alimente le BBB avec une connexion active sur eth0. L'autonomie semble donc suffisante pour les premiers combats.

### Schémas

Les schémas électriques ont été réalisés avec gEDA sur Linux. Il faudrait que je trouve un programme équivalent sur Windows, ou que j'utilise le format DWG à la place (plus commun). Ou SVG.

2016-12-12 : J'utilise maintenant Eagle pour mes circuits électriques et les PCB. Ceux-ci sont commandés chez OSH Park. La tendance est aussi de faire les circuits dans des sous-projets à part, tels que [marcus-boucliers](https://github.com/miek770/marcus-boucliers) et [marcus-bbbcape](https://github.com/miek770/marcus-bbbcape).

### Chasse

Une fois l'autre robot détecté, le robot doit le viser et faire feu. La version préliminaire sera assez limitée puisqu'il n'y aura pas de bouclier et de canon, mais je devrais faire 2 boucles de contrôle avec feedback pour :

1. Centrer le robot sur la cible (viser);
2. Maintenir une distance désirée.

## Installation

- Flasher le BBB avec l'image Debian;
- Configurer hostname, PermitRootLogin;
- Installer git, screen;
- Désinstaller les programmes inutiles (Apache2, Xorg, lightdm, etc.);
- Configurer :

  - dpkg-reconfigure tzdata;
  - dpkg-reconfigure locales (voir la section Standard de https://wiki.debian.org/Locale pour modifier /etc/profile);
  - Samba;

            apt-get install samba
            mv /etc/samba/smb.conf /etc/samba/smb.conf.old
            cp /root/marcus/ressources/smb.conf /etc/samba/smb.conf
            testparm /etc/samba/smb.conf
            systemctl start samba
            systemctl enable samba

  - hosts;
  - vim;
  - bash;
  - marcus.service;
  - uEnv.txt.

