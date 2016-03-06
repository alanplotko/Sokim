import random
import time

from player import Player

# Constants
ALL_OR_NOT = 0
ROUND_ROBIN = 1
debug = False
deck = [i for i in range(0, 100)]
random.shuffle(deck)

class Game:

    def __init__(self):

        if debug:
            print "Inside __init__"
       # Initialize players
        self.numPlayers = input("Enter number of players: ")
        self.players = [Player(deck) for i in range(self.numPlayers)]
        if debug:
            for i in range(self.numPlayers):
                print "Created new player"
                self.players[i].displayHand()
        random.shuffle(self.players)


        # Initialize votes
        self.votes = [0 for i in range(self.numPlayers)]
        self.hiddenboard = [0 for i in range(self.numPlayers)]
        self.displayedboard = [0 for i in range(self.numPlayers)]
        self.cardOwners = {}

        self.storyteller = 0 #Index of storyteller
        self.highestScore = 0
        self.highestScorer = 0
        self.storyteller = 0

    # Make sure board and votes are loaded first
    def evaluateBoard(self,storytellerCard):
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

    def gameloop(self):
        if debug:
            print "Inside setupNextRound"

        if debug:
            print("Start of Loop")
        #Prompt players for cards
        for i in range(self.numPlayers):
            print "Player %d: Choose a card from your hand: " % i
            self.players[i].displayHand()
            enteredCardIndex = -1
            while True:
                enteredCardIndex = input(">> ")
                if enteredCardIndex <= 6 and enteredCardIndex >= 0:
                    break
                else:
                    print "Invalid card"

            enteredCard = self.players[i].removeCard(enteredCardIndex)
            self.hiddenboard[i] = enteredCard
            self.cardOwners[enteredCard] = i #Associating card to owner
            if debug:
                print "You entered %d, which is the card [%d]" % (enteredCardIndex, enteredCard)
        self.displayedboard = self.cardOwners.keys()
        random.shuffle(self.displayedboard)

        #Ask for votes
        print "Here's the shuffled board: "
        print self.displayedboard
        for i  in range(self.numPlayers):
            if i != self.storyteller:
                print "Player %d goes!\nVote on the card that matches the description: " % i
                vote = -1
                while True:
                    vote = input(">> ")
                    if vote <= 6 and vote >= 0:
                        break
            self.votes[i] = input("Vote on the card that matches the description: ")
        #Evaluate board
        print "Storyteller is Player %d" % self.storyteller
        self.countPoints(self.evaluateBoard(self.hiddenboard[self.storyteller]),self.hiddenboard[self.storyteller])
        self.setupNextRound()
        if debug:
            print("End of Loop")


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
    deceit = Game()
    deceit.main()
