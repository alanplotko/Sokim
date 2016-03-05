debug = True
class Player:

    def __init__(self, deck):
        self.hand = []
        self.score = 0
        # name = ""
        for i in range(6):
            if not deck:
                print "Deck is empty" #Placeholder respone
            else:
                self.hand.append(deck.pop())

    def drawCard(self, deck):
        if len(self.hand) <= 6:
            self.hand.append(deck.pop())
        else:
            if debug:
                print "Hand is too full"

    def displayHand(self):
        print self.hand

    def removeCard(self, index):
        removedCard = self.hand[index]
        del self.hand[index]
        return removedCard


    def cardsInHand(self):
        return len(self.hand)

    def addPoints(self, num):
        self.score += num

    def getScore(self):
        return self.score
