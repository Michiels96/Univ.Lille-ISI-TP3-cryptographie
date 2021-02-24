# coding: utf-8
import subprocess
import sys

class AddService:

    def __init__(self):
        self.data = {}

    def findPersonne(self, nom) :
        if nom in self.data.keys():
            return self.data[nom]
        else:
            return None

    def getData(self, data):
        data = data.split("\n")
        data.remove('')

        for line in data:
            personne = line.split(';')
            self.data[personne[0]] = personne[1]

    def setData(self):
        dataToFile = ""
        for nomProprietaire in self.data.keys():
            dataToFile += nomProprietaire+";"+self.data[nomProprietaire]+"\n"

        self.fileHandler("./ramdisk/unlockedFile", "w", dataToFile)

    def fileHandler(self, file, mode, content=None):
        f = open(file, mode)
        if mode == "w":
            f.write(content)
        elif mode == "r":
            self.getData(f.read())
        f.close

    def run(self):
        print("\n\tService - Ajouter une paire - Sélectionné\n")

        print("Donnez le nom de la personne possédant la carte bancaire:")
        print("\til est envisagé qu'une personne ne peut avoir qu'un numéro\n\tSi le nom existe déjà, il se verra attribuer le nouveau numéro attribué")
        nomProprietaire = ''
        for line in sys.stdin:
            nomProprietaire = line
            break
        # enlever le '\n'
        nomProprietaire = nomProprietaire[:-1]
        print("Donnez le numéro de la carte bancaire de \"{0}\":".format(nomProprietaire))
        print("\tAttention! -- Vous devez introduire un code IBAN sans espaces (ex: BE00111122223333)")
        print("\t(Le code pays vous sera demandé par la suite)")
        print("Introduisez les 14 chiffres:")
        numCarte = ''
        for line in sys.stdin:
            try:
                # enlever le '\n'
                line = line[:-1]
                numCarte = int(line)
                
                if len(line) < 14 or len(line) > 14:
                    print("\tErreur, vous n'avez pas introduis 14 chiffres, recommencez:")
                else:
                    break
            except:
                print("\tErreur, votre saisie n'est pas valide, recommencez:")

        print("Voici les codes pays disponibles:")
        print("1. BE - Belgique")
        print("2. FR - France")
        print("3. CH - Suisse")

        codePays = 0
        print("\nIntroduisez le chiffre correspondant au pays:")
        for line in sys.stdin:
            try:
                codePays = int(line)
                if codePays < 1 or codePays > 3:
                    print("\nErreur, vous n'avez pas introduis un chiffre valide, recommencez:")
                else:
                    break
            except:
                print("\nErreur, vous n'avez pas introduis un chiffre, recommencez:")

        iban = ""
        if codePays == 1:
            iban = "BE"+str(numCarte)
        elif codePays == 2:
            iban = "FR"+str(numCarte)
        elif codePays == 3:
            iban = "CH"+str(numCarte)

        # récupération des données
        self.fileHandler("./ramdisk/unlockedFile", "r")

        # chercher si la personne existe déjà
        res = self.findPersonne(nomProprietaire)
        if res == None:
            # ajout 
            print("\tAJOUT")
            self.data[nomProprietaire] = iban
        else:
            # mise à jour du numéro de carte
            print("\tMISE A JOUR")
            self.data[nomProprietaire] = iban

        self.setData()


        print("\tAjouter une paire réussi\n")
        return 0


        

        
