from sources.fonts import ubuntu_bold_graph as Calibri

class loading:
    def __init__(self):
        self.text = "Loading"
        self.add = ""
        self.current = "Loading"
        self.background = (100,255,100)
        self.loops = 0
        self.X = 0
        self.Y = 0
        surface = Calibri.render("Loading . . .",0,(0,0,0))
        self.W,self.H = surface.get_size()
    def set_position(self,position):
        self.X,self.Y = position
    def logic_update(self,EVENTS):
        if (self.loops % 40 < 10):
            self.add = " "
        elif (self.loops % 40 < 20):
            self.add = " ."
        elif (self.loops % 40 < 30):
            self.add = " . ."
        else:
            self.add = " . . ."
        self.current = self.text + self.add
        self.loops += 1
        
    def graphic_update(self,SCREEN):
        surface = Calibri.render(self.current,0,(0,0,0))
        SCREEN.blit(surface,(self.X,self.Y))
        