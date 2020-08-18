import pygame
import add_border
from sources.fonts import ubuntu_bold_graph,ubuntu_bold_graph_initial
from pygame import *

"""
import pygtk
pygtk.require('2.0')
import gtk
"""

lowerCase = []
upperCase = []
letterCode = []
keyLetters = []
numbersSt = []
numbAcode = []
numBcode = []
numCode = []

def start():
    global lowerCase 
    lowerCase = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",".",":","/"," "]
    global upperCase 
    upperCase = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",".",":","/"," "]
    global letterCode 
    letterCode = [[K_a],[K_b],[K_c],[K_d],[K_e],[K_f],[K_g],[K_h],[K_i],[K_j],[K_k],[K_l],[K_m],[K_n],[K_o],[K_p],[K_q],[K_r],[K_s],[K_t],[K_u],[K_v],[K_w],[K_x],[K_y],[K_z],[K_PERIOD],[58],[47],[K_SPACE]]
    
    global keyLetters 
    keyLetters = []
    for x in range(len(lowerCase)):
        keyLetters.append([lowerCase[x],upperCase[x]])
    
    global numbersSt
    numbersSt = [["0"],["1"],["2"],["3"],["4"],["5"],["6"],["7"],["8"],["9"]]
    for x in range(len(numbersSt)):
        numbersSt[x].append(numbersSt[x][0])
        
    global numbAcode 
    numbAcode = [K_0,K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9]
    global numBcode
    numbBcode = [K_KP0,K_KP1,K_KP2,K_KP3,K_KP4,K_KP5,K_KP6,K_KP7,K_KP8,K_KP9]
    
    global numCode 
    numCode = []
    for x in range(len(numbAcode)):
        numCode.append([numbAcode[x],numbBcode[x]])
start()

