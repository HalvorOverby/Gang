import datetime
from time import sleep
import pygame
from weather import weather
from wifi_surv_module import Surveilance
import threading

pygame.init()

class GuestList:
    def __init__(self):
        self.guests = []
    def get(self):
        return self.guests
    def update(self, new):
        self.guests = new
    def at(self, n):
        if len(self.guests) > n:
            return self.guests[n]
        return ""


def ui(overskrift: str, underskrifter:list,startTid: datetime.datetime,vær: weather):
    pygame.font.get_fonts()
    guests : GuestList = GuestList()
    surv = Surveilance()
    x = threading.Thread(target=surv.surveil, args=(guests,))
    x.start()
    underoverskrifter=["","","",""]
    if len(underskrifter)>0:
        for i in range(min(len(underskrifter),4)):
            underoverskrifter[i]=underskrifter[i]

    refreshrate=2#every x minute
    update=True


    white = (255, 255, 255)
    offwhite= (250,250,250)
    black= (0,0,0)
    gray= (116,118,136)
    
    X = 1920   
    Y = 1020


    marg=(Y/80)
    largeFontSize=int(X*13/108)
    smallFontSize=int(Y*7/108)


    
    display_surface = pygame.display.set_mode((X, Y))
    tittelfont = pygame.font.SysFont("poppins", largeFontSize)
    underoverskriftfont= pygame.font.SysFont("poppins",smallFontSize)
    
    tittel = tittelfont.render(overskrift, True, black, offwhite)
    underoverskrift1= underoverskriftfont.render(underoverskrifter[0],True,gray,offwhite)
    underoverskrift2= underoverskriftfont.render(underoverskrifter[1],True,gray,offwhite)
    underoverskrift3= underoverskriftfont.render(underoverskrifter[2],True,gray,offwhite)
    underoverskrift4= underoverskriftfont.render(underoverskrifter[3],True,gray,offwhite)
    time=underoverskriftfont.render(startTid.strftime("%H:%M"),True,gray,offwhite)
    værstatus= underoverskriftfont.render(f"{vær.weatherstatus()}°", True,gray,offwhite)
    værtemp= tittelfont.render(f"{round(vær.temp)}°", True,gray,offwhite )
    symbol=pygame.image.load(f"png/{vær.symbol}.png")

    Recttittel=tittel.get_rect()
    Rectunderoverskrift1=underoverskrift1.get_rect()
    Rectunderoverskrift2=underoverskrift2.get_rect()
    Rectunderoverskrift3=underoverskrift3.get_rect()
    Rectunderoverskrift4=underoverskrift4.get_rect()
    Recttime=time.get_rect()
    RectTemp=værtemp.get_rect()
    RectWeather=værstatus.get_rect()
    RectSymbol=symbol.get_rect()

    Recttittel.topleft = (marg, 0)
    Rectunderoverskrift1.topleft = (2*marg,Recttittel.bottom+marg)
    Rectunderoverskrift2.topleft = (2*marg,Rectunderoverskrift1.bottom+marg) #3*marg+largeFontSize+smallFontSize
    Rectunderoverskrift3.topleft = (2*marg,Rectunderoverskrift2.bottom+marg)
    Rectunderoverskrift4.topleft = (2*marg,Rectunderoverskrift3.bottom+marg)
    Recttime.bottomright=(X-marg*2,Y-marg)
    RectWeather.topright=(X-marg,Recttittel.bottom+marg+largeFontSize)
    RectTemp.topleft=(RectWeather.left, Recttittel.bottom)
    RectSymbol.bottomright=(RectWeather.right-4*marg,RectWeather.top)
    
    

    i = 0
    while True:
        i += 1
        display_surface.fill(offwhite)
        display_surface.blit(tittelfont.render(overskrift, True, black, offwhite), Recttittel)
        display_surface.blit(underoverskriftfont.render(underoverskrifter[0],True,gray,offwhite),Rectunderoverskrift1)
        display_surface.blit(underoverskriftfont.render(underoverskrifter[1],True,gray,offwhite),Rectunderoverskrift2)
        display_surface.blit(underoverskriftfont.render(underoverskrifter[2],True,gray,offwhite),Rectunderoverskrift3)
        display_surface.blit(underoverskriftfont.render(underoverskrifter[3],True,gray,offwhite),Rectunderoverskrift4)
        display_surface.blit(underoverskriftfont.render(datetime.datetime.now().strftime("%H:%M"),True,gray,offwhite),Recttime)
        display_surface.blit(tittelfont.render(f"{round(vær.temp)}°", True,gray,offwhite ),RectTemp)
        display_surface.blit(underoverskriftfont.render(vær.weatherstatus(), True,gray,offwhite),RectWeather)
        display_surface.blit(pygame.image.load(f"png/{vær.symbol}.png"),RectSymbol)
        
        if i % 10 == 0:
            underoverskrifter[0] = "Gjester:"
            underoverskrifter = [
                underoverskrifter[0],
                "   "+guests.at(0),
                "   "+guests.at(1),
                "   "+guests.at(2)
            ]

        if update and (datetime.datetime.now().minute%refreshrate==0):
            print("Melding og vær oppdateres")
            vær.updateWeather()
            if 5<datetime.datetime.now().hour<11:
                overskrift="God Morgen"
            elif 11<=datetime.datetime.now().hour<18:
                overskrift="God Dag"
            elif 18<=datetime.datetime.now().hour<22:
                overskift="God Kveld"
            else:
                overskift="God Natt"
            update=False
        if datetime.datetime.now().minute%refreshrate==1:
            update=True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()
        sleep(0.1)

ui("God Dag",["", "", ""],datetime.datetime.now(),weather())