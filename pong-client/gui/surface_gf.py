
class surface_gf:
    def __init__(self,surface,position):
        self.X,self.Y = position
        self.surface = surface
    def graphic_update(self,SCREEN):
        SCREEN.blit(self.surface,(self.X,self.Y))
    def logic_update(self,EVENTS):
        pass