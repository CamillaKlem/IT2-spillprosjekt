import pygame as pg
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT)
import math as m
import random
import tkinter as tk
from tkinter import messagebox


rot = tk.Tk() #kaller funksjonen
rot.withdraw() #fjerner vinduet som dannes, da jeg kun skal ha spill vinduet


gameover=False

class Ball:
  def __init__(self, x, y, radius, farge, vindusobjekt):
    self.x = x
    self.y = y
    self.radius = radius
    self.farge = farge
    self.vindusobjekt = vindusobjekt
  
  def tegn(self):
    pg.draw.circle(self.vindusobjekt, self.farge, (self.x, self.y), self.radius)
  
  def flytt(self):
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
    xAvstand2 = (self.x - annenBall.x)**2 
    yAvstand2 = (self.y - annenBall.y)**2  
    sentrumsavstand = m.sqrt(xAvstand2 + yAvstand2)

    radiuser = self.radius + annenBall.radius

    avstand = sentrumsavstand - radiuser
    return avstand<=0

class Sverd(Ball):
  def __init__(self, x, y, radius, farge, vindusobjekt, fart):
    super().__init__(x, y, radius, farge, vindusobjekt)
    self.fart=fart
    
 
    
class Spiller(Ball):
  def __init__(self, x, y, radius, farge, vindusobjekt, fart):
    super().__init__(x, y, radius, farge, vindusobjekt)
    self.fart = fart

class Infoboks(Ball):
    def __init__(self, x, y, radius, farge, vindusobjekt):
      super().__init__(x, y, radius, farge, vindusobjekt)
    
    
class SpillBrett:
    def __init__(self, bredde, høyde):
        self.VINDU_BREDDE : int = bredde
        self.VINDU_HOYDE : int  = høyde
        self.objekter : Ball = []
        

    def start_spillet(self):
        pg.init() 
        self.vindu = pg.display.set_mode([self.VINDU_BREDDE, self.VINDU_HOYDE])
        
        self.objekter.append(Spiller(100, 250, 20, (255,192,203), self.vindu, 0.5))
        self.objekter.append(Sverd(250, 250, 10, (192, 192, 192), self.vindu, 0.5))
        self.objekter.append(Infoboks(10, 10, 10, (150, 75, 0), self.vindu))
        
       
        
    def oppdater(self):
        global gameover 
        self.vindu.fill((0, 0, 0))
        
        spiller=self.objekter[0]
        sverd=self.objekter[1]
        infoboks=self.objekter[2]
        
       
        for objekt in self.objekter:
            objekt.tegn()
        
        spiller.flytt()
        
        
        if spiller.finnAvstand(sverd):
            sverd.x=spiller.x + 2*sverd.radius
            sverd.y=spiller.y + 2*sverd.radius
            
        
        if spiller.finnAvstand(infoboks):
            font = pg.font.SysFont("Arial", 30)
            informasjon = font.render("Her må du finne sverdet!", True, (50, 0, 250))
            self.vindu.blit(informasjon, (50, 200))
            
            
               
        pg.display.flip() 


spill = SpillBrett(500,500)


spill.start_spillet()

messagebox.showinfo("Introduksjon", "Velkommen til spillet! Her skal du slåss med monstre for å få tak i premien. Det første du skal gjøre er å finne sverdet")


fortsett = True
while fortsett:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False
    
    spill.oppdater()
    
       


pg.quit()
