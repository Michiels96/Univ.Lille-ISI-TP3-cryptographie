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
        print("\n\tService - Initialisation (BOOT) - Sélectionné\n")

        # suppression des restes
        subprocess.run(["rm -rf ./cle-usb-1/*"], shell=True)
        subprocess.run(["rm -rf ./cle-usb-2/*"], shell=True)
        subprocess.run(["rm -rf ./ramdisk/*"], shell=True)
        subprocess.run(["rm -rf ./disk/*"], shell=True)

        print("----- Etape 1: création de valeurs random pour mainKey.decrypt, key1.decrypt, key1a.decrypt, key2.decrypt et key2a.decrypt -----")
        subprocess.check_output(["dd if=/dev/random of=ramdisk/mainKey.decrypt bs=32 count=1"], shell=True, universal_newlines=True)
        subprocess.check_output(["dd if=/dev/random of=ramdisk/key1.decrypt bs=32 count=1"], shell=True, universal_newlines=True)
        subprocess.check_output(["dd if=/dev/random of=ramdisk/key1a.decrypt bs=32 count=1"], shell=True, universal_newlines=True)    
        subprocess.check_output(["dd if=/dev/random of=ramdisk/key2.decrypt bs=32 count=1"], shell=True, universal_newlines=True)
        subprocess.check_output(["dd if=/dev/random of=ramdisk/key2a.decrypt bs=32 count=1"], shell=True, universal_newlines=True)

        
        print("----- Etape 2: XOR avec toutes les combinaisons -----")
        self.operationXOR("./ramdisk/key1a.decrypt", "./ramdisk/key2.decrypt", "./ramdisk/XORKey1aKey2")
        self.operationXOR("./ramdisk/key1a.decrypt", "./ramdisk/key2a.decrypt", "./ramdisk/XORKey1aKey2a")
        self.operationXOR("./ramdisk/key1.decrypt", "./ramdisk/key2.decrypt", "./ramdisk/XORKey1Key2")
        self.operationXOR("./ramdisk/key1.decrypt", "./ramdisk/key2a.decrypt", "./ramdisk/XORKey1Key2a")

        
        print("----- Etape 3: cryptage du mainKey.decrypt avec les 4 combinaisons -----")
        res = subprocess.run(["openssl enc -aes-256-ecb -in ./ramdisk/mainKey.decrypt -out ./disk/mainKey1.crypt -K $(cat ./ramdisk/XORKey1aKey2)"], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur, le cryptage 'mainKey1.crypt' n'a pu être crypté - Initialisation échouée\n")
            return -1
        res = subprocess.run(["openssl enc -aes-256-ecb -in ./ramdisk/mainKey.decrypt -out ./disk/mainKey2.crypt -K $(cat ./ramdisk/XORKey1aKey2a)"], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur, le cryptage 'mainKey2.crypt' n'a pu être crypté - Initialisation échouée\n")
            return -1
        res = subprocess.run(["openssl enc -aes-256-ecb -in ./ramdisk/mainKey.decrypt -out ./disk/mainKey3.crypt -K $(cat ./ramdisk/XORKey1Key2)"], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur, le cryptage 'mainKey3.crypt' n'a pu être crypté - Initialisation échouée\n")
            return -1
        res = subprocess.run(["openssl enc -aes-256-ecb -in ./ramdisk/mainKey.decrypt -out ./disk/mainKey4.crypt -K $(cat ./ramdisk/XORKey1Key2a)"], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur, le cryptage 'mainKey4.crypt' n'a pu être crypté - Initialisation échouée\n")
            return -1

        
        print("----- Etape 4: création et cryptage du fichier unlockedFile -----")
        # Création unlockedFile vide
        self.fileHandler("./ramdisk/unlockedFile", "w", "")
        res = subprocess.run(["openssl enc -aes-256-ecb -in ./ramdisk/unlockedFile -out ./disk/dataFile.crypt -K $(cat ./ramdisk/mainKey.decrypt)"], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur, le cryptage 'dataFile.crypt' n'a pu être crypté - Initialisation échouée\n")
            return -1

        
        print("----- Etape 5. cyptage des 4 clés -----")
        # 1. hasher mdpResponsable1
        print("RESPONSABLE 1 - Entrez votre mot de passe:")
        choix = ''
        for line in sys.stdin:
            choix = line
            break

        # hashage mot de passe Responsable1
        # écriture mdp Responsable1 dans ramdisk/mdpResponsable1
        self.fileHandler("./ramdisk/mdpResponsable1", "w", choix)

        # hasher mdpResponsable1 => hash(mdpResponsable1)
        subprocess.check_output(["cat ./ramdisk/mdpResponsable1 | shasum -a 256 > ./ramdisk/mdpResponsable1-hashe"], shell=True, universal_newlines=True)
        res = subprocess.run(["openssl enc -aes-256-ecb -in ./ramdisk/key1.decrypt -out ./cle-usb-1/key1.crypt -K $(cat ./ramdisk/mdpResponsable1-hashe)"], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur, le cryptage 'key1.crypt' n'a pu être crypté - Initialisation échouée\n")
            return -1

        print("\t(RESPONSABLE 1 OK)\n")


        # 1. hasher mdpRepresentant1
        print("REPRESENTANT 1 - Entrez votre mot de passe:")
        choix = ''
        for line in sys.stdin:
            choix = line
            break

        # hashage mot de passe Representant1
        # écriture mdp Representant1 dans ramdisk/mdpRepresentant1
        self.fileHandler("./ramdisk/mdpRepresentant1", "w", choix)

        # hasher mdpRepresentant1 => hash(mdpRepresentant1)
        subprocess.check_output(["cat ./ramdisk/mdpRepresentant1 | shasum -a 256 > ./ramdisk/mdpRepresentant1-hashe"], shell=True, universal_newlines=True)
        res = subprocess.run(["openssl enc -aes-256-ecb -in ./ramdisk/key1a.decrypt -out ./cle-usb-1a/key1a.crypt -K $(cat ./ramdisk/mdpRepresentant1-hashe)"], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur, le cryptage 'key1a.crypt' n'a pu être crypté - Initialisation échouée\n")
            return -1

        print("\t(REPRESENTANT 1 OK)\n")



        # 1. hasher mdpResponsable2
        print("RESPONSABLE 2 - Entrez votre mot de passe:")
        choix = ''
        for line in sys.stdin:
            choix = line
            break

        # hashage mot de passe Responsable2
        # écriture mdp Responsable2 dans ramdisk/mdpResponsable2
        self.fileHandler("./ramdisk/mdpResponsable2", "w", choix)

        # hasher mdpResponsable2 => hash(mdpResponsable2)
        subprocess.check_output(["cat ./ramdisk/mdpResponsable2 | shasum -a 256 > ./ramdisk/mdpResponsable2-hashe"], shell=True, universal_newlines=True)
        res = subprocess.run(["openssl enc -aes-256-ecb -in ./ramdisk/key2.decrypt -out ./cle-usb-2/key2.crypt -K $(cat ./ramdisk/mdpResponsable2-hashe)"], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur, le cryptage 'key2.crypt' n'a pu être crypté - Initialisation échouée\n")
            return -1

        print("\t(RESPONSABLE 2 OK)\n")


        # 1. hasher mdpRepresentant2
        print("REPRESENTANT 2 - Entrez votre mot de passe:")
        choix = ''
        for line in sys.stdin:
            choix = line
            break

        # hashage mot de passe Representant2
        # écriture mdp Representant2 dans ramdisk/mdpRepresentant2
        self.fileHandler("./ramdisk/mdpRepresentant2", "w", choix)

        # hasher mdpRepresentant2 => hash(mdpRepresentant2)
        subprocess.check_output(["cat ./ramdisk/mdpRepresentant2 | shasum -a 256 > ./ramdisk/mdpRepresentant2-hashe"], shell=True, universal_newlines=True)
        res = subprocess.run(["openssl enc -aes-256-ecb -in ./ramdisk/key2a.decrypt -out ./cle-usb-2a/key2a.crypt -K $(cat ./ramdisk/mdpRepresentant2-hashe)"], shell=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("\tErreur, le cryptage 'key2a.crypt' n'a pu être crypté - Initialisation échouée\n")
            return -1

        print("\t(REPRESENTANT 2 OK)\n")



        print("----- Etape 6: cleanup -----")
        subprocess.run(["rm -rf ./ramdisk/*"], shell=True)

        print("\tInitialisation réussie\n")
        return 0