from serial import *
import serial.tools.list_ports

# import os
# import sys
# sys.path.append(os.getcwd())
# from pygame_textinput_custom import *
from pygame_widgets.textbox import *
import pygame_widgets as pw

import pygame as pg
import time
from pygame.locals import *
import pygame.locals as pl
from win32gui import SetWindowPos
import os
import re

ports = sorted(serial.tools.list_ports.comports())
i = 1
print("\n")
for elem in ports:
  print(i, " - " + elem[0])
  i = i + 1
selectedPort = input("Select COM port option: ")
if selectedPort == '':
    pass
else:
    comPort = ports[int(selectedPort) - 1][0]
    
    serialPort = Serial(comPort, 9600, timeout=0, writeTimeout=0)

pg.init()
h=700
w=1000
icon = pg.image.load(os.getcwd()+'\\nanopen_icon.png')
pg.display.set_icon(icon)
screen = pg.display.set_mode((w, h))
pg.display.set_caption('Nanopen Manipulator')
SetWindowPos(pg.display.get_wm_info()['window'], -1, 300, 30, 0, 0, 1)
# pygame setup
pg.init()
clock = pg.time.Clock()
running = True
print("Starting game")
to_print=''
font = pg.font.SysFont('Arial', 40)
objects=[]

class KeyInput(): # button class
        def __init__(self, x, y, width, height, Text='Button', size=100, Key=None, onePress=False):
            self.key_font = pg.font.SysFont('Arial', size)
            self.size = size
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.Key = Key
            self.Text = Text
            self.onePress = onePress
            self.alreadyPressed = False
            self.keys = [pg.K_1,pg.K_2,pg.K_3,pg.K_4,pg.K_5]
            self.fillColors = {
                'normal': '#E8E8E8',
                'pressed': '#B1B1B1'
            }
            
            self.buttonSurface = pg.Surface((self.width, self.height))
            self.buttonRect = pg.Rect(self.x, self.y, self.width, self.height)

            if self.Key in self.keys:
                if self.alreadyPressed:
                    status = 'Active'
                else:
                    status = 'Inactive'
                self.buttonSurf = self.key_font.render(self.Text+status, True, (20, 20, 20))
            else:
                self.buttonSurf = self.key_font.render(self.Text, True, (20, 20, 20))
    
            objects.append(self)
            #print(self.keys)

    
        def process(self):
            keyPress = pg.key.get_pressed()
            # if keyPress[self.Key]:
            #     print(self.Key, end='\r')
            keys_truth=[]
            for i in self.keys:
                keys_truth.append(keyPress[i])
            if self.Key in self.keys:
                if keyPress[self.Key]:
                    self.alreadyPressed = True
                    self.buttonSurface.fill(self.fillColors['pressed'])
                elif any(keys_truth):
                    self.alreadyPressed = False
                    self.buttonSurface.fill(self.fillColors['normal'])
            else:
                self.buttonSurface.fill(self.fillColors['normal'])
            if keyPress[self.Key]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.alreadyPressed = True

            if self.Key in self.keys:
                if self.alreadyPressed:
                    status_text = 'Active'
                    self.buttonSurface.fill(self.fillColors['pressed'])
                else:
                    self.buttonSurface.fill(self.fillColors['normal'])
                    status_text = 'Inactive'

        def blit_proc(self):
            if self.Key in self.keys:
                if self.alreadyPressed:
                    status = 'Active'
                else:
                    status = 'Inactive'
                self.buttonSurf = self.key_font.render(self.Text+status, True, (20, 20, 20))
            else:
                self.buttonSurf = self.key_font.render(self.Text, True, (20, 20, 20))
            self.buttonSurface.blit(self.buttonSurf, [
                self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
                self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
            ])
            screen.blit(self.buttonSurface, self.buttonRect)


