import time
import random

debug = True

currentmoveer = 0
deck = [i for i in range(0, 24)]
hands = [ [-1 for i in range(0, 6)] for x in range(0, 4)]

def gameInit():
    random.shuffle(deck)
    for a in range(0, 4):
        for b in range(0, 6):
            hands[a][b] = draw()
    if debug:
        print("Game Init")


def draw():
    return deck.pop()

def leadermove():
    if debug:
        print("Leader's Move")

    return

def othersmove():
    if debug:
        print("Other moveer's Move")

    return

def flipCards():
    if debug:
        print("Flip Cards")

    return

def countPoints():
    if debug:
        print("Counting Points")

    return

def nextPlayer():
    global currentmoveer
    currentmoveer  = (currentmoveer + 1) % 4
    if debug:
        print("Next moveer")


def gameloop():
    if debug:
        print("Start of Loop")

    leadermove()
    othersmove()
    flipCards()
    countPoints()
    nextPlayer()
    if debug:
        print("End of Loop")


def main():
    hello = 0
    while(True):
        if debug:
            print("************ start of loop" + str(hello) + " ********************")
        gameloop()
        time.sleep(1)
        if debug:
            print("************ end of loop" + str(hello) + " ********************")

        hello += 1
    return

main()



