import input_text
import area_movil

class selection_menu:
    def __init__(self):
        self.options = []
    
            
        self.movil = area_movil.area_movil()
        self.movil.enableA(20)
        self.movil.disableB()
        
        self.search_input = input_text.text_input()
        self.search_input.set_show_text("Search your option")
        self.search_input.add_allowed_keys(input_text.keyLetters, input_text.letterCode)
        
    def set_dimensions(self,dimensions):
        self.W,self.H = dimensions
        self.movil.set_surface_dimensions(dimensions)
    def add_option(self,option):
        self.options.append( option )
    def set_position(self,position):
        self.X,self.Y = position
    def set_option_size(self,size):
        self.oX,self.oY = size
    def set_width_shown(self,amount):
        self.amount = amount
        
    def logic_update(self,EVENTS):
        pass