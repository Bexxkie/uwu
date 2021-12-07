#
# physics-Entity
#
# @ㇼㇼ
import pygame
import physics

class Sprite(pygame.sprite.Sprite):
    def __init__(self,image,x,y,id=0):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        a,b = self.rect.topleft
        c,d = self.rect.bottomright
        
        #boundingBox (same as rect but as vector)
        self.bb = physics.aabb(physics.Vector2(a,b),physics.Vector2(c,d),None)
        self.id = id
        
        self.current_speed = 0
        self.vSpeed = 0
        self.hSpeed = 0
        self.on_ground = False
        self.jumping = False
        self.key_down = False
        self.is_sliding = True
        self.is_player= False
        # Veolicy = current_speed + direction
        # Direction = vSpeed +/- down/update
        # Direction = hSpeed +/- right/left
        
    
    def draw(self,screen):
        pygame.draw.rect(screen,((56,120,201)),self.rect,2 )
        screen.blit(self.image, self.rect)
    
    # all movement and physics checks should be in here
    def update(self):
        self.bb = physics.aabb(physics.Vector2(self.rect.topleft[0],self.rect.topleft[1])\
                ,physics.Vector2(self.rect.bottomright[0],self.rect.bottomright[1]),None)
        #Temp floor, will be a vector path later
        
        