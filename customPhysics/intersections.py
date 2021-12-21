#
# collision
#
#
# @ㇼㇼ
#
'''
objectives-
 proper simplified collision for any straight line angle
 
 need to detect if a point intersects a line (check if a point is part of a line)
 that'll be the first thing i need to get done. since that will help with collision in general
	
	get Slope of line
	(y2-y1)/(x2-x1)
	
	check if point is on line (is the slope if it was a line with 'x1y1' the same)
	if (y3-y1) == slope * (x3-x1)
	
	check if the point is /on/ the line
	
	min(x1,x2) <=x3 <= max(x1,x2)
	min(y1,y2) <=y3 <= max(y1,y2)
	
	just check that the lower of the x/y endPoints is lower than the point were checking and that the higher of the x/y endpoints is higher than the point were checking
	
	in my case endpoint1 will always be the lower value on the line
	
	so i can use x1 <= x3 <=x2

'''
#
# Just handles collisions from given shapes (will require a primitives lib)
#


import math
#
# COMPARATORS 
# 
def point_on_line(line,c):
    # line = point a - point b
    
    ax, ay = line[0]
    bx, by = line[1]
    cx, cy = c
    slope = get_slope(line[0],line[1])
    if cy-ay == slope*(cx-ax):
        if (ax <= cx <=bx) and (ay <= cy <=by):
            return True
    return False
#
#
def point_on_circle(circle,c):
    # circle will concist of a point and a floating radius as z
    # get distance between 2 points 
    # distance = √(x2-x1)^2/(y2-y1)^2
    center,radius = circle
    d = get_distance(center,c)        
    if d <= radius:
        return True
    return False
#
# MATH FUNCS
#    
def get_distance(a,b):
    ax,ay = a
    bx,by = b
    return math.sqrt((bx-ax)**2+(by-ay)**2)
#
#
def get_slope(a,b):
    ax, ay = a
    bx, by = b
    slope = (by-ay) / (bx-ax)
    
    return slope