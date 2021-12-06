#
# gamepls
#
# @ㇼㇼ
#

import math
import pygame
from pygame.locals import *
import physics
import physEntity
import os 
imdir = os.getcwd()+'\\icoFrames\\'
_GAMETICK = 60
 


#
# KEYBINDS
#
KEYBINDS = { 
            "MOVEMENT" :{
                "LEFT"  : [pygame.K_LEFT, ord('a')],
                "RIGHT" : [pygame.K_RIGHT, ord('d')],
                "JUMP"  : [pygame.K_UP, K_SPACE,ord,('w')],
                "DUCK"  : [pygame.K_DOWN,ord('s')]
                }
            }




class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        self.mouseDown = False
        self.clock = pygame.time.Clock()
    #
    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self._running = True 
        self.sprite = physEntity.Sprite(imdir+"0.gif",50,50)
        
        
    #
    #
    def on_event(self,event):
        if event.type == pygame.QUIT:
            self._running = False

        
    #
    #
    def on_loop(self):
        pass

    #
    #
    def on_render(self):
        # start new frame
        self.screen.fill((50,50,50))
        pygame.draw.ellipse(self.screen,(100,190,180),[-200,350,900,300])
        self.sprite.draw(self.screen)
                
        
        pygame.display.flip()

    

    #
    #
    def on_cleanup(self):
        pygame.quit()

    #
    #
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while(self._running):            
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.clock.tick(_GAMETICK)
        self.on_cleanup()   

if __name__ == "__main__":
    mesher = App()    
    mesher.on_execute()        