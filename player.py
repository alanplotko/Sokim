debug = True
class Player:

    def __init__(self, name, deck):
        self.hand = []
        self.score = 0
        self.name = name
        self.deck = deck
        for i in range(6):
            if not self.deck:
                print "Deck is empty" #Placeholder respone
            else:
                self.hand.append(self.deck.pop())

    def getName(self):
        return self.name

    def drawCard(self, deck):
        if len(self.hand) <= 6:
            self.hand.append(self.deck.pop())
        else:
            if debug:
                print "Hand is too full"

    def displayHand(self):
        s = ""
        for url in self.hand:
            s += '<img class="deceit_card" src="/static/assets/cards/' + url + '" />'
        return s

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
