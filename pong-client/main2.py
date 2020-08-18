import pygame
from gui.server_list import server_list
from gui import events
import gui.status_cur as gs

def main():
    SCREEN = pygame.display.set_mode((800,600))
    server = server_list()
    server.set_position((50,50))
    cont = True
    gs.init()
    while (cont):
        SCREEN.fill((255,255,255))
        
        EVENTS = events.events()
        EVENTS.update_keyboard(pygame.key.get_pressed())
        EVENTS.update_mouse(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                cont = False
                
                
        server.logic_update(EVENTS)
        server.graphic_update(SCREEN)
        gs.update()
        pygame.display.update()
        
        
main()