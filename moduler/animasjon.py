def animate(levels, params, DELTA_T, rnd):
    '''
    Funksjon som animerer nivået til fire tanker.
    Inn-parameterne er fire dictionaries for nivåene til tankene,
    parameterne til tankene, tidssteget for euler (DELTA_T)
    og antall desimaler for tidslagringen.
    '''
    import pygame, sys, os
    pygame.init() 
    pygame.display.set_caption("Tanksimulering - Eulers metode")

    # Definerer noe universelle variabler
    speedfactor = 1
    speed = 1000 / speedfactor
    run = True
    img = pygame.image.load(os.path.join("data",os.path.dirname(os.path.abspath(__file__)),"arrow.png"))
    img = pygame.transform.scale(img, (50, 50))

    #Farger
    GRAY = (50,50,50)
    WHITE = (255,255,255)
    SEA_BLUE = (0,105,148)
    SEA_BLUE_DARK = (0,78,109)
    GREEN = (0,255,0)
    RED = (255,0,0)
    GREEN_DARK = (0,125,0)
    RED_DARK = (125,0,0)

    #Dimensjoner på programvindu
    SIZE = WIDTH,HEIGHT = 1280,720
    screen = pygame.display.set_mode(SIZE)
    CENTER_HORIZ = WIDTH // 2
    CENTER_VERT = HEIGHT // 2

    #Bilder per sekund
    FPS = 10
    timer = pygame.time.Clock()
    ui_txt = pygame.font.SysFont('Consolas', 22)
    ui_txt_small = pygame.font.SysFont('Consolas', 14)

    # Definerer variablene til tankene
    tank1 = {
        "top": 120,
        "left": 900,
        "dm-top": 120,
        "dm-bot": 100,
        "height": 100,
        "h0": 100,
        "levels": levels[0],
        "params": params[0]
    }
    tank2 = {
        "top": 250,
        "left": 750,
        "dm-top": 150,
        "dm-bot": 120,
        "height": 120,
        "h0": 120,
        "levels": levels[1],
        "params": params[1]
    }
    tank3 = {
        "top": 400,
        "left": 600,
        "dm-top": 150,
        "dm-bot": 150,
        "height": 100,
        "h0": 100,
        "levels": levels[2],
        "params": params[2]
    }
    tank4 = {
        "top": 530,
        "left": 400,
        "dm-top": 200,
        "dm-bot": 150,
        "height": 170,
        "h0": 170,
        "levels": levels[3],
        "params": params[3]
    }

    tanks = [tank1,tank2,tank3,tank4] # Liste med alle tankene
    time = 0 # Tiden i sekunder
    level_time = 0 # "Hentetiden" til bruk for å hente høyden fra dictionariene
    pause = False # Pausevariabel for simuleringen
    while run:
        screen.fill(GRAY) # Renser skjermen fra forrige bilde

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Løkke som henter høyden gitt tiden og tegner tankene med tekst
        for index, tank in enumerate(tanks):
            if level_time in tank["levels"]:
                tank["height"] = (tank["levels"][level_time] / 
                                  tank["params"]["h_max"]) * tank["h0"]
                #draw info on current height
                screen.blit(ui_txt_small.render(
                            "Høyde: {}cm".format(round(tank["levels"][level_time],2)),True,WHITE),
                            [tank["left"]+tank["dm-top"]+10, tank["top"]+tank["h0"]-tank["height"]])
                #draw arrow
                screen.blit(img, (tank["left"]-60, tank["top"]+tank["h0"]-30))

            elif level_time > list(tank["levels"].values())[-1]:
                tank["height"] = (list(tank["levels"].values())[-1] / 
                                       tank["params"]["h_max"]) * tank["h0"]
                #draw info on current height
                screen.blit(ui_txt_small.render(
                            "Høyde: {}cm".format(round(list(tank["levels"].values())[-1],2)),True,WHITE),
                            [tank["left"]+tank["dm-top"]+10, tank["top"]+tank["h0"]-tank["height"]])
            
            else:
                #draw info on current height
                screen.blit(ui_txt_small.render(
                            "Høyde: {}cm".format(round(list(tank["levels"].items())[-1][1],2)),True,WHITE),
                            [tank["left"]+tank["dm-top"]+10, tank["top"]+tank["h0"]-tank["height"]])

            r = (tank["dm-bot"]/2) + (((tank["dm-top"] - tank["dm-bot"])/2) / (tank["h0"])) * tank["height"]
            h = tank["height"]
            #draw tank
            pygame.draw.polygon(screen, (SEA_BLUE), [
                [tank["left"]+tank["dm-top"]/2-r,tank["top"]+tank["h0"]-h], # Top left
                [tank["left"]+(tank["dm-top"]-tank["dm-bot"])/2,tank["top"]+tank["h0"]], # Bottom left
                [tank["left"]+(tank["dm-top"]-tank["dm-bot"])/2+tank["dm-bot"],tank["top"]+tank["h0"]], # Bottom right
                [tank["left"]+tank["dm-top"]//2+r,tank["top"]+tank["h0"]-h]] # Top right
            )
            pygame.draw.polygon(screen, (WHITE), [[tank["left"],tank["top"]],
            [tank["left"]+(tank["dm-top"]-tank["dm-bot"])/2, tank["top"]+tank["h0"]],
            [tank["left"]+(tank["dm-top"]-tank["dm-bot"])/2 + tank["dm-bot"],tank["top"]+tank["h0"]], 
            [tank["left"]+tank["dm-top"],tank["top"]]],
            4)
            #draw info on tank
            screen.blit(ui_txt_small.render("Tank {}"         .format(index+1),                          True,WHITE), [tank["left"]-60,tank["top"]-100])
            screen.blit(ui_txt_small.render("Maks høyde: {}cm".format(tank["params"]["h_max"]),          True,WHITE), [tank["left"]-60,tank["top"]-85])
            screen.blit(ui_txt_small.render("Starthøyde: {}cm".format(tank["params"]["h_0"]),            True,WHITE), [tank["left"]-60,tank["top"]-70])
            screen.blit(ui_txt_small.render("Stopphøyde: {}cm".format(tank["params"]["h_1"]),            True,WHITE), [tank["left"]-60,tank["top"]-55])
            screen.blit(ui_txt_small.render("C: {}"           .format(tank["params"]["C"]),              True,WHITE), [tank["left"]-60,tank["top"]-40])
            screen.blit(ui_txt_small.render("Hull: {}cm^2"    .format(round(tank["params"]["A_hole"],4)),True,WHITE), [tank["left"]-60,tank["top"]-25])

        # Progressbar (kan brukes ved å klikke og dra med musa for å stille tiden)
        pygame.draw.rect(screen, GREEN, pygame.Rect(50, 110, 30, 500))

        # Tegner knapper
        speedUp_button = pygame.draw.rect(screen, GREEN, pygame.Rect(150, 150, 125, 50))
        speedDown_button = pygame.draw.rect(screen, RED, pygame.Rect(150, 210, 125, 50))
        screen.blit(ui_txt.render("Øk fart", True, GRAY), (172, 165))
        screen.blit(ui_txt.render("Senk fart", True, GRAY), (160, 225))
        pause_button = pygame.draw.rect(screen, SEA_BLUE, pygame.Rect(150, 270, 125, 50))
        if pause:
            screen.blit(ui_txt.render("Fortsett", True, WHITE), (166, 285))
        else:
            screen.blit(ui_txt.render("Pause", True, WHITE), (182, 285))

        # Sjekker om knapper blir presset
        pos = pygame.mouse.get_pos()
        p1, p2, p3 = pygame.mouse.get_pressed()
        if speedUp_button.collidepoint(pos):
            pygame.draw.rect(screen, GREEN_DARK, pygame.Rect(150, 150, 125, 50))
            screen.blit(ui_txt.render("Øk fart", True, WHITE), (172, 165))
            if p1:
                speedfactor += 1
        if speedDown_button.collidepoint(pos):
            pygame.draw.rect(screen, RED_DARK, pygame.Rect(150, 210, 125, 50))
            screen.blit(ui_txt.render("Senk fart", True, WHITE), (160, 225))
            if p1 and speedfactor-1 > 0:
                speedfactor -= 1
        if pause_button.collidepoint(pos):
            pygame.draw.rect(screen, SEA_BLUE_DARK, pygame.Rect(150, 270, 125, 50))
            if pause:
                screen.blit(ui_txt.render("Fortsett", True, WHITE), (166, 285))
            else:
                screen.blit(ui_txt.render("Pause", True, WHITE), (182, 285))
            pause =  p1 ^ pause
        # Tegner omriss av knappene
        pygame.draw.rect(screen, WHITE, pygame.Rect(150, 150, 125, 50),2)
        pygame.draw.rect(screen, WHITE, pygame.Rect(150, 210, 125, 50),2)
        pygame.draw.rect(screen, WHITE, pygame.Rect(150, 270, 125, 50),2)
        
        # Sjekker om man drar i progressbaren
        pos_x = pos[0]
        pos_y = pos[1]
        if pos_x >= 50 and pos_x <= 80 and p1:
            if pos_y < 110: time = 0
            elif pos_y > 610: time = list(levels[3].keys())[-1]
            else:
                pygame.draw.rect(screen, WHITE, pygame.Rect(50, 110, 30, 500))
                pygame.draw.rect(screen, GREEN, pygame.Rect(50, pos_y, 30, 610 - pos_y))
                time = round(list(levels[3].keys())[-1] * (pos_y - 110) / 500)
        if pause == False and time < list(levels[3].keys())[-1]+DELTA_T:
            time += (1/FPS)*speedfactor
            level_time = round(time,rnd)

        # Tegner progressbaren
        if round(time) < list(levels[3].keys())[-1]:
            px = (round(time) / list(levels[3].keys())[-1] * 500)
        else:
            px = 500
        pygame.draw.rect(screen, WHITE, pygame.Rect(50, 110, 30, px))

        # Viser tiden og simuleringsfart
        screen.blit(ui_txt.render("Medgått tid: {}s = {}min".format(round(time,2),round(time/60,2)),True,WHITE,), [10,10])
        screen.blit(ui_txt.render("Simuleringsfart: {}x".format(speedfactor), True, WHITE), [10, 50])

        # Oppdaterer skjermen og setter antall bilder per sekund
        pygame.display.flip()
        timer.tick(FPS)
