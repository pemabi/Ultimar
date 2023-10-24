import pygame as p
from copy import deepcopy

WIDTH = HEIGHT = 512  # tweak idea : user inputted / selected board size
MENUS = {}
MAX_FPS = 15
clock = p.time.Clock()
optionKeys = ['onePlayer', 'twoPlayer', 'zeroPlayer', 'undos', 'highlightImmob', 'highlightMoves', 'color']
optionDefaults = [False, False, False, True, True, True, True]  # [oneplayer, twoplayer, aivsai, undos, immobhighlight, movehighlight, colorselect]

# awkward, but dict that takes button and existing gameplay menu references as a key for relevant menu screen that should be displayed
gameplayMenuSelect = {
    (1, 0) : 3, (1, 3) : 3, (1, 6) : 6, (1, 9) : 9, (1, 12) : 12, (1, 15) : 6, (1, 18) : 12, (1, 21) : 9,
    (2, 0) : 15, (2, 3) : 6, (2, 6) : 6, (2, 9) : 12, (2, 12) : 12, (2, 15) : 15, (2, 18) : 18, (2, 21) : 18,
    (3, 0) : 21, (3, 3) : 9, (3, 6) : 12, (3, 9) : 9, (3, 12) : 12, (3, 15) : 18, (3, 18) : 18, (3, 21) : 21,
    (4, 0) : 1, (4, 3) : 4, (4, 6) : 7, (4, 9) : 10, (4, 12) : 13, (4, 15) : 16, (4, 18) : 19, (4, 21) : 22,
    (5, 0) : 2, (5, 3) : 5, (5, 6) : 8, (5, 9) : 11, (5, 12) : 14, (5, 15) : 17, (5, 18) : 20, (5, 21) : 23               
    }

def loadImages():
    for pic in range(24):
        MENUS[pic] = p.transform.scale(p.image.load("Ultimar/images/Menus/gameplaymenu/menu2_" + str(pic) + ".png"), (WIDTH, HEIGHT))
    MENUS[25] = p.transform.scale(p.image.load("Ultimar/images/Menus/mainmenu/main_menu.png"), (WIDTH, HEIGHT))
    MENUS[26] = p.transform.scale(p.image.load("Ultimar/images/Menus/mainmenu/mainmenu_buttons_1.png"), (WIDTH, HEIGHT))
    MENUS[27] = p.transform.scale(p.image.load("Ultimar/images/Menus/mainmenu/mainmenu_buttons_2.png"), (WIDTH, HEIGHT))
    MENUS[28] = p.transform.scale(p.image.load("Ultimar/images/Menus/mainmenu/mainmenu_buttons_3.png"), (WIDTH, HEIGHT))
    MENUS[39] = p.transform.scale(p.image.load("Ultimar/images/Menus/mainmenu/mainmenu_buttons_blank.png"), (WIDTH, HEIGHT))
    MENUS[30] = p.transform.scale(p.image.load("Ultimar/images/Menus/transition_100p opacity.png"), (WIDTH, HEIGHT))
    MENUS[31] = p.transform.scale(p.image.load("Ultimar/images/Menus/mainmenu/Main_background_rotated.png"), (WIDTH, HEIGHT))
    MENUS[32] = p.transform.scale(p.image.load("Ultimar/images/Menus/mainmenu/main_menu_1.png"), (WIDTH, HEIGHT))
    MENUS[33] = p.transform.scale(p.image.load("Ultimar/images/Menus/mainmenu/main_menu_2.png"), (WIDTH, HEIGHT))
    MENUS[34] = p.transform.scale(p.image.load("Ultimar/images/Menus/mainmenu/main_menu_3.png"), (WIDTH, HEIGHT))
    MENUS[35] = p.transform.scale(p.image.load("Ultimar/images/Menus/mainmenu/main_menu_background.png"), (WIDTH, HEIGHT))
    MENUS[36] = p.transform.scale(p.image.load("Ultimar/images/Menus/menu2.png"), (WIDTH, HEIGHT))
    for pic in range(37, 40):
        MENUS[pic] = p.transform.scale(p.image.load("Ultimar/images/Menus/colorselect/colorSelect_" + str(pic-37) + ".png"), (WIDTH, HEIGHT))

    for image in MENUS:
        MENUS[image] = MENUS[image].convert_alpha()  # converts photos into easier to blit format, with alpha settings

def isMainButton(mouse):  # checks if mouse pos in main menu is in button area
    if 82.8 <= mouse[0] <= 429.2:
        if 222 <= mouse[1] <= 262.9:
            return 32
        elif 292.6 <= mouse[1] <= 333.5:
            return 33
        elif 356.4 <= mouse[1] <= 397.3:
            return 34
    else:
        return False
    
def checkSelected():  # returns gameplay menu screen based on options selected
    if options[3]:
        if options[4]:
            x = 12 if options[5] else 6
        else:
            x = 9 if options[5] else 3
    else:
        if options[4]:
            x = 18 if options[5] else 15
        else:
            x = 21 if options[5] else 0
    return x

def drawCircles(screen):  # draws on green circles to gameplay menu select boxes
    if options[3]:
        p.draw.circle(screen, (25, 89, 0), (75, 102.5), 15)
    if options[4]:
        p.draw.circle(screen, (25, 89, 0), (75, 170.5), 15)
    if options[5]:
        p.draw.circle(screen, (25, 89, 0), (75, 313.5), 15)

