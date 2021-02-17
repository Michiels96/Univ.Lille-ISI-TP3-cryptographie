# coding: utf-8
import subprocess


class ProofOfConcept:

    def __init__(self):
        self.nom = "Ferrari"


    def run(self):
        res = subprocess.check_output(["ls", "-l"], universal_newlines=True)
        #res = res.split('\n')
        print("ici "+res)




pof = ProofOfConcept()
pof.run()



# Phase de BOOT
# ce qu'il y a dans les clés lorsqu'ils sont décryptés: un mdp hashé  (il ne sera dès lors impossible de connaitre le véritable mdp car hashage est une fct à sens unique)
# il faut alors, lors de la création de key1 et key2, hasher les mot de passe et les mettre respectivement dans key1 et key2.
#   un hash se fait dans un sens, impossible de "dé-hasher"
# 1. hasher mdp-cle1
# (depuis crypto/dossier-critique)
#   cat mdp-cle1 | shasum -a 256 > mdp-cle1-hache
# 2. avec openssl, crypter mdp-cle1 avec mdp-cle1-hache comme clé (=> openssl(mdp-cle1, mdp-cle1-hache) où -K est mdp-cle1-hache) 
#   et le mettre dans cle-usb-1/key1
# (depuis crypto/)
#   openssl enc -aes-256-ecb -in ./dossier-critique/mdp-cle1-hache -out ./cle-usb-1/key1 -K $(cat ./dossier-critique/mdp-cle1-hache)

# 1. hasher mdp-cle2
# (depuis crypto/dossier-critique)
#   cat mdp-cle2 | shasum -a 256 > mdp-cle2-hache
# 2. avec openssl, crypter mdp-cle2 avec mdp-cle2-hache comme clé (=> openssl(mdp-cle2, mdp-cle2-hache) où -K est mdp-cle2-hache) 
#   et le mettre dans cle-usb-2/key2
# (depuis crypto/)
#   openssl enc -aes-256-ecb -in ./dossier-critique/mdp-cle2-hache -out ./cle-usb-2/key2 -K $(cat ./dossier-critique/mdp-cle2-hache)


# Cette partie n'est pas nécessaire à garder car ce sont des fichiers situés sur ramdisk/
#
# key1.decrypt et key2.decrypt sont des fichiers qui contiennent chaqu'un un mdp hashé 
#   ce sont les équivalants à ./dossier-critique/mdp-cle1-hache ./dossier-critique/mdp-cle2-hache


# Pour créer le dataFile.decrypt:
# (depuis crypto/)
#   openssl enc -aes-256-ecb -in ./dossier-critique/unlockedFile -out ./ramdisk/dataFile.decrypt -K $(cat ./dossier-critique/key2.decrypt)

# Pour créer le dataFile:
# (depuis crypto/)
#   openssl enc -aes-256-ecb -in ./dossier-critique/dataFile.decrypt -out ./disk/dataFile -K $(cat ./dossier-critique/key1.decrypt)








#ce programme est en premier lieu un programme qui déchiffre 
#pour les clés:
# 1. demander mdp à l'user1
# 1.2. hacher mdp user1 => hash(mdpUser1)
# (depuis crypto/)
#   $(mdpUser1) | shasum -a 256 > hashedUserPassword
# 1.3. décrypter avec openssl(key1, hash(mdpUser1)) => key1.decrypt
# (depuis crypto/)
#   openssl enc -d -aes-256-ecb -in ./cle-usb-1/key1 -out ./ramdisk/key1.decrypt -K $(hash(mdpUser1))
# 1.4. comparer les hashs reçu d'openssl et le hash du mdp entré par l'user1


# 2.1. demander mdp à l'user2
# 2.2. hacher mdp user2 => hash(mdpUser2)
# (depuis crypto/)
#   $(mdpUser2) | shasum -a 256 > hashedUserPassword
# 2.3. décrypter avec openssl(key2, hash(mdpUser2)) => key2.decrypt
# (depuis crypto/)
#   openssl enc -d -aes-256-ecb -in ./cle-usb-2/key2 -out ./ramdisk/key2.decrypt -K $(hash(mdpUser2))
# 2.4. comparer les hashs reçu d'openssl et le hash du mdp entré par l'user2

# 3. Décrypter le dataFile sur disk/
# (depuis crypto/)
#   openssl enc -d -aes-256-ecb -in ./disk/dataFile -out ./ramdisk/dataFile.decrypt -K $(cat ./ramdisk/key1.decrypt)
# (depuis crypto/)
#   openssl enc -d -aes-256-ecb -in ./ramdisk/dataFile.decrypt -out ./ramdisk/unlockedFile -K $(cat ./ramdisk/key2.decrypt)
