# coding: utf-8
import subprocess
import sys

class DelService:

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
        print("\n\tService - Supprimer une paire - Sélectionné\n")

        print("Donnez le nom de la personne possédant la carte bancaire:")
        nomProprietaire = ''
        for line in sys.stdin:
            nomProprietaire = line
            break
        # enlever le '\n'
        nomProprietaire = nomProprietaire[:-1]

        # récupération des données
        self.fileHandler("./ramdisk/unlockedFile", "r")


        # chercher si la personne existe déjà
        res = self.findPersonne(nomProprietaire)
        if res == None:
            print("\tErreur, aucun compte à ce nom\n")
            return -1
        else:
            self.data.pop(nomProprietaire)
            self.setData()
            print("\tSupprimer une paire réussi\n")
            return 0
        return -1