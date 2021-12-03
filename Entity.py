#
# gamepls
# Entity abstract class
#
# @ㇼㇼ
#
import pygame
from main import KEYBINDS
from main import _GAMETICK
import os
import math
imdir = os.getcwd()+'\\icoFrames\\'

class Sprite(pygame.sprite.Sprite):
    #
    #
    def __init__(self, image, startX, startY):
        super().__init__()
        
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        
        self.rect.center = [startX,startY]
    #
    #
    def draw(self,screen):
        screen.blit(self.image, self.rect)
        if self.color_mod != (0,0,0,0):
            screen.blit(self.image, self.rect,special_flags = pygame.BLEND_RGBA_MULT)
#
# imageString, startingLocationX, startingLocationY
class Entity(Sprite):
    
    def __init__(self, image, startX, startY):
        super(Entity,self).__init__(image,startX,startY)
        
        self.alive  = True
        self.health = 100
        self.ground_speed = 4
        self.is_player = False
        self.color_mod = (0,0,0,0)
        
        self.stand_image = self.image
        self.walk_cycle = [None]
        self.frame_speed = 0
        self.facing_left = True
    
        self.can_dbl_jump = False
        self.jumpspeed = 15
        self.vspd = 0
        self.sprint = False
        
        self.gravity = 1
        
        self.ground_friction = .3 #subtracts from current speed
        self.air_friction = .03
        
        self.current_speed =0
        self.moving= False
        
        
        self.animation_index = 0
        self.frame  = 0
        self.frame_speed = 0
        
    def recolour(self):
        self.image = self.walk_cycle[self.animation_index]
        colorImage = pygame.Surface(self.image.get_size()).convert_alpha()
        colorImage.fill(self.color_mod)
        
        
        
    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]        
        if not self.facing_left:
            self.image = pygame.transform.flip(self.image,True,False)
        if self.moving:
            self.frame+=1
            if self.frame == self.frame_speed:
                if self.animation_index<len(self.walk_cycle)-1:
                    self.animation_index+=1
                else:
                    self.animation_index=0
            if self.frame > self.frame_speed:
                self.frame = 0
    #
    #
    # Need to change this for something better later
    def _update(self,terrain,enemies):
        hspd = 0
        speed = self.ground_speed
        fric = self.air_friction
        self.sprint = False
        
        
        #collideTerrain = pygame.sprite.spritecollideany(self,terrain)
        #onGround   = pygame.sprite.spritecollideany(self,floors)
        #touchWall  = pygame.sprite.spritecollideany(self,walls)
        touchEnemy = pygame.sprite.spritecollideany(self,enemies)
        onGround = None
        rightWall = None
        leftWall = None
        
        
        for ter in terrain:
             if pygame.sprite.collide_rect(self, ter): 
                tldist = self.get_distance(ter.rect.topright,self.rect.topleft)
                trdist = self.get_distance(ter.rect.topleft,self.rect.topright)
                if self.rect.bottom - ter.rect.top <= 10 and tldist >=self.rect.h-5 and trdist >=self.rect.h-5:
                    onGround = ter
                #-->>
                elif self.rect.right - ter.rect.left < 10:
                    rightWall = ter
                #<<--
                elif self.rect.left - ter.rect.right < 10:
                    leftWall = ter
                
            
        if onGround:
            fric = self.ground_friction
        
        # Player control
        #
        if self.is_player:
            key = pygame.key.get_pressed()
            #pygame.key.get_mods()
        #
        #SPRINT
            if key[pygame.K_LSHIFT]:
                self.sprint = True
                speed*=1.3
            
        #
        #MOVE_LEFT
            if key[pygame.K_LEFT] and leftWall is  None:
                self.facing_left = True
                self.moving = True
                hspd = -speed
            #
            #MOVE_RIGHT        
            elif key[pygame.K_RIGHT] and rightWall is  None: 
                self.facing_left = False
                self.moving = True
                hspd = speed

            elif self.moving:
                if self.current_speed > 0:
                    hspd = self.current_speed - fric
                if self.current_speed < 0:
                    hspd = self.current_speed + fric
                if abs(self.current_speed) <= 0.2:
                    self.moving = False                               
            if not key[pygame.K_UP] and self.jump_count >0:
                self.can_dbl_jump = True
            #
            #JUMP
            if key[pygame.K_UP]:
                if onGround and leftWall is None and rightWall is None:
                    self.vspd = -self.jumpspeed
                    self.jump_count+=1
                elif self.jump_count < self.max_jumps and self.can_dbl_jump:
                    self.vspd = -self.jumpspeed*1.1
                    self.jump_count+=1
       
       # not a player
        else:
            #
            # D = sqrt x2-x1**2 + y2-y1**2
            
            distance = self.get_distance(enemies[0].rect.center, self.rect.center)
            #Move_left
            if enemies[0].rect.x+(self.rect.width*1.5) < self.rect.x:
                if leftWall:
                    self.vspd = -self.jumpspeed
                hspd = -speed
                self.moving = True
                self.facing_left = True
            #Move_right
            if enemies[0].rect.x-(self.rect.width*1.5) > self.rect.x:
                if rightWall:
                    self.vspd = -self.jumpspeed
                hspd = +speed
                self.moving = True
                self.facing_left = False
            if distance < self.rect.width*1.8:
                self.color_mod = (255,0,0,100)
                self.recolour()
            else:
                self.color_mod = (0,0,0,0)
            
        # COLLISION STUFF 
        #
        #
        if self.moving and touchEnemy:
            if self.is_player and self.rect.y < touchEnemy.rect.y:
                self.vspd = -6
            #hsdp = self.rect.x-touchEnemy.rect.x
        #
        #Wallcollision
        if self.moving:
            # hop            
            if onGround and abs(self.current_speed) > speed/2 and not self.sprint and leftWall is None and rightWall is None:
                self.vspd = -10
            #bounce off wall
            elif leftWall:
                hspd = 1
            elif rightWall:
                hspd = -1
        
        #
        #GRAVITY
        if self.vspd <10:
            self.vspd +=self.gravity
        # don't fall through stuff
        if onGround:
            floor = onGround.rect.y-self.rect.h+5
            if self.vspd >=0:
                self.rect.y = floor
                self.vspd = 0
                self.jump_count = 0
                self.can_dbl_jump = False
        
        self.current_speed = hspd
        self._move(hspd,self.vspd)
        
        
    def get_distance(self,pointA,pointB):
        a = (pointA[0] - pointB[0])**2
        b = (pointA[1] - pointB[1])**2
        return(math.sqrt(a+b))
        
        
    def _move(self, x, y):
        
        self.rect.move_ip((x,y))
        self.walk_animation()
    #
    #
        
class Box(Entity):
    
    def __init__(self,startX,startY):
        super().__init__("overlay.png", startX, startY)
    


class Enemy(Entity):
    def __init__(self,startX,startY):
        super().__init__(imdir+"0.gif",startX,startY)
        self.stand_image = self.image
        self.walk_cycle = [pygame.image.load(imdir+f"{i}.gif") for i in range (1,8)]
        self.frame_speed = int(_GAMETICK/len(self.walk_cycle)-1)        
        self.facing_left = True
        


class Player(Entity):
    
    def __init__(self, startX, startY):
        super().__init__(imdir+"0.gif", startX, startY)
        self.stand_image = self.image
        self.walk_cycle = [pygame.image.load(imdir+f"{i}.gif") for i in range (1,8)]
        self.frame_speed = int(_GAMETICK/len(self.walk_cycle)-1)
        
        self.is_player = True
        
        self.jump_count = 0
        self.max_jumps = 2
        self.facing_left = True