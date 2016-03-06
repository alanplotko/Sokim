from os import listdir
from os.path import isfile, join
# import Image
import random

class Deck:

    def __init__(self, folderPath):
        self.folderPath = folderPath
        self.imageFilenames = [f for f in listdir(folderPath) if isfile(join(folderPath,f))]
        random.shuffle(self.imageFilenames)

    def printFilenames(self):
        for filename in self.imageFilenames:
            print filename

    def shuffle(self):
        random.shuffle(self.imageFilenames)

    def getDeck(self):
        return self.imageFilenames

if __name__ == "__main__":
    testDeck = Deck("static/assets/img")
    testDeck.printFilenames()
    print len(testDeck.imageFilenames)

