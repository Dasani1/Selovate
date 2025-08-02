import pygame

BLACK = (0,0,0)

pygame.init()

screenx = 800
screeny = 450
screen_size = [screenx,screeny]

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Selovate")

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)