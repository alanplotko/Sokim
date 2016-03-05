import random
import time

from player import Player

# Constants
ALL_OR_NOT = 0
ROUND_ROBIN = 1
debug = True
deck = [i for i in range(0, 100)]
hiddenboard = []
displayedboard = []
cardOwners = {}
players = []
votes = []
storyteller = 0 #Index of storyteller
highestScore = 0
highestScorer = 0
numPlayers = 0

def gameInit():
    if debug:
        print "Inside gameInit"
    random.shuffle(deck)
    global numPlayers, players, storyteller, votes, hiddenboard

    # Get number of players
    numPlayers = input("Enter number of players: ")
    # Initialize players
    players = [Player(deck) for i in range(numPlayers)]
    if debug:
        for i in range(numPlayers):
            print "Created new player"
            players[i].displayHand()
    random.shuffle(players)
    storyteller = 0

    # Initialize votes
    votes = [0 for i in range(numPlayers)]
    hiddenboard = [0 for i in range(numPlayers)]

# Make sure board and votes are loaded first
def evaluateBoard(storytellerCard):
    #Check if all or none found it
    cardCount = 0 #Evaluate 'all or nothing' rule through card count
    for i in range(len(votes)):
        if i != storyteller:
            if displayedboard[votes[i]] == storytellerCard:
                cardCount += 1
                if debug:
                    print "DDENG"
            else:
                cardCount -= 1
                if debug:
                    print "RIP"

    if cardCount == numPlayers-1 or cardCount == 1-numPlayers:
        return ALL_OR_NOT
    else:
        return ROUND_ROBIN

def countPoints(boardEvaluation, storytellerCard):
    if debug:
        print "Inside countPoints"
    global displayedboard
    topScore = 0 #Not modifying the topScore
    topScorer = 0
    if boardEvaluation == ROUND_ROBIN:
        if debug:
            print "ROUND ROBIN"
        # Each player including storyteller gets 3 pts for each vote
        for i in range(len(players)):
            if i == storyteller:
                players[i].addPoints(3)
            else:
                if displayedboard[votes[i]] == storytellerCard:
                    players[i].addPoints(3)
                else:
                    print "Finish this part"

            if topScore < players[i].getScore():
                topScore = players[i].getScore()
                topScorer = i

    else:
        if debug:
            print "ALL OR NOT"
        for i in range(len(players)):
            if i != storyteller:
                players[i].addPoints(2)

            if topScore < players[i].getScore():
                topScore = players[i].getScore()
                topScorer = i

    # Evaluate top score
    global highestScore
    global highestScorer
    highestScore = topScore
    highestScorer = topScorer

def nextPlayer():
    global storyteller
    storyteller = (storyteller + 1) % len(players)
    if debug:
        print("Next moveer")

def setupNextRound():
    if debug:
        print "Inside setupNextRound"
    global cardOwners, votes, hiddenboard, displayedboard, players
    cardOwners.clear()
    # Reset all the votes
    for vote in votes:
        vote = 0

    # Reset board/throw board cards away
    for i in range(numPlayers):
        hiddenboard[i] = 0
        displayedboard[i] = 0

    for player in players:
        player.drawCard(deck)

    nextPlayer()

def gameloop():
    if debug:
        print "Inside setupNextRound"
    global hiddenboard, cardOwners, votes, displayedboard

    if debug:
        print("Start of Loop")
    #Prompt players for cards
    for i in range(numPlayers):
        print "Player %d: Choose a card from your hand: " % i
        players[i].displayHand()
        enteredCardIndex = input("Enter your selection: ")
        enteredCard = players[i].removeCard(enteredCardIndex)
        hiddenboard[i] = enteredCard
        cardOwners[enteredCard] = i #Associating card to owner
        if debug:
            print "You entered %d, which is the card [%d]" % (enteredCardIndex, enteredCard)
    displayedboard = cardOwners.keys()
    random.shuffle(displayedboard)

    #Ask for votes
    print "Here's the shuffled board: "
    print displayedboard
    for i  in range(numPlayers):
        if i != storyteller:
            print "Player %d goes!" % i
            votes[i] = input("Vote on the card that matches the description: ")
    #Evaluate board
    print "Storyteller is Player %d" % storyteller
    countPoints(evaluateBoard(hiddenboard[storyteller]),hiddenboard[storyteller])
    setupNextRound()
    if debug:
        print("End of Loop")


def main():
    hello = 0
    gameInit()
    while(True):
        # if debug:
            # print("************ start of loop" + str(hello) + " ********************")
        gameloop()
        time.sleep(1)
        if highestScore == 30:
            break
        else:
            print "Current high score is %d by Player %d" % (highestScore, highestScorer)
            for i in range(numPlayers):
                print "Player %d has %d points" % (i, players[i].score)

        # if debug:
            # print("************ end of loop" + str(hello) + " ********************")

        hello += 1
    print "Winner is Player %d" % highestScorer
    return

main()
