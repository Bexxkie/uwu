#
# entity
#
# @ㇼㇼ
#

import pygame

class entity(pygame.sprite.Sprite):
    
    def __init__(self, image, start):
        self.image = image
        self.rect = self.image.get_rect()        
        self.center = start
        #
        self.is_player = False
        #
        self.current_speed = 0
        self.max_speed = 10
        #
        self.facing_left = True
        self.frame = 0
        self.animation_index = 0
        
    def _draw(self,screen):
        screen.blit(self.image, self.rect)

    def _move(self, x, y):
        self.rect.move_ip((x,y))
        # spritesheet not setup yet`
        #self.walk_animation()
                
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
        
        
'''
    Need a kinda skeletal system for handling collisions
    Maybe use a capsule for collision instead of rects
    




'''