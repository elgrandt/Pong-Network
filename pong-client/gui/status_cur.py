import pygame
import sources.cursors as cu

cursor = None

def init():
    global cursor
    cursor = "arrow"

def set_pointer():
    global cursor
    cursor = "pointer"

def update():
    global cursor
    if (cursor == "arrow"):
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
    elif (cursor == "pointer"):
        pygame.mouse.set_cursor( (24,24), (0,0), cu.datatuple, cu.masktuple )
        
    cursor = "arrow"