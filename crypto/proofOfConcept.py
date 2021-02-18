# coding: utf-8
import subprocess
import sys
import os.path
from os import path

# classes
from StartService import StartService
from AddService import AddService
from DelService import DelService
from FindService import FindService
from BootService import BootService

class ProofOfConcept:

    def __init__(self):
        self.miseEnServiceOK = False
        self.bootOK = False

        #initialisation des objets
        self.startService = StartService()
        self.addService = AddService()
        self.delService = DelService()
        self.findService = FindService()
        self.bootService = BootService()

    def startServiceHandler(self):
        return self.startService.run()

    def addServiceHandler(self):
        return self.addService.run()

    def delServiceHandler(self):
        return self.delService.run()

    def findServiceHandler(self):
        return self.findService.run()

    def bootServiceHandler(self):
        return self.bootService.run()

    def cryptNewData(self):
        # but: crypter ramdisk/unlockedFile => /disk/dataFile
        # Création dataFile.decrypt
        res = subprocess.run(["openssl enc -aes-256-ecb -in ./ramdisk/unlockedFile -out ./ramdisk/dataFile.decrypt -K $(cat ./ramdisk/key2.decrypt)"], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur, unlockedFile n'a pu être crypté - cryptNewData échoué\n")
            return -1

        # Modification dataFile
        res = subprocess.run(["openssl enc -aes-256-ecb -in ./ramdisk/dataFile.decrypt -out ./disk/dataFile -K $(cat ./ramdisk/key1.decrypt)"], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur, dataFile.decrypt n'a pu être crypté - cryptNewData échoué\n")
            return -1

    def run(self):
        if path.exists('./disk/dataFile') == True:
            self.bootOK = True
        while(True):
            print("Bienvenue dans le serveur, voici les services disponibles:")
            print("1. Mise en Service")
            print("2. Ajouter une paire")
            print("3. Supprimer une paire")
            print("4. Chercher les n° de cartes associées à un nom")
            print("5. BOOT de la machine (initialisation)")
            print("6. Quitter le programme\n")

            print("Entrez votre choix (chiffre correspondant):")
            for line in sys.stdin:
                try:
                    choix = int(line)
                    if choix < 1 or choix > 6:
                        print("\nErreur, vous n'avez pas introduis un chiffre valide, recommencez:")
                    else:
                        break
                except:
                    print("\nErreur, vous n'avez pas introduis un chiffre, recommencez:")
                
            
            if choix == 1:
                if self.bootOK == True:
                    res = self.startServiceHandler()
                    if res == 0:
                        self.miseEnServiceOK = True
                else:
                    print("\tErreur, vous devez d'abord initialiser les supports\n")
            elif choix == 2:
                if self.miseEnServiceOK == True:
                    res = self.addServiceHandler()
                    if res == 0:
                        self.cryptNewData()
                else:
                    print("\tErreur, mise en service requise\n")
            elif choix == 3:
                if self.miseEnServiceOK == True:
                    res = self.delServiceHandler()
                    if res == 0:
                        self.cryptNewData()
                else:
                    print("\tErreur, mise en service requise\n")
            elif choix == 4:
                if self.miseEnServiceOK == True:
                    self.findServiceHandler()
                else:
                    print("\tErreur, mise en service requise\n")
            elif choix == 5:
                print("Cela supprimera déjà les fichiers existants dans /disk, /ramdisk, /cle-usb-1 et /cle-usb-2\n\tEtes vous sur? (O/N)")
                choix = ''
                for line in sys.stdin:
                    choix = line
                    break
              
                if choix == "Oui\n" or choix == "oui\n" or choix == "O\n" or choix == "o\n":
                    res = self.bootServiceHandler()
                    if res == 0:
                        self.bootOK = True  
                else:
                    print("\tInitialisation annulée, OUF! :o\n")
                      
            elif choix == 6:
                print("Aurevoir!")
                subprocess.run(["rm -rf ./ramdisk/*"], shell=True)
                break



pof = ProofOfConcept()
pof.run()



# Phase de BOOT
# ce qu'il y a dans les clés lorsqu'ils sont décryptés: un mdp hashé (il ne sera dès lors impossible de connaitre le véritable mdp car hashage est une fct à sens unique)
# il faut alors, lors de la création de key1 et key2, hasher les mot de passe et les mettre respectivement dans key1 et key2.
#   un hash se fait dans un sens, impossible de "dé-hasher"
# 1. hasher mdp-cle1
# (depuis crypto/dossier-critique)
#   cat mdp-cle1 | shasum -a 256 > mdp-cle1-hashe
# 2. avec openssl, crypter mdp-cle1-hashe avec mdp-cle1-hashe comme clé (=> openssl(mdp-cle1-hashe, mdp-cle1-hashe) où -K est mdp-cle1-hashe) 
#   et le mettre dans cle-usb-1/key1
# (depuis crypto/)
#   openssl enc -aes-256-ecb -in ./dossier-critique/mdp-cle1-hashe -out ./cle-usb-1/key1 -K $(cat ./dossier-critique/mdp-cle1-hashe)

# 1. hasher mdp-cle2
# (depuis crypto/dossier-critique)
#   cat mdp-cle2 | shasum -a 256 > mdp-cle2-hashe
# 2. avec openssl, crypter mdp-cle2-hashe avec mdp-cle2-hashe comme clé (=> openssl(mdp-cle2-hashe, mdp-cle2-hashe) où -K est mdp-cle2-hashe) 
#   et le mettre dans cle-usb-2/key2
# (depuis crypto/)
#   openssl enc -aes-256-ecb -in ./dossier-critique/mdp-cle2-hashe -out ./cle-usb-2/key2 -K $(cat ./dossier-critique/mdp-cle2-hashe)


# Cette partie n'est pas nécessaire à garder car ce sont des fichiers situés sur ramdisk/
#
# key1.decrypt et key2.decrypt sont des fichiers qui contiennent chaqu'un un mdp hashé 
#   ce sont les équivalants à ./dossier-critique/mdp-cle1-hashe ./dossier-critique/mdp-cle2-hashe


# Pour créer le dataFile.decrypt:
# (depuis crypto/)
#   openssl enc -aes-256-ecb -in ./dossier-critique/unlockedFile -out ./ramdisk/dataFile.decrypt -K $(cat ./dossier-critique/key2.decrypt)

# Pour créer le dataFile:
# (depuis crypto/)
#   openssl enc -aes-256-ecb -in ./dossier-critique/dataFile.decrypt -out ./disk/dataFile -K $(cat ./dossier-critique/key1.decrypt)







# Phase de décryptage (Mise en service)
#ce programme est en premier lieu un programme qui déchiffre 
#pour les clés:
# 1.1. demander mdp à l'user1
# 1.2. hasher mdp user1 => hash(mdpUser1)
# (depuis crypto/)
#   $(mdpUser1) | shasum -a 256 > hashedUserPassword
# 1.3. décrypter avec openssl(key1, hash(mdpUser1)) => key1.decrypt
# (depuis crypto/)
#   openssl enc -d -aes-256-ecb -in ./cle-usb-1/key1 -out ./ramdisk/key1.decrypt -K $(hash(mdpUser1))
# 1.4. comparer les hashs reçu d'openssl et le hash du mdp entré par l'user1


# 2.1. demander mdp à l'user2
# 2.2. hasher mdp user2 => hash(mdpUser2)
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
