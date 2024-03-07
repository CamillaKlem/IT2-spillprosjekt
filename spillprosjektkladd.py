import pygame as pg
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT)
import math as m
import random

gameover=False

class Spillobjekt:
  def __init__(self, x, y, radius, farge, vindusobjekt):
    self.x = x
    self.y = y
    self.radius = radius
    self.farge = farge
    self.vindusobjekt = vindusobjekt
  
  def tegn(self):
    pg.draw.circle(self.vindusobjekt, self.farge, (self.x, self.y), self.radius) 
  
  def kollisjon(self, annenBall):
    xAvstand2 = (self.x - annenBall.x)**2  
    yAvstand2 = (self.y - annenBall.y)**2  
    sentrumsavstand = m.sqrt(xAvstand2 + yAvstand2)

    radiuser = self.radius + annenBall.radius

    avstand = sentrumsavstand - radiuser
    
    return avstand<=0

class Spiller(Spillobjekt):
  def __init__(self, x, y, bilde, vindusobjekt, fart):
        self.bilde = bilde
        self.rect = self.bilde.get_rect(center=(x, y))
        self.vindusobjekt=vindusobjekt
        self.fart = fart
        self.poeng = 0

  def flytt(self):
      if not gameover:
            taster = pg.key.get_pressed()
            if taster[K_UP] and self.rect.top > 0:
                self.rect.y -= self.fart
            if taster[K_DOWN] and self.rect.bottom < self.vindusobjekt.get_height():
                self.rect.y += self.fart
            if taster[K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.fart
            if taster[K_RIGHT] and self.rect.right < self.vindusobjekt.get_width():
                self.rect.x += self.fart
                
            self.x = self.rect.centerx
            self.y = self.rect.centery
            

class Fiende(Spillobjekt):    
    def __init__(self, x, y, radius, farge, vindusobjekt, xFart, yFart):
        super().__init__(x, y, radius, farge, vindusobjekt)
        self.xFart = xFart
        self.yFart = yFart
    
    
    def flytt(self):
      if not gameover:
        if ((self.x - self.radius) <= 0) or ((self.x + self.radius) >= self.vindusobjekt.get_width()):
          self.xFart = -self.xFart
          
        if ((self.y - self.radius) <= 0) or ((self.y + self.radius) >= self.vindusobjekt.get_height()):
          self.yFart = -self.yFart
          
        self.x += self.xFart
        self.y += self.yFart
        
    
           
class SpillBrett:
    def __init__(self, bredde, høyde):
        self.VINDU_BREDDE : int = bredde
        self.VINDU_HOYDE : int  = høyde
        self.objekter = []
        self.ballobjekter = []
        self.poeng=0
        

    def start_spillet(self):
        pg.init() #starter spillet her
        self.vindu = pg.display.set_mode([self.VINDU_BREDDE, self.VINDU_HOYDE])
        # Lager et Spiller-objekt, den henter fra spiller
        spiller_bilde = pg.image.load("spiller.png").convert_alpha()

        # Lag et Spiller-objekt og legg det til i objekter-listen
        self.objekter.append(Spiller(200, 200, spiller_bilde, self.vindu, 5))
        
        
        for i in range(50):
            self.ballobjekter.append(Fiende(random.randint(0, 1300), random.randint(0, 800), 15, (40, 60, 255), self.vindu, 0.08, 0.3))#lager et hinder og legger den i objekter lista over    
    
        
    
    def oppdater(self):
        global gameover
        
        
        self.vindu.fill((0, 0, 0))
        
        for objekt in self.objekter:
            if isinstance(objekt, Spiller):
                self.vindu.blit(objekt.bilde, objekt.rect)
                objekt.flytt()
            else:
                objekt.tegn()
                objekt.flytt()
        
        for objekt in self.ballobjekter:
            objekt.tegn()
            
        
        font = pg.font.SysFont("Arial", 42)
        tekst = f"Poengsum: {self.poeng}"
        poengoversikt = font.render(tekst, True, (255, 255, 255))
        self.vindu.blit(poengoversikt, (700, 700))
            
        pg.display.flip() #oppdaterer innholdet

# Lag spillobjekt
spill = SpillBrett(1300, 700)

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
        

    