def isGameplayButton(mouse):
    x = 0  # represents which button mouse is on, with 0 as no button
    if (57 <= mouse[0] <= 92 or 108 <= mouse[0] <= 458) and 85 <= mouse[1] <= 331:  # options buttons
        if 85 <= mouse[1] <= 120:  # top button
            x = 1
        elif 153 <= mouse[1] <= 188 or (153 <= mouse[1] <= 263 and 108 <= mouse[0] <= 458):  # highlight immob pcs button
            x = 2
        elif 296 <= mouse[1] <= 331:  # highlight moves button
            x = 3
    elif 376 <= mouse[1] <= 411:  # checks y axis to see if it is at right height for back/enter buttons
        if 58 <= mouse[0] <= 173:  # checks is back button
            x = 4
        elif 201 <= mouse[0] <= 459:  # enter button
            x = 5
    return x

def colorSelect(mouse):  # checks mouse pos on select color screen. Returns Fasle for white and True for black
    if 0 <= mouse[1] <= 512:
        if 0 <= mouse[0] <= 256:
            return False
        elif 256 < mouse[0] <= 512:
            return True
        
def fadeBlack(screen):
    MENUS[30].set_alpha(0)  # fade to black
    i = 0
    while i <= 254:
        i += 2
        MENUS[30].set_alpha(i)
        screen.blit(MENUS[30], (0,0))
        p.display.flip()
        clock.tick(60)

def runMenu(screen):
    loadImages()  # loads menu screens
    runMainMenu(screen)
    return options

def runMainMenu(screen):
    inMenu = True  # controls exit of main loop
    mainButton = False
    gameplayButton = False
    mainAnimation = False  # flag that triggers animation from main menu to gameplay menu
    mainMenu = True  # flag for which menu user is in
    gameplayMenu = False  # flag for which menu
    colorSelectMenu = False
    mainscreen = 25  # default main screen

    global options
    options = deepcopy(optionDefaults)

    while inMenu:
        for ev in p.event.get():
            if ev.type == p.QUIT:
                inMenu = False
                p.quit()
            if ev.type == p.MOUSEBUTTONDOWN:  # checks for mouseclick
                if mainMenu:
                    mainButton = isMainButton(p.mouse.get_pos())  # checks to see if click is inside button
                elif gameplayMenu:
                    gameplayButton = isGameplayButton(p.mouse.get_pos())
                elif colorSelectMenu:
                    if colorSelect(p.mouse.get_pos()):
                        options[6] = False
                    fadeBlack(screen)
                    mainscreen = 30
                    colorSelectMenu = False
                    inMenu = False
            if ev.type == p.K_DELETE:
                inMenu = False

        if mainMenu:
            highlightMainButton = isMainButton(p.mouse.get_pos())  # returns a number if mouse pos is on button, this number correpsonds to relevant menu screen index
            if highlightMainButton:
                mainscreen = highlightMainButton
            else:
                mainscreen = 25

            if mainButton:  # checks to see if button has been clicked, and adds relevant info to options array
                if mainButton == 32:
                    options[0] = True
                elif mainButton == 33:
                    options[1] = True
                elif mainButton == 34:
                    options[2] = True
                
                mainscreen = mainButton  # if click is inside button, passes dict reference for relevant screen
                mainAnimation = True
                mainButton = False

        elif gameplayMenu:  # if in gameplayMenu
            mainscreen = checkSelected()  # checks which options are selected, returns mainscreen
            button = isGameplayButton(p.mouse.get_pos())  # gets mouse position, checks if it is over button
            if button and gameplayMenuSelect.get((button, mainscreen)):  # checks dict
                mainscreen = gameplayMenuSelect.get((button, mainscreen))
            if gameplayButton in [1, 2, 3]:  # if clicked button is an option, switches relevant options bool
                options[gameplayButton + 2] = not options[gameplayButton + 2]
            elif gameplayButton == 4:  # if back button pressed
                # fade to black 
                MENUS[30].set_alpha(0)
                i = 0
                while i <= 254:
                    i += 2
                    MENUS[30].set_alpha(i)
                    screen.blit(MENUS[30], (0,0))
                    p.display.flip()
                    clock.tick(60)
                runMainMenu(screen)  # runs function again
            elif gameplayButton == 5:  # enter button
                if not options[1]:
                    fadeBlack(screen)
                    mainscreen = 30
                    inMenu = False
                else:
                    MENUS[37].set_alpha(0)
                    i = 0
                    while i <= 255:
                        i += 2
                        MENUS[37].set_alpha(i)
                        screen.blit(MENUS[37], (0,0))
                        p.display.flip()
                        clock.tick(60)
                    gameplayMenu = False
                    colorSelectMenu = True
                    mainscreen = 37
            gameplayButton = False  # resets button

        elif colorSelectMenu:
            color = colorSelect(p.mouse.get_pos())
            mainscreen = 39 if color else 38

        if mainAnimation:
            background = MENUS[35]
            for i in range(150):
                background.set_alpha(i/8)  # incrementally increases background alpha
                screen.blit(background, (0,0))
                p.display.flip()
                clock.tick(60)
            background.set_alpha(255)
            for i in range(150):
                background = p.transform.smoothscale(background, (WIDTH+i/2, HEIGHT+i/2))
                screen.blit(background, (-i/2,-i/2))
                if i > 50:
                    MENUS[30].set_alpha((i-50)*2)
                    screen.blit(MENUS[30], (0,0))
                p.display.flip()
                clock.tick(60)

            MENUS[30].set_alpha(250)
            i = 250
            while i >= 0:
                i -= 2
                MENUS[30].set_alpha(i)
                screen.blit(MENUS[12], (0,0))
                screen.blit(MENUS[30], (0,0))
                p.display.flip()
                clock.tick(60)
            mainMenu = False
            gameplayMenu = True
            mainscreen = 12
            mainAnimation = False

        screen.blit(MENUS[mainscreen], (0, 0))

        if gameplayMenu:  # draws 'tick-box' circles over menu screen to show selected options
            drawCircles(screen)

        p.display.flip()
        clock.tick(30)
