debug = True
class Player:

    def __init__(self, name, deck):
        self.hand = []
        self.score = 0
        self.name = name
        self.deck = deck
        self.selectedCard = None
        for i in range(6):
            if not self.deck:
                print "Deck is empty" #Placeholder respone
            else:
                self.hand.append(self.deck.pop())

    def getName(self):
        return self.name

    def getSelectedCard(self):
        return self.selectedCard

    def setSelectedCard(self, card):
        self.selectedCard = card

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

    def removeCard(self, card):
        self.hand.remove(card)

    def cardsInHand(self):
        return len(self.hand)

    def addPoints(self, num):
        self.score += num

    def getScore(self):
        return self.score
