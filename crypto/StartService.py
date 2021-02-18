# coding: utf-8
import subprocess
import sys

class StartService:

    def __init__(self):
        self.abc = 0

    def fileHandler(self, file, mode, content=None):
        f = open(file, mode)
        if mode == "w":
            f.write(content)
        elif mode == "r":
            print("ici "+str(f.read()))
        f.close


    def run(self):
        print("\n\tService - Mise en Service - Sélectionné\n")
        # 1.1. demander mdp à l'user1
        print("USER 1 - Entrez votre mot de passe:")
        choix = ''
        for line in sys.stdin:
            choix = line
            break

        # hashage mot de passe user1
        # écriture mdp user dans ramdisk/mdpUser1
        self.fileHandler("./ramdisk/mdpUser1", "w", choix)

        # 1.2. hasher mdp user1 => hash(mdpUser1)
        subprocess.check_output(["cat ./ramdisk/mdpUser1 | shasum -a 256 > ./ramdisk/mdpUser1-hashe"], shell=True, universal_newlines=True)

        # 1.3. décrypter avec openssl(key1, hash(mdpUser1)) => key1.decrypt
        # 1.4. comparer les hashs reçu d'openssl et le hash du mdp entré par l'user1
        #   La commande de décryptage permet de vérifier si l'argument '-K' est valide ou non en fct du returncode
        res = subprocess.run(["openssl enc -d -aes-256-ecb -in ./cle-usb-1/key1 -out ./ramdisk/key1.decrypt -K $(cat ./ramdisk/mdpUser1-hashe)"], shell=True, stderr=subprocess.PIPE)
   
        #print("return code -> {0}".format(res.returncode))
        if res.returncode != 0:
            print("\tErreur, votre mot de passe (USER 1) est incorrect - Mise en service échouée\n")
            return -1

        print("\t(USER 1 OK)\n")


        # 2.1. demander mdp à l'user2
        print("USER 2 - Entrez votre mot de passe:")
        choix = ''
        for line in sys.stdin:
            choix = line
            break

        # hashage mot de passe user2
        # écriture mdp user dans ramdisk/mdpUser2
        self.fileHandler("./ramdisk/mdpUser2", "w", choix)

        # 2.2. hasher mdp user2 => hash(mdpUser2)
        subprocess.check_output(["cat ./ramdisk/mdpUser2 | shasum -a 256 > ./ramdisk/mdpUser2-hashe"], shell=True, universal_newlines=True)

        # 2.3. décrypter avec openssl(key2, hash(mdpUser2)) => key2.decrypt
        # 2.4. comparer les hashs reçu d'openssl et le hash du mdp entré par l'user2
        #   La commande de décryptage permet de vérifier si l'argument '-K' est valide ou non en fct du returncode
        res = subprocess.run(["openssl enc -d -aes-256-ecb -in ./cle-usb-2/key2 -out ./ramdisk/key2.decrypt -K $(cat ./ramdisk/mdpUser2-hashe)"], shell=True, stderr=subprocess.PIPE)
   
        #print("return code -> {0}".format(res.returncode))
        if res.returncode != 0:
            print("\tErreur, votre mot de passe (USER 2) est incorrect - Mise en service échouée\n")
            return -1

        print("\t(USER 2 OK)\n")           
        

        # 3. Décrypter le dataFile sur disk/
        res = subprocess.run(["openssl enc -d -aes-256-ecb -in ./disk/dataFile -out ./ramdisk/dataFile.decrypt -K $(cat ./ramdisk/key1.decrypt)"], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur au niveau du décryptage openssl ./disk/dataFile\n")
            return -1
        res = subprocess.run(["openssl enc -d -aes-256-ecb -in ./ramdisk/dataFile.decrypt -out ./ramdisk/unlockedFile -K $(cat ./ramdisk/key2.decrypt)"], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur au niveau du décryptage openssl ./ramdisk/dataFile.decrypt\n")
            return -1

        print("\tMise en service réussie\n")




        