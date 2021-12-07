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
import math
import numpy
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
        
        self.ground = physics.aabb(physics.Vector2(0,390),physics.Vector2(640,500),physics.Material("bouncy",1,.5))
        self.wall = physics.aabb(physics.Vector2(0,0),physics.Vector2(20,500),physics.Material("bouncy",1,.5))
        self.terrain = [self.ground,self.wall]
        self.player = physEntity.Sprite(imdir+"0.gif",50,50)
        
        self.Ent = pygame.sprite.Group()
        self.Ent.add(self.player)
        self.Ent.add(physEntity.Sprite(imdir+"0.gif",130,70,1))
        self.Ent.add(physEntity.Sprite(imdir+"0.gif",190,70,2))
        self.player.is_player = True
        
    #
    #
    def on_event(self,event):
        if event.type == pygame.QUIT:
            self._running = False
        
        
    #
    #
    def on_loop(self):
        # input control
        #
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            #self.facing_left = True
            self.player.hSpeed = -5
            self.player.key_down = True
            self.player.is_sliding = False
            #
            #MOVE_RIGHT        
        elif key[pygame.K_RIGHT]:
            #self.facing_left = False
            self.player.hSpeed = 5
            self.player.key_down = True
            self.player.is_sliding = False
        else:
            self.player.key_down = False
            self.player.is_sliding = True
            
            
        if key[pygame.K_UP]:
            self.player.jumping=True
        else:
            self.player.jumping=False
        
        #
        #
        #check world collisions
        for ent in self.Ent:
            ent.update() # Update ents aabb
            # Entity Collision here:
            for ent2 in self.Ent:
                if ent2.id != ent.id:
                    if physics.collided(ent.bb,ent2.bb):
                        #hits top
                        if ent.bb.max.y <= ent2.bb.min.y:# and ent.bb.min.y > ent2.bb.max.y:
                            ent.vSpeed =-10
                            ent.rect.y = ent2.bb.min.y-ent.rect.h
                            ent.is_sliding = False
                        # hits left
                        elif ent.bb.max.x >= ent2.bb.min.x and not ent.bb.min.x >= ent2.bb.min.x:
                            d = numpy.clip(ent.bb.max.x - ent2.bb.min.x,-5,5)
                            ent2.hSpeed=d
                            ent2.is_sliding = False
                        # hits right
                        else:#if ent.bb.min.x >= ent2.bb.max.x and not ent.bb.max.x >= ent2.bb.min.x:
                            d = numpy.clip(ent.bb.min.x - ent2.bb.max.x,-5,5)
                            ent2.hSpeed = d
                            ent2.is_sliding = False
                    else:
                        ent2.is_sliding = True
                    
                    
            for terrain in self.terrain:
                if not physics.collided(ent.bb,terrain):                         
                    #do gravity
                    if ent.vSpeed < physics.CONST_GRAVITY_MAX:
                        ent.vSpeed += physics.CONST_GRAVITY
                        ent.on_ground = False
                            #ent.vSpeed = 0
                # Entity hits terrain piece
                else:
                    if ent.bb.min.x <= terrain.max.x and ent.bb.max.x >= terrain.max.x:
                        ent.hSpeed = 1
                    elif ent.bb.max.y >= terrain.min.y and not ent.bb.min.y >=terrain.max.y:
                        if ent.jumping:                                  # jumping is a bool
                            ent.jumping = False
                            ent.vSpeed = 60
                            
                        if ent.is_sliding:
                            if ent.current_speed > 0:
                               ent.hSpeed -= terrain.material.friction
                                # moving left add to speed for friction
                            if ent.current_speed < 0:
                                ent.hSpeed += terrain.material.friction
                            if abs(ent.current_speed) <= 0.2:
                                ent.hSpeed=0
                        #
                        # get current atan(Speed/hSpeed)*180/pi = degrees
                        # apply a negative direction to cancel the movement maybe?
                        #
                        #deg = math.atan(vSpeed/hSpeed)*180/math.pi
                        ent.vSpeed *= -terrain.material.hardness   # hardness == elasticiy/ how much bounce the object gives
                        ent.rect.y = terrain.min.y-ent.rect.h      # snap ent to the floor (keeps everything on the same level
                        ent.on_ground = True                                                
            ent.current_speed = ent.hSpeed                      # set ents current_speed
            ent.rect.move_ip((ent.hSpeed,ent.vSpeed))           # move the ent

    #
    #
    def on_render(self):
        # start new frame
        self.screen.fill((50,50,50))
        pygame.draw.rect(self.screen,(100,190,180),[0,390,640,400])
        pygame.draw.rect(self.screen,(100,190,180),[0,0,20,500])
        for ent in self.Ent:
            print(ent.id)
            ent.draw(self.screen)
                
        
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