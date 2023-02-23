import pygame
import sys
import random
from pygame.locals import *

# Création des constantes
global tableau
tableau = 3
tailleTuile = 80
largeurFenetre = 1280
hauteurFenetre = 768
ips = 60
vide = None


#                 R    G    B
noir =         (  0,   0,   0)
blanc =         (255, 255, 255)
bleuCiel =    (  0,  50, 255)
turquoise = (  3,  54,  73)
vert =         (  0, 204,   0)

couleurBG = turquoise
couleurTuile = vert
couleurTexte = blanc
couleurBord = bleuCiel
tailleFont = 20

couleurBouton = blanc
couleurTxtBouton = noir
couleurMessage = blanc

MargeX = int((largeurFenetre - (tailleTuile * tableau + (tableau - 1))) / 15)
MargeY = int((hauteurFenetre - (tailleTuile * tableau + (tableau - 1))) / 5)

haut = 'up'
bas = 'down'
gauche = 'left'
droite = 'right'

def main():
    # Création de valeur global malgrés la mauvaise pratique d'en créé plus d'une.
    global horlogeIPS, surfaceJouable, fontBasic, RAZsurface, RAZrectangle, nouvelleSurface, nouveauRectangle, resoudreSurface, resoudreRectangle
    global facileRectangle, facileSurface, moyenRectangle, moyenSurface, difficileRectangle, difficileSurface, coups
    pygame.init()
    coups = 0
    horlogeIPS = pygame.time.Clock()
    surfaceJouable = pygame.display.set_mode((largeurFenetre, hauteurFenetre))
    pygame.display.set_caption('The Cake Is A Lie')
    fontBasic = pygame.font.Font('freesansbold.ttf', tailleFont)

    # Stockage des boutons d'options et leurs rectangles dans OPTIONS.
    RAZsurface, RAZrectangle = makeText('Remise À Zéro', couleurTexte, couleurTuile, largeurFenetre - 300, hauteurFenetre - 110)
    nouvelleSurface, nouveauRectangle = makeText('Nouvelle Partie', couleurTexte, couleurTuile, largeurFenetre - 300, hauteurFenetre - 80)
    resoudreSurface, resoudreRectangle = makeText('Résoudre', couleurTexte, couleurTuile, largeurFenetre - 300, hauteurFenetre - 50)
    facileSurface, facileRectangle = makeText('Facile (3x3)', couleurTexte, couleurTuile, largeurFenetre - 330, 150)
    moyenSurface, moyenRectangle = makeText('Moyen (4x4)', couleurTexte, couleurTuile, largeurFenetre - 330, 180)
    difficileSurface, difficileRectangle = makeText('Difficile (5x5)', couleurTexte, couleurTuile, largeurFenetre - 330, 210)

    mainBoard, solutionSeq = generateNewPuzzle(20)
    SOLVEDBOARD = getStartingBoard() # Un tableau résolut est un tableau dans un état initiale.
    allMoves = [] # Liste de déplacement créé  à partir de la configuration résolu.

    while True:
        slideTo = None
        msg = 'Appuyez sur une touche fléchée pour déplacer une case.'
        if mainBoard == SOLVEDBOARD:
            msg = 'Résolut !!'

        drawBoard(mainBoard, msg)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    if RAZrectangle.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves)
                        allMoves = []
                        coups = 0
                    elif nouveauRectangle.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(80)
                        allMoves = []
                        coups = 0
                    elif resoudreRectangle.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq + allMoves)
                        allMoves = []
                        coups = "0"
                    elif facileRectangle.collidepoint(event.pos):
                        global tableau
                        tableau = 3
                        difficulte(3)
                        mainBoard, solutionSeq = generateNewPuzzle(20)
                        allMoves = []
                        coups = 0

                    elif moyenRectangle.collidepoint(event.pos):
                        tableau = 4
                        difficulte(4)
                        mainBoard, solutionSeq = generateNewPuzzle(60)
                        allMoves = []
                        coups = 0

                    elif difficileRectangle.collidepoint(event.pos):
                        tableau = 5
                        difficulte(5)
                        mainBoard, solutionSeq = generateNewPuzzle(100)
                        allMoves = []
                        coups = 0


                elif mainBoard != SOLVEDBOARD:
                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = gauche
                        coups += 1
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = droite
                        coups += 1
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = haut
                        coups += 1
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = bas
                        coups += 1

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_q, K_a) and isValidMove(mainBoard, gauche):
                    slideTo = gauche
                    coups += 1
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, droite):
                    slideTo = droite
                    coups += 1
                elif event.key in (K_UP, K_z, K_w) and isValidMove(mainBoard, haut):
                    slideTo = haut
                    coups += 1
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, bas):
                    slideTo = bas
                    coups += 1

        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Appuyez sur une touche fléchée pour déplacer une case.', 8)
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo)
        pygame.display.update()
        horlogeIPS.tick(ips)


