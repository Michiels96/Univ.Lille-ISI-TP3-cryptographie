# coding: utf-8
import subprocess
import sys

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

    def startServiceHandler(self):
        service = StartService()
        service.run()

    def addServiceHandler(self):
        service = AddService()
        service.run()

    def delServiceHandler(self):
        service = DelService()
        service.run()

    def findServiceHandler(self):
        service = FindService()
        service.run()

    def bootServiceHandler(self):
        service = BootService()
        service.run()


    def run(self):
        # res = subprocess.check_output(["ls", "-l"], universal_newlines=True)
        # #res = res.split('\n')
        # print("ici "+res)
        # print("\n")
        # bootService = BootService()
        # bootService.run()

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
                # if self.bootOK == True:
                #     res = self.startServiceHandler()
                #     if res == 0:
                #         self.miseEnServiceOK = True
                # else:
                #     print("Erreur, fichiers manquants")
                self.startServiceHandler()
            elif choix == 2:
                # if self.miseEnServiceOK == True:
                #     self.addServiceHandler()
                # else:
                #     print("Erreur, fichiers manquants")
                self.addServiceHandler()
            elif choix == 3:
                # if self.miseEnServiceOK == True:
                #     self.delServiceHandler()
                # else:
                #     print("Erreur, fichiers manquants")
                self.delServiceHandler()
            elif choix == 4:
                # if self.miseEnServiceOK == True:
                #     self.findServiceHandler()
                # else:
                #     print("Erreur, fichiers manquants")
                self.findServiceHandler()
            elif choix == 5:
                self.bootServiceHandler()
                self.bootOK = True
            elif choix == 6:
                print("Aurevoir!")
                subprocess.run(["rm -rf ./ramdisk/*"], shell=True)
                break


            #print("choix: "+str(choix))






pof = ProofOfConcept()
pof.run()



# Phase de BOOT
# ce qu'il y a dans les clés lorsqu'ils sont décryptés: un mdp hashé  (il ne sera dès lors impossible de connaitre le véritable mdp car hashage est une fct à sens unique)
# il faut alors, lors de la création de key1 et key2, hasher les mot de passe et les mettre respectivement dans key1 et key2.
#   un hash se fait dans un sens, impossible de "dé-hasher"
# 1. hasher mdp-cle1
# (depuis crypto/dossier-critique)
#   cat mdp-cle1 | shasum -a 256 > mdp-cle1-hashe
# 2. avec openssl, crypter mdp-cle1 avec mdp-cle1-hashe comme clé (=> openssl(mdp-cle1, mdp-cle1-hashe) où -K est mdp-cle1-hashe) 
#   et le mettre dans cle-usb-1/key1
# (depuis crypto/)
#   openssl enc -aes-256-ecb -in ./dossier-critique/mdp-cle1-hashe -out ./cle-usb-1/key1 -K $(cat ./dossier-critique/mdp-cle1-hashe)

# 1. hasher mdp-cle2
# (depuis crypto/dossier-critique)
#   cat mdp-cle2 | shasum -a 256 > mdp-cle2-hashe
# 2. avec openssl, crypter mdp-cle2 avec mdp-cle2-hashe comme clé (=> openssl(mdp-cle2, mdp-cle2-hashe) où -K est mdp-cle2-hashe) 
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







# Phase de décryptage
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
