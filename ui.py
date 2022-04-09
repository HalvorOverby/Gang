import datetime
from time import sleep
import pygame

pygame.init()
def ui(overskrift: str, underskrifter:list,startTid: datetime.datetime,vær: str):
    
    underoverskrifter=["","","",""]
    if len(underskrifter)>0:
        for i in range(min(len(underskrifter),4)):
            underoverskrifter[i]=underskrifter[i]

    white = (255, 255, 255)
    offwhite= (250,250,250)
    black= (0,0,0)
    gray= (116,118,136)
    
    X = 1200   
    Y = 675

    marg=(Y/80)
    largeFontSize=int(X*10/108)
    smallFontSize=int(Y*5/108)


    
    display_surface = pygame.display.set_mode((X, Y))
    tittelfont = pygame.font.SysFont("poppins", largeFontSize)
    underoverskriftfont= pygame.font.SysFont("poppins",smallFontSize)
    
    tittel = tittelfont.render(overskrift, True, black, offwhite)
    underoverskrift1= underoverskriftfont.render(underoverskrifter[0],True,gray,offwhite)
    underoverskrift2= underoverskriftfont.render(underoverskrifter[1],True,gray,offwhite)
    underoverskrift3= underoverskriftfont.render(underoverskrifter[2],True,gray,offwhite)
    underoverskrift4= underoverskriftfont.render(underoverskrifter[3],True,gray,offwhite)
    time=underoverskriftfont.render(startTid.strftime("%H:%M"),True,gray,offwhite)
    
    Recttittel=tittel.get_rect()
    Rectunderoverskrift1=underoverskrift1.get_rect()
    Rectunderoverskrift2=underoverskrift2.get_rect()
    Rectunderoverskrift3=underoverskrift3.get_rect()
    Rectunderoverskrift4=underoverskrift4.get_rect()
    Recttime=time.get_rect()

    Recttittel.topleft = (marg, marg)
    Rectunderoverskrift1.topleft = (2*marg,Recttittel.bottom+marg)
    Rectunderoverskrift2.topleft = (2*marg,Rectunderoverskrift1.bottom+marg) #3*marg+largeFontSize+smallFontSize
    Rectunderoverskrift3.topleft = (2*marg,Rectunderoverskrift2.bottom+marg)
    Rectunderoverskrift4.topleft = (2*marg,Rectunderoverskrift3.bottom+marg)
    Recttime.bottomright=(X-marg*2,Y-marg)
    

    while True:
        display_surface.fill(offwhite)
        display_surface.blit(tittel, Recttittel)
        display_surface.blit(underoverskrift1,Rectunderoverskrift1)
        display_surface.blit(underoverskrift2,Rectunderoverskrift2)
        display_surface.blit(underoverskrift3,Rectunderoverskrift3)
        display_surface.blit(underoverskrift4,Rectunderoverskrift4)
        display_surface.blit(underoverskriftfont.render(datetime.datetime.now().strftime("%H:%M"),True,gray,offwhite),Recttime)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()

ui("Kos deg i dag",["Møte HM","Jobbe med prosjekt","Komme deg i butikken"],datetime.datetime.now(),"sol")