def terminate():
    pygame.quit()
    sys.exit()

def difficulte(diff):
    tableau = diff
    getStartingBoard()

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def getStartingBoard():
    counter = 1
    board = []
    for x in range(tableau):
        column = []
        for y in range(tableau):
            column.append(counter)
            counter += tableau
        board.append(column)
        counter -= tableau * (tableau - 1) + tableau - 1

    board[tableau-1][tableau-1] = vide
    return board


def getBlankPosition(board):
    for x in range(tableau):
        for y in range(tableau):
            if board[x][y] == vide:
                return (x, y)


def makeMove(board, move):
    blankx, blanky = getBlankPosition(board)

    if move == haut:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == bas:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == gauche:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == droite:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == haut and blanky != len(board[0]) - 1) or \
           (move == bas and blanky != 0) or \
           (move == gauche and blankx != len(board) - 1) or \
           (move == droite and blankx != 0)


def getRandomMove(board, lastMove=None):
    validMoves = [haut, bas, gauche, droite]

    if lastMove == haut or not isValidMove(board, bas):
        validMoves.remove(bas)
    if lastMove == bas or not isValidMove(board, haut):
        validMoves.remove(haut)
    if lastMove == gauche or not isValidMove(board, droite):
        validMoves.remove(droite)
    if lastMove == droite or not isValidMove(board, gauche):
        validMoves.remove(gauche)

    return random.choice(validMoves)


def getLeftTopOfTile(tileX, tileY):
    left = MargeX + (tileX * tailleTuile) + (tileX - 1)
    top = MargeY + (tileY * tailleTuile) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, tailleTuile, tailleTuile)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(surfaceJouable, couleurTuile, (left + adjx, top + adjy, tailleTuile, tailleTuile))
    textSurf = fontBasic.render(str(number), True, couleurTexte)
    textRect = textSurf.get_rect()
    textRect.center = left + int(tailleTuile / 2) + adjx, top + int(tailleTuile / 2) + adjy
    surfaceJouable.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left):
    textSurf = fontBasic.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    surfaceJouable.fill(couleurBG)
    diffSurf, diffRect = makeText('Sélectionnez une difficulté.', couleurMessage, couleurBG, largeurFenetre - 350, 100)
    surfaceJouable.blit(diffSurf, diffRect)
    scoreSurf, scoreRect = makeText('Nombre de coups joués : '+ str(coups), couleurMessage, couleurBG, 100, 700)
    surfaceJouable.blit(scoreSurf, scoreRect)
    if message:
        textSurf, textRect = makeText(message, couleurMessage, couleurBG, 15, 30)
        surfaceJouable.blit(textSurf, textRect)


    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = tableau * tailleTuile
    height = tableau * tailleTuile
    pygame.draw.rect(surfaceJouable, couleurBord, (left - 5, top - 5, width + 11, height + 11), 4)

    surfaceJouable.blit(RAZsurface, RAZrectangle)
    surfaceJouable.blit(nouvelleSurface, nouveauRectangle)
    surfaceJouable.blit(resoudreSurface, resoudreRectangle)
    surfaceJouable.blit(facileSurface, facileRectangle)
    surfaceJouable.blit(moyenSurface, moyenRectangle)
    surfaceJouable.blit(difficileSurface, difficileRectangle)


def slideAnimation(board, direction, message, animationSpeed):

    blankx, blanky = getBlankPosition(board)
    if direction == haut:
        movex = blankx
        movey = blanky + 1
    elif direction == bas:
        movex = blankx
        movey = blanky - 1
    elif direction == gauche:
        movex = blankx + 1
        movey = blanky
    elif direction == droite:
        movex = blankx - 1
        movey = blanky

    drawBoard(board, message)
    baseSurf = surfaceJouable.copy()
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, couleurBG, (moveLeft, moveTop, tailleTuile, tailleTuile))

    for i in range(0, tailleTuile, animationSpeed):
        checkForQuit()
        surfaceJouable.blit(baseSurf, (0, 0))
        if direction == haut:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == bas:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == gauche:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == droite:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        horlogeIPS.tick(ips)


def generateNewPuzzle(numSlides):
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
#   animation de mélange actuellement commenté pour permettre à l'utilisateur de pouvoir joué plus vite
        slideAnimation(board, move, "Génération d'un nouveau puzzle...", animationSpeed=int(tailleTuile / 2))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves):
    revAllMoves = allMoves[:]
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == haut:
            oppositeMove = bas
        elif move == bas:
            oppositeMove = haut
        elif move == droite:
            oppositeMove = gauche
        elif move == gauche:
            oppositeMove = droite
        slideAnimation(board, oppositeMove, '', animationSpeed=int(tailleTuile / 2))
        makeMove(board, oppositeMove)


if __name__ == '__main__':
    main()