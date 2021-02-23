# coding: utf-8
import subprocess
import sys
import os.path
from os import path

class StartService:

    def __init__(self):
        self.abc = 0

    def fileHandler(self, file, mode, content=None):
        f = open(file, mode)
        if mode == "w":
            f.write(content)
        # elif mode == "r":
        #     print("ici "+str(f.read()))
        f.close

    # https://www.megabeets.net/xor-files-python/
    def operationXOR(self, fichierA, fichierB, fichierSortie):
        # Read two files as byte arrays
        file1_b = bytearray(open(fichierA, 'rb').read())
        file2_b = bytearray(open(fichierB, 'rb').read())

        # Set the length to be the smaller one
        size = len(file1_b) if len(file1_b) < len(file2_b) else len(file2_b)
        xord_byte_array = bytearray(size)

        # XOR between the files
        for i in range(size):
            xord_byte_array[i] = file1_b[i] ^ file2_b[i]

        # Write the XORd bytes to the output file	
        open(fichierSortie, 'wb').write(xord_byte_array)


    def run(self):
        print("\n\tService - Mise en Service - Sélectionné\n")
        combinaison = {0:{"nom":"","emplacementUSBKEY":"","emplacementRAMDISKKEY":""}, 1:{"nom":"","emplacementUSBKEY":"","emplacementRAMDISKKEY":""}}
        if path.exists('./cle-usb-1/key1.crypt') == True:
            combinaison[0]["nom"] = "RESPONSABLE 1"
            combinaison[0]["emplacementUSBKEY"] = "./cle-usb-1/key1.crypt"
            combinaison[0]["emplacementRAMDISKKEY"] = "./ramdisk/key1.decrypt"
        elif path.exists('./cle-usb-1a/key1a.crypt') == True:
            combinaison[0]["nom"] = "REPRESENTANT 1"
            combinaison[0]["emplacementUSBKEY"] = "./cle-usb-1a/key1a.crypt"
            combinaison[0]["emplacementRAMDISKKEY"] = "./ramdisk/key1a.decrypt"

        if path.exists('./cle-usb-2/key2.crypt') == True:
            combinaison[1]["nom"] = "RESPONSABLE 2"
            combinaison[1]["emplacementUSBKEY"] = "./cle-usb-2/key2.crypt"
            combinaison[1]["emplacementRAMDISKKEY"] = "./ramdisk/key2.decrypt"
        elif path.exists('./cle-usb-2a/key2a.crypt') == True:
            combinaison[1]["nom"] = "REPRESENTANT 2"
            combinaison[1]["emplacementUSBKEY"] = "./cle-usb-2a/key2a.crypt"
            combinaison[1]["emplacementRAMDISKKEY"] = "./ramdisk/key2a.decrypt"

            
        print("{0} - Entrez votre mot de passe:".format(combinaison[0]["nom"]))
        choix = ''
        for line in sys.stdin:
            choix = line
            break

        # hashage mot de passe user1
        # écriture mdp user dans ramdisk/mdpUser1
        self.fileHandler("./ramdisk/mdpUser1", "w", choix)

        # 1.2. hasher mdp user1 => hash(mdpUser1)
        subprocess.check_output(["cat ./ramdisk/mdpUser1 | shasum -a 256 > ./ramdisk/mdpUser1-hashe"], shell=True, universal_newlines=True)



        res = subprocess.run(["openssl enc -d -aes-256-ecb -in {0} -out {1} -K $(cat ./ramdisk/mdpUser1-hashe)".format(combinaison[0]["emplacementUSBKEY"], combinaison[0]["emplacementRAMDISKKEY"])], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur, votre mot de passe ({0}) est incorrect - Mise en service échouée\n".format(combinaison[0]["nom"]))
            return -1

        print("\t({0} OK)\n".format(combinaison[0]["nom"]))


        print("{0} - Entrez votre mot de passe:".format(combinaison[1]["nom"]))
        choix = ''
        for line in sys.stdin:
            choix = line
            break

        # hashage mot de passe user2
        # écriture mdp user dans ramdisk/mdpUser2
        self.fileHandler("./ramdisk/mdpUser2", "w", choix)

        # 1.2. hasher mdp user1 => hash(mdpUser2)
        subprocess.check_output(["cat ./ramdisk/mdpUser2 | shasum -a 256 > ./ramdisk/mdpUser2-hashe"], shell=True, universal_newlines=True)

        res = subprocess.run(["openssl enc -d -aes-256-ecb -in {0} -out {1} -K $(cat ./ramdisk/mdpUser2-hashe)".format(combinaison[1]["emplacementUSBKEY"], combinaison[1]["emplacementRAMDISKKEY"])], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur, votre mot de passe ({0}) est incorrect - Mise en service échouée\n".format(combinaison[1]["nom"]))
            return -1

        print("\t({0} OK)\n".format(combinaison[1]["nom"]))         
        


        # Phase XOR
        self.operationXOR(combinaison[0]["emplacementRAMDISKKEY"], combinaison[1]["emplacementRAMDISKKEY"], "./ramdisk/bis")
        subprocess.check_output(["cat ./ramdisk/bis | shasum -a 256 > ./ramdisk/XORTmp"], shell=True, universal_newlines=True)
  

        # Phase 3: décryptage des 4 mainKey.crypt
        # res = subprocess.run(["openssl enc -d -aes-256-ecb -in ./disk/mainKey1.crypt -out ./ramdisk/mainKey1.decrypt -K $(cat ./ramdisk/XORTmp)"], shell=True, stderr=subprocess.PIPE)
        # if res.returncode != 0:
        #     print("\tErreur, le décryptage 'mainKey1.decrypt' n'a pu être décrypté - Mise en service échouée\n")
        #     return -1
        # res = subprocess.run(["openssl enc -d -aes-256-ecb -in ./disk/mainKey2.crypt -out ./ramdisk/mainKey2.decrypt -K $(cat ./ramdisk/XORTmp)"], shell=True, stderr=subprocess.PIPE)
        # if res.returncode != 0:
        #     print("\tErreur, le décryptage 'mainKey2.decrypt' n'a pu être décrypté - Mise en service échouée\n")
        #     return -1
        # res = subprocess.run(["openssl enc -d -aes-256-ecb -in ./disk/mainKey3.crypt -out ./ramdisk/mainKey3.decrypt -K $(cat ./ramdisk/XORTmp)"], shell=True, stderr=subprocess.PIPE)
        # if res.returncode != 0:
        #     print("\tErreur, le décryptage 'mainKey3.decrypt' n'a pu être décrypté - Mise en service échouée\n")
        #     return -1
        # res = subprocess.run(["openssl enc -d -aes-256-ecb -in ./disk/mainKey4.crypt -out ./ramdisk/mainKey4.decrypt -K $(cat ./ramdisk/XORTmp)"], shell=True, stderr=subprocess.PIPE)
        # if res.returncode != 0:
        #     print("\tErreur, le décryptage 'mainKey4.decrypt' n'a pu être décrypté - Mise en service échouée\n")
        #     return -1



        # Phase 3: trouver le mainKey.decrypt correspondant à la paire de clés
        i = 1
        while(i < 5):
            res = subprocess.run(["openssl enc -d -aes-256-ecb -in ./disk/mainKey{0}.crypt -out ./ramdisk/mainKey.decrypt -K $(cat ./ramdisk/XORTmp)".format(i)], shell=True, stderr=subprocess.PIPE)
            if res.returncode == 0:
                break
            i += 1
        if i == 5:
            print("\tErreur, aucune clé 'mainKey.decrypt' n'a pu être compatible - Mise en service échouée\n")
            return -1



        # Phase 4: décrytage dataFile.crypt
        res = subprocess.run(["openssl enc -d -aes-256-ecb -in ./disk/dataFile.crypt -out ./ramdisk/unlockedFile -K $(cat ./ramdisk/mainKey.decrypt)"], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur, le décryptage 'unlockedFile' n'a pu être crypté - Mise en service échouée\n")
            return -1

        print("\tMise en service réussie\n")
        return 0
