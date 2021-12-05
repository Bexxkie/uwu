#
# gamepls
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
        #self.enemy = Entity.Enemy(500,200)
        
        self.terrain = pygame.sprite.Group()
        
        self.floors = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        #self.enemies.add(self.enemy)
        self.enemies.add(Entity.Enemy(500,200))
        self.enemies.add(Entity.Enemy(500,100))
        self.enemies.add(Entity.Enemy(500,300))
        
        
        for floor in range(0,self.width+50,50):
            self.terrain.add(Entity.Box(floor,self.height))
        self.terrain.add(Entity.Box(self.width/2,self.height-50))
        
        for wall in range(0,self.width+50,50):
            self.walls.add(Entity.Box(0,wall))
        for wall in range(0,self.width+50,50):
            self.walls.add(Entity.Box(self.width,wall))
        self.rotate_walls()
    #
    #
    def rotate_walls(self):
        for wall in self.walls:
            wall.image = pygame.transform.rotate(wall.image,90)
            self.terrain.add(wall)
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
        self.enemies.draw(self.screen)
        #self.floors.draw(self.screen)
        #self.walls.draw(self.screen)
        self.terrain.draw(self.screen)
                
        
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
            self.player._update(self.terrain,self.enemies)            
            for enemy in self.enemies:
                enemy._update(self.terrain,self.enemies,self.player)
            self.on_loop()
            self.on_render()
            self.clock.tick(_GAMETICK)
        self.on_cleanup()   


if __name__ == "__main__":
    mesher = App()    
    mesher.on_execute()        