try: # buttons
    class wasd_input():
        def __init__(self, h, w, key_h, key_w, spacing, posx, posy):
            self.key_h=key_h
            self.key_w=key_w
            self.spacing=spacing
            self.totw=key_w*3+2*spacing
            self.toth=key_h*2+spacing
            self.posx=posx#(w-totw)/1.5
            self.posy=posy
            KeyInput(self.posx+self.key_w+self.spacing, self.posy-self.key_h-self.spacing, self.key_w, key_h, '↑', 100, pg.K_w)
            KeyInput(self.posx, self.posy, self.key_w, self.key_h, '←', 100, pg.K_a)
            KeyInput(self.posx+self.key_w+self.spacing, self.posy, self.key_w, self.key_h, '↓', 100, pg.K_s)
            KeyInput(self.posx+2*self.key_w+2*self.spacing, self.posy, self.key_w, self.key_h, '→', 100, pg.K_d)
    wasd = wasd_input(h,w,125,100,25,25,h-150)
    wasd

    def speed_input(h,w):
        key_h=40
        key_w=350
        spacing=25
        totw=key_w*3+2*spacing
        toth=key_h*5+spacing*4
        posx=25
        posy=25
        KeyInput(posx,posy,key_w,key_h,'Speed Setting 1: ', 30, pg.K_1)
        KeyInput(posx,posy+key_h+spacing,key_w,key_h,'Speed Setting 2: ', 30, pg.K_2)
        KeyInput(posx,posy+2*(key_h+spacing),key_w,key_h,'Speed Setting 3: ', 30, pg.K_3)
        KeyInput(posx,posy+3*(key_h+spacing),key_w,key_h,'Speed Setting 4: ', 30, pg.K_4)
        KeyInput(posx,posy+4*(key_h+spacing),key_w,key_h,'Speed Setting 5: ', 30, pg.K_5)
    speed_input(h,w)

    KeyInput(wasd.posx,400,75,40,'Step',30, pg.K_LCTRL)
except Exception as e: print(e)

x=688
y=380
max=4
step=0.2
upper_edge=False
lower_edge=False
right_edge=False
left_edge=False
radius=5

def drawBorder(surface, x, y, h, w, border_color, fill_color, radius, curved):
    pg.draw.rect(surface, border_color, (x,y,h,w), radius, curved)
    # for i in range(4):
    #     pygame.draw.rect(surface, border_color, (x-i,y-i,h,w), 1)


# # Text inputs
# try:
#     text_inputs=[]
#     # Pygame now allows natively to enable key repeat:
#     pg.key.set_repeat(200, 25)

#     COLOR_INACTIVE = pg.Color('lightskyblue3')
#     COLOR_ACTIVE = pg.Color('dodgerblue2')
#     class TextInput():
#         def __init__(self, posx, posy):
#             self.posx=posx
#             self.posy=posy
#             self.active = False
#             # But more customization possible: Pass your own font object
#             self.font = pg.font.SysFont("Arial", 25)
#             # Create own manager with custom input validator
#             self.manager = TextInputManager(validator = lambda input: len(input) <= 6 and input.isdigit() or input=='')
#             # Pass these to constructor
#             self.visualizer = TextInputVisualizer(manager=self.manager, font_object=self.font)
#             # Customize much more
#             self.visualizer.cursor_width = 2
#             self.visualizer.cursor_blink_interval = 400 # blinking interval in ms
#             self.visualizer.antialias = True
#             self.visualizer.font_color = (20, 20, 20)
#             self.dummy_surface = pg.Rect(self.posx, self.posy, 
#                        self.visualizer.surface.get_width(), 
#                        self.visualizer.surface.get_height())
            
#             text_inputs.append(self)
        
#         def process(self):
#             self.dummy_surface = pg.Rect(self.posx, self.posy, 
#                                    self.visualizer.surface.get_width(), 
#                                    self.visualizer.surface.get_height())
#             pg.draw.rect(screen, "RED", self.dummy_surface, 2)
#             drawBorder(screen, self.posx-2, self.posy-2, 
#                        self.visualizer.surface.get_width()-2, 
#                        self.visualizer.surface.get_height()+4, 
#                        "BLACK", "BLACK", 1, 0)
#             screen.blit(self.visualizer.surface, (self.posx, self.posy))

#         def handle_event(self, pos):
#             # If the user clicked on the input_box rect.
#             if self.dummy_surface.collidepoint(pos):
#                 print('Click!\n')
#                 # Toggle the active variable.
#                 self.active = not self.active
#             else:
#                 self.active = False
#             # Change the current color of the input box.
#             self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
#             if event.type == pg.KEYDOWN:
#                 if self.active:
#                     if event.key == pg.K_RETURN:
#                         print(self.visualizer.value+'\n')
#     TextInput(600, 65)
#     TextInput(800, 65)
# except Exception as e: print(e)

