import pygame
import sys

pygame.init()

# Definerer skjermstørrelse og farger
screen_width = 500
screen_height = 500
white = (255, 255, 255)

# Oppretter skjermobjektet
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spillerens bilde")

# Last inn bildet av spilleren
player_image = pygame.image.load("player_image.png")
player_rect = player_image.get_rect()
player_rect.center = (screen_width // 2, screen_height // 2)

# Definerer bevegelseshastighet
player_speed = 5

# Spillloopen
running = True
while running:
    screen.fill(white)
    
    # Hendelsesbehandling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Sjekk for tastetrykk
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed
    
    # Tegn spillerens bilde på skjermen
    screen.blit(player_image, player_rect)
    
    pygame.display.flip()

pygame.quit()
sys.exit()