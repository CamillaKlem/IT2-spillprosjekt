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
  
  def finnAvstand(self, annenBall):
    """Metode for å finne avstanden til en annen ball"""
    xAvstand2 = (self.x - annenBall.x)**2  # x-avstand i andre
    yAvstand2 = (self.y - annenBall.y)**2  # y-avstand i andre
    sentrumsavstand = m.sqrt(xAvstand2 + yAvstand2)

    radiuser = self.radius + annenBall.radius

    avstand = sentrumsavstand - radiuser
    return avstand<=0

class Sløyfe(Ball):
  def __init__(self, x, y, radius, farge, vindusobjekt):
    super().__init__(x, y, radius, farge, vindusobjekt)

class Hinder(Ball):
  def __init__(self, x, y, radius, farge, vindusobjekt, fart):
    super().__init__(x, y, radius, farge, vindusobjekt)
    self.fart = fart

  def flytt(self):
      if not gameover:
          if ((self.x - self.radius) <= 0) or ((self.x + self.radius) >= self.vindusobjekt.get_width()):
              self.fart = -self.fart
          self.x += self.fart
    

class Troll(Ball):
  """Klasse for å representere en spiller, arver fra ball"""
  def __init__(self, x, y, radius, farge, vindusobjekt, fart):
    super().__init__(x, y, radius, farge, vindusobjekt)
    self.fart = fart

  def flytt(self):
      if not gameover:
        """Metode for å flytte spilleren"""
        taster = pg.key.get_pressed()
        if taster[K_UP]:
          self.y -= self.fart
        if taster[K_DOWN]:
          self.y += self.fart
        if taster[K_LEFT]:
          self.x -= self.fart
        if taster[K_RIGHT]:
          self.x += self.fart
          
          
class SpillBrett:
    def __init__(self, bredde, høyde):
        # Konstruktør og attributter med type-informasjon
        self.VINDU_BREDDE : int = bredde
        self.VINDU_HOYDE : int  = høyde
        self.objekter : Ball = []
        self.poeng=0

    def start_spillet(self):
        pg.init() #starter spillet her
        self.vindu = pg.display.set_mode([self.VINDU_BREDDE, self.VINDU_HOYDE])
        
        self.objekter.append(Troll(100, 250, 20, (0, 255, 0), self.vindu, 0.09))
        self.objekter.append(Hinder(250, 250, 20, (250, 50, 50), self.vindu, 0.09))
        #self.objekter.append(Sløyfe(random.randint(0, 500), random.randint(0, 500), 20, (0, 0, 255), self.vindu))#lager et hinder og legger den i objekter lista over    
        
        
    def oppdater(self):
        global gameover 
        self.vindu.fill((0, 0, 0))
        
        trollet=self.objekter[0]
        hinder=self.objekter[1]
       
        for objekt in self.objekter:
            objekt.tegn()
            objekt.flytt()
            
        font = pg.font.SysFont("Arial", 42) 
        tekst = f"Poengsum: {self.poeng}"
        bilde = font.render(tekst, True, (255, 255, 255))
        self.vindu.blit(bilde, (0, 0))
        
        if trollet.finnAvstand(hinder):
            gameover = True 
            bilde = font.render("GAME OVER!", True, (255, 50, 50))
            self.vindu.blit(bilde, (50, 200))          
            
                      
        
            
               
        pg.display.flip() #oppdaterer innholdet

# Lag spillobjekt
spill = SpillBrett(500,500)

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