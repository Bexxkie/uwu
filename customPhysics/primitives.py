#
# primitives
#
# @ㇼㇼ
#

# I don't even know if this is the right way to define these but it *does* work with the intersections class

class Rect():

    def __init__(self, a:Point, b:Point):
        self.a = a #topleft
        self.b = b #bottomright
        self.ax,self.ay = self.a
        self.bx,self.by = self.b
        
    def _get(self):
        return(self.a,self.b)
        
    # While the rect is technically made of lines, it'll still be controlled with topL and botR points        
    
    def _get_left(self):
        return ((self.ax,self.ay),(self.ax,self.by))
    
    def _get_right(self):
        return ((self.bx,self.ay),(self.bx,self.by))
    
    def _get_top(self):
        return ((self.ax,self.ay),(self.bx,self.ay))
    
    def _get_bottom(self):
        return ((self.ax,self.by),(self.bx,self.by))
    #
    def _update_lines(self):
        self.ax,self.ay = self.a
        self.bx,self.by = self.b    
    #
    def _move(self, x,y):
        ax,ay = self.a
        bx,by = self.b
        
        ax += x
        bx += x
        ay += y
        by += y
        
        self.a = (ax,ay)
        self.b = (bx,by)
        self._update_lines()

class Circle():
    
    def __init__(self, point:Point, rad):
        self.x,self.y = point
        self.rad = rad
    
    def _get(self):
        return((self.x,self.y),self.rad)
    
    def _move(self, x, y):
        self.x += x
        self.y += y

class Point():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        
    def _get(self):
        return ((self.x,self,y))
    
    def _move(self,x,y):
        self.x += x
        self.y += y

class Line():
    
    def _innit__(self, a:Point, b:Point):
        self.a = a
        self.b = b

    def _get(self):
        return((self.a),(self.b))
    
    def _move(self, x,y):
        ax,ay = self.a
        bx,by = self.b

        ax += x
        bx += x
        ay += y
        by += y

        self.a = (ax,ay)
        self.b = (bx,by)