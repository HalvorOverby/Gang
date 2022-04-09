import datetime
import pygame


pygame.init()
def ui(overskrift: str, underskrift:str,startTid: datetime.datetime,vær: str):
    white = (255, 255, 255)
    offwhite= (237,237,236)
    black= (0,0,0)
    gray= (116,118,136)
    
    X = 960    
    Y = 540

    marg=10
    largeFontSize=100
    smallFontSize=50
    
    display_surface = pygame.display.set_mode((X, Y))
    tittelfont = pygame.font.Font("freesansbold.ttf", largeFontSize)
    underoverskriftfont= pygame.font.Font("freesansbold.ttf",smallFontSize)
    
    tittel = tittelfont.render(overskrift, True, black, offwhite)
    underoverskrift= underoverskriftfont.render(underskrift,True,gray,offwhite)
    
    Recttittel=tittel.get_rect()
    Rectunderoverskrift=underoverskrift.get_rect()

    Recttittel.topleft = (marg, marg)
    Rectunderoverskrift.topleft = (marg,2*marg+largeFontSize)
    

    while True:
        display_surface.fill(offwhite)
        display_surface.blit(tittel, Recttittel)
        display_surface.blit(underoverskrift,Rectunderoverskrift)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()

ui("God morgen :D","Memento mori",datetime.datetime.now(),"sol")