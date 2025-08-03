import pygame
import sys

BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

pygame.init()

FONT = pygame.font.Font(None, 32)
screenx = 800
screeny = 450
screen_size = [screenx,screeny]

round = 20

screen = pygame.display.set_mode(screen_size,pygame.RESIZABLE) #We want to make the screen size dynamic
pygame.display.set_caption("Selovate")

class Button:

    padding = 4

    def __init__(self,box,text,visibility): 
        self.x = box.x
        self.y = box.y

        self.name = text

        self.width = box.width
        self.height = box.height
 
        self.held = False

        self.hitbox = box
    
        self.font = self.binary_font(text) #Calls a method to do binary search to find the best size font

        self.text = self.font.render(text,True,BLACK)
        self.text_loc = self.text.get_rect(center=self.hitbox.center)

        self.visibility = visibility

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
    
    def handle(self,event):
        if self.visibility: #When switching menus I want to make it so that buttons disappear and lose the ability to function until turned back on
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hitbox.collidepoint(event.pos):
                    self.held = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: #Basically it won't activate the click unless the click is released on the button
                if self.held and self.hitbox.collidepoint(event.pos):
                    self.state()

                self.held = False
    
    def state(self):
        if self.name == "+": #Creates a pop up input box to input what you want to identify
            add.setVis(True)
        
        elif self.name == "-": #Removes the list of identifiers to image train
            if len(identifiers):
                identifiers.pop()

        

    def draw(self,surface): #If held, turn red, otherwise white
        if self.visibility:
            colour = RED if self.held else WHITE
            pygame.draw.rect(surface,colour,self.hitbox,0,round)
            screen.blit(self.text,self.text_loc)

    # def create(self,name):
    #     return Button(pygame.Rect(10,80,50,50),name,True)

    def setEverything(self):

        self.hitbox.x = screenx*(self.x/100) #Scale to the size of the screen, will implement size soon
        self.hitbox.y = screeny*(self.y/100)

        # self.hitbox.width = screenx*(self.x/100)
        # self.hitbox.height = screenx*(self.x/100)
        # self.binary_font(self.name)

        self.text_loc.center = self.hitbox.center #Update the text to follow rect

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

class InputBox:

    def __init__(self, x, y, w, h, text = ""):
        self.rect = pygame.Rect(x, y, w, h) 
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.visibility = False

    def handle_event(self, event):
        if self.visibility:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active

                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.text = self.text.strip()
                        if self.text not in names:
                            names.append(self.text) #Made sure no duplicates are allowed
                            identifiers.append(Create.create(self.text))
                        
                        self.text = ''
   
    
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]

                    else:
                        self.text += event.unicode

                    # Re-render the text.
                    self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        if self.visibility:
            # Blit the text.
            screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
            # Blit the rect.
            pygame.draw.rect(screen, self.color, self.rect, 2)

    def getVal(self):
        return self.text

    def setVal(self,word):
        self.text = word

    def setVis(self,value=bool):
        if value == True:
            self.visibility = True

class Create:

    def create(text):

        return Button(pygame.Rect(len(identifiers)*10+5,75,75,75),text,True)

clock = pygame.time.Clock()

add = InputBox(100, 200, 140, 32)

input_boxes = [add]

set = Button(pygame.Rect(80,10,50,100),"Settings",True)
minus = Button(pygame.Rect(10,10,50,50),"-",True)
plus = Button(pygame.Rect(17,10,50,50),"+",True)

main_screen = [set,minus,plus]

identifiers = []
names = []

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for button in main_screen:
            button.handle(event)
        
        if len(identifiers) != 0:
            for identity in identifiers:
                identity.handle(event)

        for box in input_boxes:
            box.handle_event(event)
    
    for box in input_boxes:
        box.update()

    screen.fill(BLACK)

    screenx, screeny = screen.get_size()

    for char in main_screen:
        char.setEverything()
        char.draw(screen)

    for box in input_boxes:
        box.draw(screen)

    if len(identifiers) != 0:
        for keys in identifiers:
            keys.setEverything()
            keys.draw(screen)

    pygame.display.flip()

    clock.tick(30)

pygame.quit()