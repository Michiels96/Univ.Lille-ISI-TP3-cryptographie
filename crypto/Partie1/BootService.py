# coding: utf-8
import subprocess
import sys

class BootService:

    def __init__(self):
        self.abc = 0

    def fileHandler(self, file, mode, content=None):
        f = open(file, mode)
        if mode == "w":
            f.write(content)
        f.close

    def run(self):
        print("\n\tService - Initialisation (BOOT) - Sélectionné\n")

        # suppression des restes
        subprocess.run(["rm -rf ./cle-usb-1/*"], shell=True)
        subprocess.run(["rm -rf ./cle-usb-2/*"], shell=True)
        subprocess.run(["rm -rf ./ramdisk/*"], shell=True)
        subprocess.run(["rm -rf ./disk/*"], shell=True)

        print("----- Etape 1: création des fichiers key1/key2 pour les clés usb -----")
        # 1. hasher mdp-cle1
        print("USER 1 - Entrez votre mot de passe:")
        choix = ''
        for line in sys.stdin:
            choix = line
            break

        # hashage mot de passe user1
        # écriture mdp user dans ramdisk/mdp-cle1
        self.fileHandler("./ramdisk/mdp-cle1", "w", choix)

        # hasher mdp user1 => hash(mdp-cle1)
        subprocess.check_output(["cat ./ramdisk/mdp-cle1 | shasum -a 256 > ./ramdisk/mdp-cle1-hashe"], shell=True, universal_newlines=True)
        # création de key1.decrypt
        subprocess.check_output(["cp ./ramdisk/mdp-cle1-hashe ./ramdisk/key1.decrypt"], shell=True, universal_newlines=True)

        # 2. avec openssl, crypter mdp-cle1-hashe avec mdp-cle1-hashe comme clé (=> openssl(mdp-cle1-hashe, mdp-cle1-hashe) où -K est mdp-cle1-hashe) 
        #   et le mettre dans cle-usb-1/key1
        res = subprocess.run(["openssl enc -aes-256-ecb -in ./ramdisk/mdp-cle1-hashe -out ./cle-usb-1/key1 -K $(cat ./ramdisk/mdp-cle1-hashe)"], shell=True, stderr=subprocess.PIPE)
   
        #print("return code -> {0}".format(res.returncode))
        if res.returncode != 0:
            print("\tErreur, votre mot de passe (USER 1) n'a pu être crypté - Initialisation échouée\n")
            return -1

        print("\t(USER 1 OK)\n")


        # 1. hasher mdp-cle2
        print("USER 2 - Entrez votre mot de passe:")
        choix = ''
        for line in sys.stdin:
            choix = line
            break

        # hashage mot de passe user2
        # écriture mdp user dans ramdisk/mdp-cle2
        self.fileHandler("./ramdisk/mdp-cle2", "w", choix)

        # hasher mdp user2 => hash(mdp-cle2)
        subprocess.check_output(["cat ./ramdisk/mdp-cle2 | shasum -a 256 > ./ramdisk/mdp-cle2-hashe"], shell=True, universal_newlines=True)
        # création de key2.decrypt
        subprocess.check_output(["cp ./ramdisk/mdp-cle2-hashe ./ramdisk/key2.decrypt"], shell=True, universal_newlines=True)

        # 2. avec openssl, crypter mdp-cle2-hashe avec mdp-cle2-hashe comme clé (=> openssl(mdp-cle2-hashe, mdp-cle2-hashe) où -K est mdp-cle2-hashe) 
        #   et le mettre dans cle-usb-2/key2
        res = subprocess.run(["openssl enc -aes-256-ecb -in ./ramdisk/mdp-cle2-hashe -out ./cle-usb-2/key2 -K $(cat ./ramdisk/mdp-cle2-hashe)"], shell=True, stderr=subprocess.PIPE)
   
        #print("return code -> {0}".format(res.returncode))
        if res.returncode != 0:
            print("\tErreur, votre mot de passe (USER 2) n'a pu être crypté - Initialisation échouée\n")
            return -1

        print("\t(USER 2 OK)\n")

        print("----- Etape 2: création du fichier vide unlockedFile dans ramdisk/ -----")

        # Création unlockedFile vide
        self.fileHandler("./ramdisk/unlockedFile", "w", "")

        print("----- Etape 3: création du fichier dataFile.decrypt dans ramdisk/ -----")

        # Création dataFile.decrypt
        res = subprocess.run(["openssl enc -aes-256-ecb -in ./ramdisk/unlockedFile -out ./ramdisk/dataFile.decrypt -K $(cat ./ramdisk/key2.decrypt)"], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur, unlockedFile n'a pu être crypté - Initialisation échouée\n")
            return -1

        print("----- Etape 4: création du fichier dataFile dans ramdisk/ -----")

        # Création dataFile
        res = subprocess.run(["openssl enc -aes-256-ecb -in ./ramdisk/dataFile.decrypt -out ./disk/dataFile -K $(cat ./ramdisk/key1.decrypt)"], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur, dataFile.decrypt n'a pu être crypté - Initialisation échouée\n")
            return -1

        # suppression des restes
        subprocess.run(["rm -rf ./ramdisk/*"], shell=True)

        print("\tInitialisation réussie\n")
        return 0