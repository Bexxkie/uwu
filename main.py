#
# slideScroller
# main
#
# @ㇼㇼ
#
#
# VectorMovement
#
# @ㇼㇼ
#
import math
import pygame
from pygame.locals import *
import Entity

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
    #
    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self._running = True       
        
        self.player = Entity.Player(100,200)
        self.boxes = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        for box_x in range(0,self.width+50,50):
            self.boxes.add(Entity.Box(box_x,self.height))
            
        for box_y in range(0,self.width+50,50):
            self.walls.add(Entity.Box(0,box_y))
        for box_y in range(0,self.width+50,50):
            self.walls.add(Entity.Box(self.width,box_y))
        self.rotate_walls()
    #
    #
    def rotate_walls(self):
        for wall in self.walls:
            wall.image = pygame.transform.rotate(wall.image,90)
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
        self.player.draw(self.screen)
        self.boxes.draw(self.screen)
        self.walls.draw(self.screen)
                
        
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
            self.player._update(self.boxes,self.walls)
            self.on_loop()
            self.on_render()
            self.clock.tick(_GAMETICK)
        self.on_cleanup()   
 


if __name__ == "__main__":
    mesher = App()    
    mesher.on_execute()        