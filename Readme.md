# Introduction à la sécurité informatique - TP 3 

Saulquin Aurélie/Clément - Master 1 Iot
Michiels Pierre - Master 1 Cloud Computing

Repository contenant notre solution du TP 3 - cryptographie.


Pour crypter les fichiers, on à utilisé un mdp hashé pour chaque mdp différent.
Commandes:

Hashage:
cat mdp-cle1 | shasum -a 256 > mdp-cle1-hache

cat mdp-cle2 | shasum -a 256 > mdp-cle2-hache

Cryptage:

openssl enc -aes-256-cbc -in mdp-cle1 -out ../cle-usb-1/key1 -K $(cat mdp-cle1-hache) -iv 0
