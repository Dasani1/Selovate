import subprocess
import os
env = os.environ.copy()
env["MKL_THREADING_LAYER"] = "GNU"

import pygame

BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)
GREY = (192,192,192)

pygame.init()

screenx = 800
screeny = 450
screen_size = [screenx,screeny]

screen = pygame.display.set_mode(screen_size,pygame.RESIZABLE) #We want to make the screen size dynamic
pygame.display.set_caption("Selovate")

round = 20

class Button:

    padding = 4

    def __init__(self,box,text,visibility): 
        self.x = box.x
        self.y = box.y

        self.name = text

        self.width = box.width / screenx
        self.height = box.height /screeny
 
        self.held = False

        self.hitbox = box
    
        self.font = self.binary_font(text) #Calls a method to do binary search to find the best size font

        self.text = self.font.render(text,True,BLACK)
        self.text_loc = self.text.get_rect(center=self.hitbox.center)

        self.visibility = visibility

        self.toggle = True #for default

    def binary_font(self,text): #In the name, uses binary search to find which size is the most optimal for the box
        max = self.hitbox.height-4
        min = 5

        optimal = min

        while min <= max:
            mid = (min + max)//2 #IT'S CALLED THE MIDWEST CAUSE EVERYTHING IN IT IS MID
            font = pygame.font.Font('freesansbold.ttf',mid)
            w,h = font.size(text)
            if w + self.padding * 2 <= self.hitbox.width and h <= self.hitbox.height:
                optimal = mid
                min = mid + 1
            else:
                max = mid-1

        return pygame.font.Font('freesansbold.ttf',optimal)
    
    def handle(self,event): #handles all events involving clicking the button
        if self.visibility: #When switching menus I want to make it so that buttons disappear and lose the ability to function until turned back on
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hitbox.collidepoint(event.pos):
                    self.held = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: #Basically it won't activate the click unless the click is released on the button
                if self.held and self.hitbox.collidepoint(event.pos):
                    self.state()

                self.held = False
    
    def state(self):
        if self.name == "Select":
            subprocess.run(['python', 'selector.py'], env=env)

        elif self.name == "Train":
            subprocess.run(['python', 'trainer.py'], env=env)

        elif self.name == "Use":
            subprocess.run(['python', 'user.py'], env=env)

    def draw(self,surface): #If held, turn red, otherwise white
        if self.visibility:
            colour = RED if self.held else GREY
            pygame.draw.rect(surface,colour,self.hitbox,0,round)
            screen.blit(self.text,self.text_loc)

    def setEverything(self): #scaling the screen

        self.hitbox.x = screenx*(self.x/100) #Scale to the size of the screen
        self.hitbox.y = screeny*(self.y/100)

        self.hitbox.width = screenx * self.width
        self.hitbox.height = screeny * self.height

        self.font = self.binary_font(self.name)
        self.text = self.font.render(self.name, True, BLACK)
        self.text_loc = self.text.get_rect(center=self.hitbox.center) #Center hitbox to follow 


    # setters
    def setState(self,state):
        self.state = state

    def setHeld(self,held):
        self.held = held

    # getters
    def getButton(self):
        return self.hitbox
    
    def getState(self): 
        return self.state
    
    def getName(self):
        return self.name
    
    
mutual1=30
mutual2=220
selector = Button(pygame.Rect(5,mutual1,mutual2,mutual2),"Select",True)
trainer = Button(pygame.Rect(35,mutual1,mutual2,mutual2),"Train",True)
user = Button(pygame.Rect(65,mutual1,mutual2,mutual2),"Use",True)

main_screen = [selector,trainer,user]

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
        
    for button in main_screen:
        button.handle(event)
        button.setEverything()
        button.draw(screen)

    screenx, screeny = screen.get_size()

    pygame.display.flip()
    clock.tick(30)