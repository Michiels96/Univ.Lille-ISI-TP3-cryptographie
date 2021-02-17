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
(ne fonctionne pas -> "hex string is too short, padding with zero bytes to length")

ou
openssl enc -aes-256-ecb -in mdp-cle1 -out ../cle-usb-1/key1 -K $(cat mdp-cle1-hache)

décrypter 
openssl enc -d -aes-256-ecb -in ../cle-usb-1/key1 -out key.decrypt -K $(cat mdp-cle1-hache)


dossier:
1. Archiver:
tar -cf cle-usb1.tar cle-usb-1/
2. Crypter l'archive
openssl enc -aes-256-ecb -in ../cle-usb1.tar -out ../cle-usb-1.crypted -K $(cat mdp-cle1-hache)

3. Décrypter l'archive 
openssl enc -d -aes-256-ecb -in ../cle-usb-1.crypted -out ../cle-usb1.tar -K $(cat mdp-cle1-hache)
4. désarchiver l'archive
tar xvf cle-usb1.tar