class text_input():
    def __init__(self):
        #saving background
        self.background = (255,255,255)
        #saving font
        self.font = ubuntu_bold_graph
        self.fontSize = 18
        #text to show
        self.text = "Enter your text here"
        #color
        self.color = (0,0,0)
        #margin
        self.margin = 3
        #width and height
        self.W , self.H = ((300,30))
        #position saving
        self.X,self.Y = 0,0
        #surface
        self.surface = pygame.surface.Surface((self.W,self.H))
        #saving alpha
        self.alpha = 1
        self.alpha2 = 0.8
        #pressed
        self.pressed = False
        self.pressed_aux = False
        #tile secondary variable
        self.loops = 0
        #intensity
        self.intensity = 20
        #saving border
        self.border_color = (0,0,0)
        #bar position
        self.letter = 0
        #keys
        self.keys = []
        #countdown
        self.countdownA = 0
        self.countdownB = 0
        self.countdownC = 0
        self.countdownD = 0
        #last key
        self.lastKeyS = []
        #default select color, start and end
        self.selection_color = (0,68,255)
        self.start_select = 0
        self.end_select = 0
        #control variable
        self.controlClick = False
        #auxiliar 2nd press value
        self.pressed_aux2 = False
        #initialvalue
        self.initial = True
        #initial color
        self.initial_color = (150,150,150)
        #initial font
        self.initial_font = ubuntu_bold_graph_initial

    def set_text_color(self,color):
        self.color = color
    def set_position(self,position):
        self.X,self.Y = position
    def set_showText(self,showtext):
        self.showtext = showtext
    def set_dimensions(self,dimensions):
        self.W, self.H = dimensions
        self.surface = pygame.surface.Surface((self.W,self.H))
    def set_border_color(self,color):
        self.border_color = color
    def set_alpha_states(self,alpha1,alpha2):
        self.alpha = alpha1*255
        self.alpha2 = alpha2*255
    def set_background(self,background):
        self.background = background
    def set_initial_color(self,color):
        self.initial_color = color
    def set_font(self,font):
        self.font = font
    def set_initial_font(self,font):
        self.initial_font = font
    def set_allowed_values(self,values):
        pass
    def set_show_text(self,text):
        self.text = text
    def set_color(self,color):
        self.color = color
    def set_margin(self,margin):
        self.margin = margin
    def set_intensity_tile(self,intensity):
        self.intensity = intensity
    def set_numbers_and_letters(self):
        self.add_allowed_keys(keyLetters, letterCode)
        self.add_allowed_keys(numbersSt, numCode)
    def set_numbers(self):
        self.add_allowed_keys(numbersSt, numCode)
    def add_allowed_keys(self,keys,codes):
        nks = []
        for x in range(len(keys)):
            nks.append([keys[x],codes[x]])
        for x in range(len(nks)):
            self.keys.append(nks[x])
    def erase_allowed_keys(self):
        self.keys = []
    def getLettersLens(self):
        if (self.initial):
            font = self.initial_font
        else:
            font = self.font
        
        self.letters = []
        for x in range(len(self.text)):
            self.letters.append(self.text[x])  
        surfaces = [] 
        lens = []
        for x in range(len(self.letters)):
            surfaces.append(font.render(self.letters[x],0,self.color))    
            if (self.letters[x] == "j"):
                lens.append(surfaces[len(surfaces)-1].get_size()[0])
            else:
                lens.append(surfaces[len(surfaces)-1].get_size()[0])
        return lens
    def update_writting(self,keys):
        #new last keys
        Erase = True
        for x in range(len(self.keys)):
            someTrue = False
            for z in range(len(self.keys[x][1])):
                if keys[ (self.keys[x][1][z]) ]:
                    someTrue = True
            if someTrue or keys[pygame.K_BACKSPACE] == True:
                Erase = False     
        if (Erase == True):
            self.lastKeyS = []
            self.countdownA = 0
        else:
            self.countdownA += 1
        
        #coping and pasting
        if (keys[pygame.K_LCTRL] == True or keys[pygame.K_RCTRL] == True):
            if (self.controlClick == False):
                if (keys[pygame.K_c] == True):
                    self.controlClick = True
                    self.copy()
                    
                elif (keys[pygame.K_x]):
                    self.controlClick = True
                    self.cut()
                elif (keys[pygame.K_v]):
                    self.controlClick = True
                    self.paste()
            return 0
        else:
            self.controlClick = False
        #check for not allowing multiple writting
        for x in range(len(self.keys)):
            for y in range(len(self.keys[x][1])):
                if (keys [ self.keys[x][1][y] ]):
                    for z in range(len(self.lastKeyS)):
                        if self.lastKeyS[z] != self.keys[x][1][y]:
                            self.countdownA = 0
                            self.countdownB = 0
        nL = [] 
        #for testing all posibilities
        for x in range(len(self.keys)):
            allowed = True
            for y in range(len(self.lastKeyS)):
                for z in range(len(self.keys[x][1])):
                    if self.lastKeyS[y] == self.keys[x][1][z]:
                        allowed = False
                        self.countdownA += 1
            #some tricks to make a stop when pressing some time the same key
            for z in range(len(self.keys[x][1])):
                if (keys[self.keys[x][1][z]]):
                    nL.append( self.keys[x][1][z] )
                
            someTrue = False
            for z in range(len(self.keys[x][1])):
                if keys[self.keys[x][1][z]]:
                    someTrue = True
            if (someTrue == True and (allowed or self.countdownA > 30)):
                self.del_selected()
                if (len(self.letters) == 0):
                    if (keys[pygame.K_CAPSLOCK] == False):
                        self.letters.append(self.keys[x][0][0])
                        self.text = self.keys[x][0][0]
                    else:
                        self.letters.append(self.keys[x][0][1])
                        self.text = self.keys[x][0][1]
                else:
                    self.letters.append(self.letters[len(self.letters)-1])
                    for y in range(len(self.letters)-1,self.letter,-1):
                        
                        self.letters[y] = self.letters[y-1]
                    if (keys[pygame.K_CAPSLOCK] == False):
                        self.letters[self.letter] = self.keys[x][0][0]
                    else:
                        self.letters[self.letter] = self.keys[x][0][1]
                    newtext = ""
                    for x in range(len(self.letters)):
                        newtext = newtext + self.letters[x]
                    self.text = newtext
                self.letter += 1
        
        
        
        #updating last keys
        
        allowed = True
        for y in range(len(self.lastKeyS)):
            if self.lastKeyS[y] == pygame.K_BACKSPACE or self.lastKeyS[y] == pygame.K_LEFT or self.lastKeyS[y] == pygame.K_RIGHT:
                allowed = False
                self.countdownB += 1
        if (keys[pygame.K_BACKSPACE] == True):
            nL.append(pygame.K_BACKSPACE)
        if keys[pygame.K_BACKSPACE] == True and self.letter > 0 and self.letter <= len(self.letters) and (allowed or self.countdownB > 10):
            delete = self.del_selected()
            if (not(delete)):
                del self.letters[self.letter-1]   
                newtext = ""
                for x in range(len(self.letters)):
                    newtext = newtext + self.letters[x]
                self.text = newtext     
                self.letter -= 1
        if (keys[pygame.K_LEFT]):
            nL.append(pygame.K_LEFT)
        if (keys[pygame.K_LEFT] == True and self.letter > 0 and (allowed or self.countdownB > 30)):
            self.letter -= 1
        if (keys[pygame.K_RIGHT]):
            nL.append(pygame.K_RIGHT)
        if (keys[pygame.K_RIGHT] == True and self.letter < len(self.letters) and (allowed or self.countdownB > 30)):
            self.letter += 1 
        self.lastKeyS = nL
        if (len(nL) == 0):
            self.countdownA = 0
            self.countdownB = 0
            self.countdownC = 0
            self.countdownD = 0
  
    def set_select_color(self,color):
        self.selection_color = color
    def copy(self):
        copytext = ""
        if (self.start_select < self.end_select):
            for x in range(self.start_select+1,self.end_select):
                copytext = copytext + self.letters[x]
        else:
            for x in range(self.end_select,self.start_select+1):
                copytext = copytext + self.letters[x]
        """
        clipboard = gtk.clipboard_get()
    
        clipboard.set_text(copytext)
        
        clipboard.store()
        """
    def cut(self):
        self.copy()
        self.del_selected()
        
        self.letter = 0
    def paste(self):
        self.del_selected()
        textoA = []
        for x in range(self.letter):
            textoA.append(self.letters[x])
            
        clipboard = gtk.clipboard_get()
        text = clipboard.wait_for_text()
        
        for x in range(len(text)):
            textoA.append(text[x])
        
        for x in range(self.letter,len(self.letters)):
            textoA.append(self.letters[x])
        self.letters = textoA
        
        nt = ""
        for x in range(len(self.letters)):
            nt = nt + self.letters[x]
        self.text = nt
        self.letter += len(text)
    def del_selected(self):
        if (self.start_select +1 == self.end_select):
            return 0
        if (self.start_select < self.end_select):
            del self.letters[self.start_select+1:self.end_select]
            self.letter = self.start_select+1
        else:
            del self.letters[self.end_select:self.start_select+1]
            self.letter = self.end_select
        newtext = ""
        for x in range(len(self.letters)):
            newtext = newtext + self.letters[x]
        
        self.start_select = 0
        self.end_select = 1
        
        self.text = newtext
        
        return 1
        
    def logic_update(self,events): 
        
        if (self.initial):
            font = self.initial_font
            color = self.initial_color
        else:
            font = self.font
            color = self.color
        
        #getting all events
        mouse = events.get_mouse()
        keys = events.get_keyboard()
        mx,my = mouse.get_position()
        pressed = mouse.get_pressed()[0]
       
        self.getLettersLens()
        #updating key events
        if (self.pressed == True):
            self.update_writting(keys) 
        #getting particular letters surfaces
        lens = self.getLettersLens()
        
        #mouse events
        if (mx > self.X and mx < self.X + self.W and my > self.Y and my < self.Y + self.H):
            if (pressed):
                
                #we calculate the position of the tile when we press
                netaX = mx - self.margin - self.X
                netaV = 0
                anetaV = 0
                for x in range(len(lens)):
                    netaV += lens[x]
                    #until we have passed the letter distance
                    if (netaV > netaX):
                        #calculating if we go forward or backforward
                        if (netaX - anetaV) < lens[x] / 2:
                            self.letter = x
                            break
                        else:
                            self.letter = x+1
                            break
                    #last value
                    anetaV = netaV
                    if (x == len(lens)-1):
                        self.letter = x+1
                #selection area
                if (self.pressed_aux == False):
                    self.start_select = self.letter-1
                    self.end_select = self.letter-1
                else:
                    self.end_select = self.letter
                self.pressed_aux = True
                self.pressed = True
                
                if (self.initial):
                    self.text = ""
                    self.letters = []
                    self.initial = False
                    self.letter = 0
            else:
                
                self.pressed_aux = False
            
        else:
            
            
            if (self.pressed_aux2 == False and pressed):
                self.pressed = False
                
            self.pressed_aux = False
        self.pressed_aux2 = pressed
            
            
        alpha = self.alpha
        if (self.pressed == False):
            alpha = self.alpha2
        
       
        #getting neta position
        
        if (len(lens) != 0):
            neta_position = 0
            for x in range(self.letter):
                try:
                    neta_position += lens[x]
                except:
                    self.letter = 1
                    break
        else:
            self.letter = 0
            neta_position = 0
        text = font.render(self.text,0,self.color)
        w,h = text.get_size()
        
        distance = ( self.H - h ) / 2
        
        #the final surface
        surface_final = pygame.surface.Surface((self.W,self.H))
        
        #creating surface and border
        background = pygame.surface.Surface((self.W,self.H))
        background.set_alpha ( alpha )
        background.fill(self.background)
        border_background = add_border.add_border(background, self.border_color)
        
        #bliting the final surface
        surface_final.blit(border_background,(0,0))
        
        #bliting text
        add = 0
        
        
        for x in range(len(self.letters)):
            surface_letter = font.render(self.letters[x],0,color)
            
            #handling the selected colors
            toFill = pygame.surface.Surface(surface_letter.get_size())
            toFill.fill(self.selection_color)
            if (x > self.start_select and x < self.end_select):
                toFill.set_alpha(170)
            elif (x-1 < self.start_select and x+1 > self.end_select):
                toFill.set_alpha(170)
            else:
                toFill.set_alpha(0)
                
            surface_final.blit(toFill,(self.margin+add,distance))
            surface_final.blit(surface_letter,(self.margin+add,distance))
            add += surface_letter.get_size()[0]
        
        #blitting tile
        if (self.loops % self.intensity > self.intensity / 8.0 * 3.0 and self.pressed):
            tile = pygame.surface.Surface((1,h))
            surface_final.blit(tile,(neta_position+self.margin,distance))
        
        #updating surface
        self.surface = surface_final
        
        #updating variable
        self.loops += 1
    def graphic_update(self,SCREEN):
        SCREEN.blit(self.surface,(self.X,self.Y))
        
        
