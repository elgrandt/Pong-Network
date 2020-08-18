
class mouse:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.left = False
        self.center = False
        self.right = False
    def update_position(self,x,y):
        self.x = x;
        self.y = y;
    def update_pressed(self,pressed):
        self.left = pressed[0]
        self.center = pressed[1]
        self.right = pressed[2]
    def get_pressed(self):
        return [self.left, self.center, self.right]
    def get_position(self):
        return [self.x, self.y]
    
class events:
    def __init__(self):
        self.mouse = mouse()
        self.movment = []
        self.rX = []
        self.rY = []
    def fv(self,value):
        for x in range(len(self.movment)):
            if self.movment[x][0] == value:
                return x
    def update_keyboard(self,pressed):
        self.keyboard = pressed
    def update_mouse(self,position,pressed):
        self.mouse.update_position(position[0],position[1])
        self.mouse.update_pressed(pressed)
    def set_player_movement(self,up,down,left,right,shoot,playerID):
        replace = True
        for x in range(len(self.movment)):
            if self.movment[x][0] == playerID:
                replace = False
        if (replace == True):
            new_mov = []
            new_mov.append(playerID)
            new_mov.append(up)
            new_mov.append(down)
            new_mov.append(left)
            new_mov.append(right)
            new_mov.append(shoot)
            self.movment.append(new_mov)
        else:
            self.movment[self.fv(playerID)][1] = up
            self.movment[self.fv(playerID)][2] = down
            self.movment[self.fv(playerID)][3] = left
            self.movment[self.fv(playerID)][4] = right
            self.movment[self.fv(playerID)][5] = shoot
    def get_mouse(self):
        return self.mouse
    def get_keyboard(self):
        return self.keyboard
    def get_m(self):
        return self.movment
    def generate_relative(self,(positionX,positionY)):
        x,y = self.mouse.get_position()
        self.mouse.update_position(x-positionX, y-positionY)
        
        self.rX .append( positionX )
        self.rY .append( positionY )
    def delete_relative(self):
        x,y = self.mouse.get_position()
        self.mouse.update_position(x+self.rX[len(self.rX)-1], y+self.rY[len(self.rY)-1])

        del self.rX[len(self.rX)-1]
        del self.rY[len(self.rY)-1]