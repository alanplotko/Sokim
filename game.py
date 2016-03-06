import random
import time

from player import Player
from deck import Deck

# Constants
ALL_OR_NOT = 0
ROUND_ROBIN = 1
debug = False

class Game:

    def __init__(self, users, room):
        if debug:
            print "Inside __init__"
       # Initialize players
        self.numPlayers = len(users)
        self.room = room
        self.deck = Deck('static/assets/cards/').getDeck()
        self.players = [Player(users[name], self.deck) for name in range(self.numPlayers)]
        self.pending = self.numPlayers
        print(self.players)
        if debug:
            for i in range(users):
                print "Created new player"
                self.players[i].displayHand()
        random.shuffle(self.players)

        # Select host
        self.host = self.players[0].getName()

        # Initialize votes
        self.votes = [0 for i in range(self.numPlayers)]
        self.hiddenboard = [0 for i in range(self.numPlayers)]
        self.displayedboard = [0 for i in range(self.numPlayers)]
        self.cardOwners = {}

        self.storyteller = 0 #Index of storyteller
        self.highestScore = 0
        self.highestScorer = 0
        self.inputVars = -1
        self.prntout = ""
        self.waiting = False

    def getPlayers(self):
        return self.players

    def getPending(self):
        return self.pending

    def resetPending(self):
        self.pending = self.numPlayers

    def getHost(self):
        return self.host

    def displayVotingHand(self):
        s = ""
        for url in self.displayedboard:
            s += '<img class="deceit_card" src="/static/assets/cards/' + url + '" />'
        return s

    def getPlayerByName(self, name):
        for player in self.players:
            if player.getName() == name:
                return player

    def setDisplayedBoard(self, cards):
        for i in range(self.numPlayers):
            self.displayedboard[i] = cards[i]
        random.shuffle(self.displayedboard)

    def setHiddenBoard(self, cards):
        for i in range(self.numPlayers):
            self.hiddenboard[i] = cards[i]

    def decrementPending(self):
        self.pending -= 1

    def getRoom(self):
        return self.room

    def waitforinput(self, printout, variable):
        self.waiting = True
        self.prntout = printout
        while(self.waiting):
            print("DSLKJDSLK")
            pass
        return self.inputVars

    # Make sure board and votes are loaded first
    def evaluateBoard(self, storytellerCard):
        if debug:
            print "Inside evaluateBoard"
        #Check if all or none found it
        cardCount = 0 #Evaluate 'all or nothing' rule through card count
        for i in range(len(self.votes)):
            if i != self.storyteller:
                if self.displayedboard[self.votes[i]] == storytellerCard:
                    cardCount += 1
                    if debug:
                        print "DDENG"
                else:
                    cardCount -= 1
                    if debug:
                        print "RIP"

        if cardCount == self.numPlayers-1 or cardCount == 1-self.numPlayers:
            return ALL_OR_NOT
        else:
            return ROUND_ROBIN

    def countPoints(self, boardEvaluation, storytellerCard):
        if debug:
            print "Inside countPoints"
        topScore = 0 #Not modifying the topScore
        topScorer = 0
        if boardEvaluation == ROUND_ROBIN:
            if debug:
                print "ROUND ROBIN"
            # Each player including storyteller gets 3 pts for each vote
            for i in range(len(self.players)):
                if i == self.storyteller:
                    self.players[i].addPoints(3)
                else:
                    if self.displayedboard[self.votes[i]] == storytellerCard:
                        self.players[i].addPoints(3)
                    else:
                        print "Finish this part"

                if topScore < self.players[i].getScore():
                    topScore = self.players[i].getScore()
                    topScorer = i

        else:
            if debug:
                print "ALL OR NOT"
            for i in range(self.numPlayers):
                if i != self.storyteller:
                    self.players[i].addPoints(2)

                if topScore < self.players[i].getScore():
                    topScore = self.players[i].getScore()
                    topScorer = i

        # Evaluate top score
        self.highestScore = topScore
        self.highestScorer = topScorer

    def nextPlayer(self):
        if debug:
            print("Inside nextPlayer")
        self.storyteller = (self.storyteller + 1) % self.numPlayers

    def setupNextRound(self):
        if debug:
            print "Inside setupNextRound"
        self.cardOwners.clear()
        # Reset all the votes
        for vote in self.votes:
            vote = 0

        # Reset board/throw board cards away
        for i in range(self.numPlayers):
            self.hiddenboard[i] = 0
            self.displayedboard[i] = 0

        for player in self.players:
            player.drawCard(deck)

        self.nextPlayer()

    # def gameloop(self):
        # ret = []
        # if debug:
            # print "Inside setupNextRound"
        # if debug:
            # print("Start of Loop")
        # #Prompt players for cards
        # for i in range(self.numPlayers):
            # pp = "Player %d: Choose a card from your hand: " % i
            # #ret.append(pp)
            # self.players[i].displayHand()
            # enteredCardIndex = -1
            # while True:
                # enteredCardIndex = self.waitforinput( pp , "cardindex")
                # if enteredCardIndex <= 6 and enteredCardIndex >= 0:
                    # break
                # else:
                    # print "Invalid card"
            # enteredCard = self.players[i].removeCard(enteredCardIndex)
            # self.hiddenboard[i] = enteredCard
            # self.cardOwners[enteredCard] = i #Associating card to owner
            # if debug:
                # print "You entered %d, which is the card [%d]" % (enteredCardIndex, enteredCard)
        # self.displayedboard = self.cardOwners.keys()
        # random.shuffle(self.displayedboard)

        # #Ask for votes
        # ret.append("Here's the shuffled board: ")
        # ret.append(self.displayedboard)
        # for i  in range(self.numPlayers):
            # if i != self.storyteller:
                # ret.append("Player %d goes!\nVote on the card that matches the description: " % i)
                # vote = -1
                # while True:
                    # vote = input(">> ")
                    # if vote <= 6 and vote >= 0 and i != self.cardOwners[self.displayedboard[vote]]:
                        # break
                # self.votes[i] = vote
        # #Evaluate board
        # ret.append("Storyteller is Player %d" % self.storyteller)
        # self.countPoints(self.evaluateBoard(self.hiddenboard[self.storyteller]),self.hiddenboard[self.storyteller])
        # self.setupNextRound()
        # if debug:
            # print("End of Loop")
        # return ret

    def playerChooseCard(self, playerIndex, cardIndex):
        if enteredCardIndex <= 6 and enteredCardIndex >= 0:
            enteredCard = self.players[playerIndex].removeCard(cardIndex)
            self.hiddenboard[i] = enteredCard
            self.cardOwners[enteredCard] = i #Associating card to owner

    def playerVote(self, playerIndex):
        if vote <= 6 and vote >= 0 and i != self.cardOwners[self.displayedboard[vote]]:
                self.votes[i] = vote

    def update(self):
        ret = []
        ret += self.gameloop()
        # time.sleep(1)
        if self.highestScore == 30:
            ret +=  "Winner is Player %d" % self.highestScorer
            return ret
        else:
            ret.append("Current high score is %d by Player %d" % (self.highestScore, self.highestScorer))
            for i in range(self.numPlayers):
                ret.append("Player %d has %d points" % (i, self.players[i].score))
        return ret

    def main(self):
        while(True):
            self.gameloop()
            # time.sleep(1)
            if self.highestScore == 30:
                break
            else:
                print "Current high score is %d by Player %d" % (self.highestScore, self.highestScorer)
                for i in range(self.numPlayers):
                    print "Player %d has %d points" % (i, self.players[i].score)

        print "Winner is Player %d" % self.highestScorer
        return

if __name__ == "__main__":
    uzers = [0, 1, 2]
    deceit = Game(uzers)
    deceit.main()