try:
    def output():
        # Get text in the textbox
        print(width_box.getText())
    
    width_box = TextBox(screen, 600, 55, 125, 40, fontSize=25, font="arial",
                   placeholderText='Width (mm)', placeholderTextColour='#8E8D8D',
                  borderColour="BLACK", textColour="BLACK",
                  onSubmit=output, radius=0, borderThickness=1)
    # height_box = TextBox(screen, 800, 55, 125, 40, fontSize=25, font="arial",
    #                placeholderText='Length (mm)', placeholderTextColour='#8E8D8D',
    #               borderColour="BLACK", textColour="BLACK",
    #               onSubmit=output, radius=0, borderThickness=1)
except Exception as e: print(e)

while running:
    # poll for events
    events = pg.event.get()
    # pygame.QUIT event means the user clicked X to close your window
    keys = pg.key.get_pressed()

    # Feed it with events every frame
    # for text_input in text_inputs:
    #     text_input.visualizer.update(events)
    
    for event in pg.event.get():
        try:
            if event.type == pg.QUIT:
                running = False
                
            if event.type == pg.KEYDOWN:
                if keys[pg.K_LCTRL]:
                    if keys[pg.K_w]:
                        y-=1
                    if keys[pg.K_a]:
                        x-=1
                    if keys[pg.K_s]:
                        y+=1
                    if keys[pg.K_d]:
                        x+=1
        except Exception as e: print(e)
            

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    try:
        # for i in events:
        #     if i.type == pg.MOUSEBUTTONDOWN:
        #         print(i.pos)
        #         for text_input in text_inputs:
        #             text_input.handle_event(event.pos)
        if keys[pg.K_q]:
            pg.QUIT
            print("Closing game                             ")
            running = False
            
        for object in objects:
            object.blit_proc()

        for object in objects:
            object.process()

        if not keys[pg.K_LCTRL]:
            if keys[pg.K_w] and not upper_edge:
                y-=round(step*max,0)
            if keys[pg.K_a] and not left_edge:
                x-=round(step*max,0)
            if keys[pg.K_s] and not lower_edge:
                y+=round(step*max,0)
            if keys[pg.K_d] and not right_edge:
                x+=round(step*max,0)
            if keys[pg.K_r]:
                x=688
                y=380
        
        if keys[pg.K_1]:
            step=0.2
        if keys[pg.K_2]:
            step=0.4
        if keys[pg.K_3]:
            step=0.6
        if keys[pg.K_4]:
            step=0.8
        if keys[pg.K_5]:
            step=1

        if x <= 400+3*radius:
            left_edge = True
        if x >= 975-2*radius:
            right_edge = True
        if y <= 100+3*radius:
            upper_edge = True
        if y >= 675-2*radius:
            lower_edge = True

        if x >= 400+2*radius:
            left_edge = False
        if x <= 975-2*radius:
            right_edge = False
        if y >= 100+2*radius:
            upper_edge = False
        if y <= 675-2*radius:
            lower_edge = False

        # Draw bounding box
        drawBorder(screen, 400, 100, 575, 575, "#E8E8E8", "BLACK", radius, 0)
        # Draw dot
        pg.draw.circle(screen,"RED", (x,y), radius)
        # Draw position
        my_font = pg.font.SysFont('Arial', 25)
        text_surface = my_font.render('Position: ('+re.split("\.",str(x))[0]+', '+re.split("\.",str(y))[0]+')                ', True, (20, 20, 20))   
        screen.blit(text_surface, (400,65))
        
        # # Text input blit
        # for text_input in text_inputs:
        #     text_input.process()
        # if running:
        #     print('Pos: ('+str(x)+', '+str(y)+')                ', end='\r')  
        pw.update(events)
        pg.display.update()
    except Exception as e: print(e)
    # flip() the display to put your work on screen
    pg.display.flip()
    clock.tick(60)  # limits FPS to 60
    
pg.quit()