import pygame

BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)

pygame.init()

screenx = 800
screeny = 450
screen_size = [screenx,screeny]

round = 20

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Selovate")

class Button:
    def __init__(self,x,y,width,height,type): #Type to identify what purpose the button is used for
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.state = False
        self.held = False
        self.hitbox = pygame.Rect(self.x,self.y,self.width,self.height)

    def draw(self):
        if self.held == True:
            pygame.draw.rect(screen,RED,self.hitbox,0,round)
        else:
            pygame.draw.rect(screen,WHITE,self.hitbox,0,round)

    def setState(self,state):
        self.state = state

    def setHeld(self,held):
        self.held = held
    def getButton(self):
        return self.hitbox
    
    def getState(self): 
        return self.state


clock = pygame.time.Clock()

demo = Button(350,150,100,100,"idk")
demo_list = [demo]
last = 0 #Last saved index so I don't have to iterate twice

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(demo_list)):
                if event.button == 1 and pygame.Rect.collidepoint(demo_list[i].getButton(),event.pos):
                    last = i
                    demo_list[i].setHeld(True)
                    


        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and pygame.Rect.collidepoint(demo_list[last].getButton(),event.pos):
                demo_list[last].setState(True) #Checks if buttons clicked are released in or outside the button
                print("works")

            else:
                demo_list[last].setState(False)

            demo_list[last].setHeld(False)


    screen.fill(BLACK)

    for char in demo_list:
        char.draw()

    pygame.display.flip()

    clock.tick(30)

pygame.quit()