import pygame

def add_border(surface,color = (0,0,0),b1 = 1,b2 = 1,b3 = 1,b4 = 1):
    w,h = surface.get_size()
    b1 = pygame.surface.Surface((w,1))
    b2 = pygame.surface.Surface((1,h))
    b3 = pygame.surface.Surface((1,h))
    b4 = pygame.surface.Surface((w,1))
    
    b1.fill(color)
    b2.fill(color)
    b3.fill(color)
    b4.fill(color)
    
    surface.blit(b1,(0,0))
    surface.blit(b2,(0,0))
    surface.blit(b3,(w-1,0))
    surface.blit(b4,(0,h-1))
    
    return surface