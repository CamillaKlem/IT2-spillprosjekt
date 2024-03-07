import pygame as pg
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT)
import math as m
import random

gameover=False

class Ball:
  """Klasse for å representere en ball"""
  def __init__(self, x, y, radius, farge, vindusobjekt):
    """Konstruktør"""
    self.x = x
    self.y = y
    self.radius = radius
    self.farge = farge
    self.vindusobjekt = vindusobjekt
  
  def tegn(self):
    """Metode for å tegne ballen"""
    pg.draw.circle(self.vindusobjekt, self.farge, (self.x, self.y), self.radius)
  
  def flytt(self):
      if not gameover:
          taster = pg.key.get_pressed()
          if taster[K_UP]:
            self.y -= self.fart
          if taster[K_DOWN]:
            self.y += self.fart
          if taster[K_LEFT]:
            self.x -= self.fart
          if taster[K_RIGHT]:
            self.x += self.fart
  
  def finnAvstand(self, annenBall):
    """Metode for å finne avstanden til en annen ball"""
    xAvstand2 = (self.x - annenBall.x)**2  # x-avstand i andre
    yAvstand2 = (self.y - annenBall.y)**2  # y-avstand i andre
    sentrumsavstand = m.sqrt(xAvstand2 + yAvstand2)

    radiuser = self.radius + annenBall.radius

    avstand = sentrumsavstand - radiuser
    return avstand<=0

class Sverd(Ball):
  def __init__(self, x, y, radius, farge, vindusobjekt, fart):
    super().__init__(x, y, radius, farge, vindusobjekt)
    self.fart=fart
    
 
    
class Spiller(Ball):
  """Klasse for å representere en spiller, arver fra ball"""
  def __init__(self, x, y, radius, farge, vindusobjekt, fart):
    super().__init__(x, y, radius, farge, vindusobjekt)
    self.fart = fart
    

class Monster(Ball):
    def __init__(self, x, y, radius, farge, vindusobjekt, fart):
      super().__init__(x, y, radius, farge, vindusobjekt)
      self.fart = fart
    
    def flyttautomatisk(self):
        if not gameover:
          if ((self.x - self.radius) <= 0) or ((self.x + self.radius) >= self.vindusobjekt.get_width()):
              self.fart = -self.fart
          self.x += self.fart


class Premie(Ball):
    def __init__(self, x, y, radius, farge, vindusobjekt):
      super().__init__(x, y, radius, farge, vindusobjekt)
  
class Infoboks(Ball):
    def __init__(self, x, y, radius, farge, vindusobjekt):
      super().__init__(x, y, radius, farge, vindusobjekt)    
    
class SpillBrett:
    def __init__(self, bredde, høyde):
        self.VINDU_BREDDE : int = bredde
        self.VINDU_HOYDE : int  = høyde
        self.objekter= []
        

    def start_spillet(self):
        pg.init() #starter spillet her
        self.vindu = pg.display.set_mode([self.VINDU_BREDDE, self.VINDU_HOYDE])
        
        self.objekter.append(Spiller(100, 250, 20, (255,192,203), self.vindu, 0.5))
        self.objekter.append(Sverd(100, 250, 10, (192, 192, 192), self.vindu, 0.5))
        self.objekter.append(Monster(23, 80, 20, (255, 0, 0), self.vindu, 0.5))
        self.objekter.append(Infoboks(10, 400, 10, (150, 75, 0), self.vindu))
        
       
        
    def oppdater(self):
        global gameover 
        self.vindu.fill((0, 0, 0))
        
        spiller=self.objekter[0]
        sverd=self.objekter[1]
        monster=self.objekter[2]
        infoboks=self.objekter[3]
        
        if spiller.finnAvstand(infoboks):
            font = pg.font.SysFont("Arial", 30)
            tekst1= "Her må du anrgipe monsteret med sverdet!"
            informasjon = font.render(tekst1, True, (50, 0, 250))
            self.vindu.blit(informasjon, (50, 200))
        
        x=len(self.objekter)
        
        if x==4: 
            for objekt in self.objekter:
                objekt.tegn()
            
            spiller.flytt()
            
            monster.flyttautomatisk()
            
            
            
            if spiller.finnAvstand(sverd):
                sverd.x=spiller.x + 2*sverd.radius
                sverd.y=spiller.y + 2*sverd.radius
                
            if spiller.finnAvstand(monster):
                gameover = True
                font = pg.font.SysFont("Arial", 42)
                bilde = font.render("GAME OVER!", True, (255, 50, 50))
                self.vindu.blit(bilde, (50, 200))
            
            if sverd.finnAvstand(monster):
                self.objekter.insert(4, Premie(250, 250, 20, (0, 0, 255), self.vindu))
                
        else:
            premie=self.objekter[4]
            
            spiller.tegn()
            sverd.tegn()
            premie.tegn()
            infoboks.tegn()
            
            spiller.flytt()
            
            
            if spiller.finnAvstand(sverd):
                sverd.x=spiller.x + 2*sverd.radius
                sverd.y=spiller.y + 2*sverd.radius
                
               
        pg.display.flip() #oppdaterer innholdet

# Lag spillobjekt
spill = SpillBrett(1000,1000)

# Start opp spillet
spill.start_spillet()

# Gjenta helt til brukeren lukker vinduet
fortsett = True
while fortsett:

    # Sjekker om brukeren har lukket vinduet
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False
    
    spill.oppdater()
    
       

# Avslutter pygame
pg.quit()