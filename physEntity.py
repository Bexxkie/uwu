#
# physics-Entity
#
# @ㇼㇼ
import pygame
import physics

class Sprite(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        a,b = self.rect.topleft
        c,d = self.rect.bottomright
        #boundingBox (same as rect but as vector)
        self.bb = physics.aabb(physics.Vector2(a,b),physics.Vector2(c,d))                
    
    def draw(self,screen):
        pygame.draw.rect(screen,((56,120,201)),self.rect,2 )
        screen.blit(self.image, self.rect)
    
    # all movement and physics checks should be in here
    def update(self):
        self.rect = [self.bb.min.x,self.bb.min.y,self.bb.max.x,self.bb.max.y]
        #Temp floor, will be a vector path later
        
        #
        