import datetime
from time import sleep
import pygame
from weather import weather
from wifi_surv_module import Surveilance
import threading
from news_module import news
from math import ceil

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
    def size(self):
        return len(self.guests)


def ui(overskrift: str, underskrifter:list,startTid: datetime.datetime,vær: weather, nyheter: news):
    pygame.font.get_fonts()
    guests : GuestList = GuestList()
    surv = Surveilance()
    x = threading.Thread(target=surv.surveil, args=(guests,))
    x.start()
    underoverskrifter=["","","","",""]
    if len(underskrifter)>0:
        for i in range(min(len(underskrifter),5)):
            underoverskrifter[i]=underskrifter[i]

    refreshrate=30#every x minute
    update=True
    current_news = str(nyheter)


    trulywhite = (255, 255, 255)
    trulyoffwhite= (250,250,250)
    trulyblack= (0,0,0)
    trulygray= (116,118,136)
    notwhite = (0, 0, 0)
    notoffwhite= (5,5,5)
    notblack= (255,255,255)
    notgray= (139,137,119)
    white = (255, 255, 255)
    offwhite= (250,250,250)
    black= (0,0,0)
    gray= (116,118,136)
    
    X = 1920   
    Y = 1080


    marg=(Y/80)
    largeFontSize=int(200)
    smallFontSize=int(60)
    pageFontSize=30


    
    display_surface = pygame.display.set_mode((X, Y),pygame.FULLSCREEN) 
    tittelfont = pygame.font.SysFont("poppins", largeFontSize)
    underoverskriftfont= pygame.font.SysFont("poppins",smallFontSize)
    sidetallfont=pygame.font.SysFont("poppins",pageFontSize)
    
    tittel = tittelfont.render(overskrift, True, black, offwhite)
    underoverskrift1= underoverskriftfont.render(underoverskrifter[0],True,gray,offwhite)
    underoverskrift2= underoverskriftfont.render(underoverskrifter[1],True,gray,offwhite)
    underoverskrift3= underoverskriftfont.render(underoverskrifter[2],True,gray,offwhite)
    underoverskrift4= underoverskriftfont.render(underoverskrifter[3],True,gray,offwhite)
    underoverskrift5= underoverskriftfont.render(underoverskrifter[4],True,gray,offwhite) 
    time=underoverskriftfont.render(startTid.strftime("%H:%M"),True,gray,offwhite)
    værstatus= underoverskriftfont.render(f"{vær.weatherstatus()}°", True,gray,offwhite)
    værtemp= tittelfont.render(f"{round(vær.temp)}°", True,gray,offwhite )
    symbol=pygame.image.load(f"png/{vær.symbol}.png")
    nyhet=underoverskriftfont.render(current_news,True,gray,offwhite)
    sidetall=sidetallfont.render("",True,gray,offwhite)

    Recttittel=tittel.get_rect()
    Rectunderoverskrift1=underoverskrift1.get_rect()
    Rectunderoverskrift2=underoverskrift2.get_rect()
    Rectunderoverskrift3=underoverskrift3.get_rect()
    Rectunderoverskrift4=underoverskrift4.get_rect()
    Rectunderoverskrift5=underoverskrift5.get_rect() 
    Recttime=time.get_rect()
    RectTemp=værtemp.get_rect()
    RectWeather=værstatus.get_rect()
    RectSymbol=symbol.get_rect()
    Rectnyhet=nyhet.get_rect()
    RectSidetall=sidetall.get_rect()

    Recttittel.topleft = (marg, 0)
    Rectunderoverskrift1.topleft = (2*marg,Recttittel.bottom+marg)
    Rectunderoverskrift2.topleft = (2*marg,Rectunderoverskrift1.bottom+marg) #3*marg+largeFontSize+smallFontSize
    Rectunderoverskrift3.topleft = (2*marg,Rectunderoverskrift2.bottom+marg)
    Rectunderoverskrift4.topleft = (2*marg,Rectunderoverskrift3.bottom+marg)
    Rectunderoverskrift5.topleft = (2*marg,Rectunderoverskrift4.bottom+marg)
    RectSidetall.topright=(1/8*X,Rectunderoverskrift5.bottom+marg)
    Recttime.bottomright=(X-marg*2,Y-marg)
    RectWeather.topright=(X-marg,Recttittel.bottom+largeFontSize+marg+3)
    RectTemp.topleft=(RectWeather.left, Recttittel.bottom)
    RectSymbol.bottomleft=(RectTemp.right+marg,RectWeather.top)
    Rectnyhet.bottomleft=(marg,Recttime.bottom)
    pygame.mouse.set_visible(FALSE)
    
    
    

    i = 0
    guest_i = 0
    sidetall_string = ""
    while True:
    
        if i % 20 == 0:
            if guests.size() > 0:
                guest_i = (guest_i + 4) if (guest_i+4 < guests.size()) else 0
                underoverskrifter[0] = "Tilstede:"
                underoverskrifter = [
                    underoverskrifter[0],
                    "   "+guests.at(guest_i),
                    "   "+guests.at((guest_i + 1)),
                    "   "+guests.at((guest_i + 2)),
                    "   "+guests.at((guest_i + 3)),
                ]
                sidetall_string = str((guest_i//4)+1)+" / "+str(ceil(guests.size()/4)) if guests.size() > 4 else ""

        display_surface.fill(offwhite)
        display_surface.blit(tittelfont.render(overskrift, True, black, offwhite), Recttittel)
        display_surface.blit(underoverskriftfont.render(underoverskrifter[0],True,gray,offwhite),Rectunderoverskrift1)
        display_surface.blit(underoverskriftfont.render(underoverskrifter[1],True,gray,offwhite),Rectunderoverskrift2)
        display_surface.blit(underoverskriftfont.render(underoverskrifter[2],True,gray,offwhite),Rectunderoverskrift3)
        display_surface.blit(underoverskriftfont.render(underoverskrifter[3],True,gray,offwhite),Rectunderoverskrift4)
        display_surface.blit(underoverskriftfont.render(underoverskrifter[4],True,gray,offwhite),Rectunderoverskrift5)
        display_surface.blit(sidetallfont.render(sidetall_string,True,gray,offwhite),RectSidetall)
        display_surface.blit(underoverskriftfont.render((current_news[:57]+"...") if len(current_news) > 60 else current_news ,True,gray,offwhite),Rectnyhet)
        display_surface.blit(underoverskriftfont.render(datetime.datetime.now().strftime("%H:%M"),True,gray,offwhite),Recttime)
        display_surface.blit(tittelfont.render(f"{round(vær.temp)}°", True,gray,offwhite ),RectTemp)
        display_surface.blit(underoverskriftfont.render(vær.weatherstatus(), True,gray,offwhite),RectWeather)
        display_surface.blit(pygame.image.load(f"png/{vær.symbol}.png"),RectSymbol)

        if i % 100 == 0:
            current_news = str(nyheter)

        if update and (datetime.datetime.now().minute%refreshrate==0):
            print("Melding og vær oppdateres")
            vær.updateWeather()
            nyheter.update_news()
            if 5<datetime.datetime.now().hour<11:
                overskrift="God Morgen"
                vær.symbol=vær.next6hoursSymbol
                offwhite=notoffwhite
                gray=notgray
                black=notblack
                white=notwhite
            elif 11<=datetime.datetime.now().hour<18:
                overskrift="God Dag"
                offwhite=notoffwhite
                gray=notgray
                black=notblack
                white=notwhite
            elif 18<=datetime.datetime.now().hour<22:
                overskift="God Kveld"
                offwhite=notoffwhite
                gray=notgray
                black=notblack
                white=notwhite
            else:
                overskift="God Natt"
                offwhite=notoffwhite
                gray=notgray
                black=notblack
                white=notwhite
            update=False
        if datetime.datetime.now().minute%refreshrate==1:
            update=True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        pygame.display.update()
        i += 1
        sleep(0.1)

ui("God Dag",["", "", ""],datetime.datetime.now(),weather(),news())