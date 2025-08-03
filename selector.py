import pygame
import json
import tkinter as tk
from tkinter import filedialog
import os

BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)
GREY = (192,192,192)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
DISPLAY_BOX_MARGIN_X = 0.22  # 10% from left and right
DISPLAY_BOX_MARGIN_Y = 0.22  # 10% from top and bottom


pygame.init()
root = tk.Tk()  
root.withdraw()

FONT = pygame.font.Font(None, 32)
screenx = 800
screeny = 450
screen_size = [screenx,screeny]

answers = {}

round = 20

def upload_folder(): #Open file dialog, return file path
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    root.destroy()
    return folder_path

def images_folder(folder_path):
    images = []
    valid_types = (".png", ".jpg", ".jpeg")
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(valid_types):
            full_path = os.path.join(folder_path, filename)
            try:
                img = pygame.image.load(full_path)
                images.append(( filename, img))
            except pygame.error:
                print(f"Could not load {full_path}")
    return images

uploaded_image = []

screen = pygame.display.set_mode(screen_size,pygame.RESIZABLE) #We want to make the screen size dynamic
pygame.display.set_caption("Selovate")

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
        global uploaded_image
        global iterate

        if self.name == "+": #Creates a pop up input box to input what you want to identify
            if self.toggle:
                add.setVis(True)
                self.toggle = False
            else:
                add.setVis(False)
                self.toggle = True
        
        elif self.name == "-": #Removes the list of identifiers to image train
            if len(identifiers):
                identifiers.pop()
                removed = names.pop()

        elif self.name == "Upload":
            folder_path = upload_folder()

            if folder_path:
                uploaded_image = images_folder(folder_path)

        elif self.name in names:
            name = str(uploaded_image[iterate][0]).split(".")
            answers[name[0]] = self.name
            print(answers)
            

            iterate += 1 

        elif self.name == "Finish":
            file_path = "answers.json"
            with open(file_path,"w") as f:
                json.dump(answers,f)

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

class InputBox:

    def __init__(self, x, y, w, h, text = ""):
        self.rect = pygame.Rect(x, y, w, h) 
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.visibility = False #By default it just needs to be off
        self.x = x / screenx
        self.y = y / screeny
        self.width = w / screenx
        self.height = h / screeny

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

    def rescale(self):
        self.rect.x = (screenx * self.x/100)
        self.rect.y = (screeny * self.y/100)
        self.rect.w = (screenx * self.width/100)
        self.rect.h = (screeny * self.height/100)

        self.txt_surface = FONT.render(self.text, True, self.color)


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
        self.visibility = value

class Create:

    def create(text):

        return Button(pygame.Rect(len(identifiers)*7+5,85,50,50),text,True)

clock = pygame.time.Clock()

add = InputBox(30, 10, 140, 32)

input_boxes = [add]

# set = Button(pygame.Rect(80,10,50,100),"Settings",False) #Later if I even have time
upload = Button(pygame.Rect(80,10,100,50),"Upload",True)
minus = Button(pygame.Rect(10,10,50,50),"-",True)
plus = Button(pygame.Rect(17,10,50,50),"+",True)
finish = Button(pygame.Rect(80,80,100,50),"Finish",True)

main_screen = [minus,plus,upload,finish]

identifiers = []
names = []
iterate = 0

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

    border_x = int(screenx * DISPLAY_BOX_MARGIN_X)
    border_y = int(screeny * DISPLAY_BOX_MARGIN_Y)
    border_width = int(screenx * (1 - 2 * DISPLAY_BOX_MARGIN_X))
    border_height = int(screeny * (1 - 2 * DISPLAY_BOX_MARGIN_Y))

    image_area = pygame.Rect(border_x, border_y, border_width, border_height)

    pygame.draw.rect(screen, (200, 200, 200), image_area, border_radius=10)

    if uploaded_image:
        original = uploaded_image[iterate][1]
        orig_width, orig_height = original.get_size()
        ratio_x = border_width / orig_width
        ratio_y = border_height / orig_height
        scale = min(ratio_x, ratio_y)
        scaled_width = int(orig_width * scale)
        scaled_height = int(orig_height * scale)
        scaled_image = pygame.transform.scale(original, (scaled_width, scaled_height))

        image_x = border_x + (border_width - scaled_width) // 2
        image_y = border_y + (border_height - scaled_height) // 2
        screen.blit(scaled_image, (image_x, image_y))

    pygame.display.flip()

    clock.tick(30)
