#
# Rigid bodies
#
# @ㇼㇼ
#
#
#


from dataclasses import dataclass
import numpy
#
#
class Vector2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        
    def __add__(self, other):
        return Vector2(self.x + other.x,self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        return self.x * other.x + self.y * other.y
    
    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def __eq__(self, other):
        return numpy.allclose(self.x, other.x) and numpy.allclose(self.y, other.y)
    
    def __str__(self):
        return '(%g, %g)' % (self.x, self.y)
        
    def __ne__(self, other):
        return not self.__eq__(other)

class circle:
    def __init__(self, radius:float, position:Vector2):
        self.radius = radius
        self.position = position
    
    def __hit__(self,other):
        r = self.radius + other.radius
        r *= r 
        return r < (self.position.x + other.position.x)**2 \
                  + (self.position.y + other.position.y)**2

@dataclass
class aabb:
    min: Vector2   #topLeft
    max: Vector2   #topRight

#Boolean
def collided(a: aabb,b: aabb):    
    if a.max.x < b.min.x or a.min.x > b.max.x:
        return False
    if a.max.y < b.min.y or a.min.y > b.max.y:
        return False
    
    return True




def resolve_collision(a,b):    
    rel_vel = b.velocity - a.velocity
    pass