#
# slidescroller
# Entity abstract class
#
# @ㇼㇼ
#
import pygame
from main import KEYBINDS
from main import _GAMETICK
import os

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

#
# imageString, startingLocationX, startingLocationY
class Entity(Sprite):
    
    def __init__(self, image, startX, startY):
        super(Entity,self).__init__(image,startX,startY)
        self.alive  = True
        self.health = 100
        self.ground_speed = 4
        
        
        self.jumpspeed = 15
        self.vspd = 0
        
        self.gravity = 1
        
        self.ground_friction = .3 #subtracts from current speed
        self.air_friction = .03
        
        self.current_speed =0
        self.moving= False
        
        self.animation_index = 0
        self.frame  = 0
        self.frame_speed = 0
        
    #   
    #   
    def _move(self, x, y):
        
        self.rect.move_ip((x,y))
        self.walk_animation()
    #
    #
        
class Box(Entity):
    
    def __init__(self,startX,startY):
        super().__init__("overlay.png", startX, startY)



class Enemy(Entity):
    pass



class Player(Entity):
    
    def __init__(self, startX, startY):
        super().__init__(imdir+"0.gif", startX, startY)
        self.stand_image = self.image
        self.walk_cycle = [pygame.image.load(imdir+f"{i}.gif") for i in range (1,8)]
        self.frame_speed = int(_GAMETICK/len(self.walk_cycle)-1)
        
        
        self.jump_count = 0
        self.max_jumps = 2
        self.facing_left = True
    #
    #
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
    
    def _update(self,boxes,walls):
        hspd = 0
        speed = self.ground_speed
        fric = self.air_friction
        onGround = pygame.sprite.spritecollideany(self,boxes)
        touchWall = pygame.sprite.spritecollideany(self,walls)
        if onGround:
            fric = self.ground_friction
        
        key = pygame.key.get_pressed()
        
        #
        #MOVE_LEFT
        if key[pygame.K_LEFT]:
            self.facing_left = True
            self.moving = True
            hspd = -speed
        #
        #MOVE_RIGHT        
        elif key[pygame.K_RIGHT]:       
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
        if self.moving and touchWall:
            if self.current_speed > 0:
                hspd = -speed
            if self.current_speed < 0:
                hspd = +speed
        #
        #JUMP
        if key[pygame.K_UP] and onGround or key[pygame.K_UP] and self.jump_count < self.max_jumps:
            self.vspd = -self.jumpspeed
            self.jump_count+=1
        #
        #GRAVITY
        if self.vspd <10:
            self.vspd +=self.gravity
        #
        if self.vspd >0 and onGround:
            self.vspd = 0
            self.jump_count = 0
        
        self.current_speed = hspd
        self._move(hspd,self.vspd)