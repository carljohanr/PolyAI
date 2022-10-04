# Pieces for Isle of Cats base game

import math

# Rotate xcoordinate of object by a degree [90 180 270 360]
def rotatex(pt, refpt, deg):
    return (refpt[0] + (math.cos(math.radians(deg)) * (pt[0] - refpt[0])) +
            (math.sin(math.radians(deg)) * (pt[1] - refpt[1])));

# Rotate ycoordinate of object by a degree [90 180 270 360]
def rotatey(pt, refpt, deg):
    return (refpt[1] + (-math.sin(math.radians(deg))*(pt[0] - refpt[0])) +
            (math.cos(math.radians(deg)) * (pt[1] - refpt[1])));

# Rotate coordinates of a point.
def rotatep(pt, refpt, deg):
    return (int(round(rotatex(pt, refpt, deg))),
            int(round(rotatey(pt, refpt, deg))));


# Represents a Piece. Each piece has a unique ID and remembers its size so
# player score can be easily calculated. 
class Piece:
    def __init__(self, color):
        self.id = None;
        self.size = 1;

    # This function will use (x,y) and present points and coordinates to fill out shape
    # on the board.
    def set_points(self, x, y):
        self.points = [];
        self.corners = [];

    # Create the object
    def create(self, num, pt):
        self.set_points(0, 0);
        pm = self.points;
        self.pts_map = pm;

        self.refpt = pt;
        x = pt[0] - self.pts_map[num][0];
        y = pt[1] - self.pts_map[num][1];
        self.set_points(x, y);

    # Rotate the object; any rotations are valid for the board.
    def rotate(self, deg):
        self.points = [rotatep(pt, self.refpt, deg) for pt in self.points];
        self.corners = [rotatep(pt, self.refpt, deg) for pt in self.corners];

    # Flip the board; any flip is valid for the board.
    def flip(self, orientation):
        def flip_h(pt):
            x1 = self.refpt[0];
            x2 = pt[0];
            x1 = (x1 - (x2 - x1));
            return (x1, pt[1]);

        if orientation == 'h':
            self.points = [flip_h(pt) for pt in self.points];
            self.corners = [flip_h(pt) for pt in self.corners];


'''
Define 17 shapes in Isle of Cats base game
'''


# big_pieces = [[[1,0,0],[1,1,1],[1,0,1]],[[1,1,1,1],[0,1,0,0],[0,1,0,0]],[[1,1,1,0],[0,1,1,1]],\
#             [[0,1,1],[1,1,1],[0,0,1]],[[0,1,0,0],[1,1,1,1],[0,1,0,0]],[[0,1,1,1],[1,1,0,1]],\
#           [[0,1,0],[1,1,1],[0,1,0]],[[1,1,1],[0,1,0],[0,1,0]],[[1,1,1,1,1]],\
#               [[0,1,1],[1,1,0],[1,0,0]],[[1,1,1],[1,0,0],[1,0,0]],[[1,1,1],[1,0,1]],[[1,1,1],[1,1,0]],\
#         [[0,1,1,1],[1,1,0,0]],[[1,1,1,1],[0,1,0,0]],[[1,1,1,1],[1,0,0,0]],[[1,1,0],[0,1,1]]]


# class Pass(Piece):
#     def __init__(self,color):
#         self.size = 0;
#         self.uniques = 1; # number of unique transformations per piece, for AI
#         self.color=color
#         self.id = 'Pass'+str(self.color);
        
#     def set_points(self, x, y):
#         self.points = [];
#         self.corners = [];
    
class TR1(Piece):
    def __init__(self,color):
        self.size = 1;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'TR1'+str(self.color);
        
    def set_points(self, x, y):
        self.points = [(x, y)];
        self.corners = [(x, y)];

class TR2(Piece):
    def __init__(self,color):
        self.size = 2;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'TR2'+str(self.color);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y)];
        self.corners = [(x, y)];
        
class TR3(Piece):
    def __init__(self,color):
        self.size = 3;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'TR3'+str(self.color);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y)];
        self.corners = [(x, y)];

class TR4(Piece):
    def __init__(self,color):
        self.size = 3;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'TR4'+str(self.color);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x,y+1)];
        self.corners = [(x, y)];

class RT1(Piece):
    def __init__(self,color,counter):
        self.size = 4;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'RT1'+str(counter);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x,y+1),(x+1,y+1)];
        self.corners = [(x, y)];

class RT2(Piece):
    def __init__(self,color,counter):
        self.size = 4;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'RT2'+str(counter);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y+1),(x,y+1),(x+1,y+2)];
        self.corners = [(x, y)];
        
class RT3(Piece):
    def __init__(self,color,counter):
        self.size = 4;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'RT3'+str(counter);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x,y+1),(x+2,y)];
        self.corners = [(x, y)];

class RT4(Piece):
    def __init__(self,color,counter):
        self.size = 4;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'RT4'+str(counter);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+1,y+1),(x+2,y)];
        self.corners = [(x, y)];
        
class RT5(Piece):
    def __init__(self,color,counter):
        self.size = 4;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'RT5'+str(counter);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y)];
        self.corners = [(x, y)];

        
    
class T0(Piece):
    def __init__(self,color):
        self.size = 6;
        self.uniques = 8; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'T0'+str(self.color);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+1,y+1),(x+1,y-1)];
        self.corners = [(x, y)];

class T1(Piece):
    def __init__(self,color):
        self.size = 6;
        self.uniques = 8; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'T1'+str(self.color);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+1,y+1),(x+1,y+2)];
        self.corners = [(x, y)];

class N0(Piece):
    def __init__(self,color):
        self.size = 6;
        self.uniques = 8; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'N0'+str(self.color);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y+1),(x+2,y+1),(x,y+1)];
        self.corners = [(x, y)];

class N1(Piece):
    def __init__(self,color):
        self.size = 6;
        self.uniques = 8; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'N1'+str(self.color);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1),(x+2,y+1),(x,y-1)];
        self.corners = [(x, y)];

class P0(Piece):
    def __init__(self,color):
        self.size = 6;
        self.uniques = 8; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'P0'+str(self.color);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+1,y+1),(x+2,y+1),(x+3,y+1)];
        self.corners = [(x, y)];
        
class P1(Piece):
    def __init__(self,color):
        self.size = 6;
        self.uniques = 8; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'P1'+str(self.color);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1),(x+1,y+1),(x+1,y+2)];
        self.corners = [(x, y)];

class NN(Piece):
    def __init__(self,color):
        self.size = 4;
        self.uniques = 8; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'NN'+str(self.color);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+1,y+1),(x+2,y+1)];
        self.corners = [(x, y)];


# class D0(Piece):
#     def __init__(self):
#         self.id = 'D0';
#         self.size = 6;
#         self.uniques = 4; # number of unique transformations per piece, for AI

#     def set_points(self, x, y):
#         self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+1,y+1),(x+2,y+1)];
#         self.corners = [(x, y)];

# class X0(Piece):
#     def __init__(self):
#         self.id = 'X0';
#         self.size = 6;
#         self.uniques = 4; # number of unique transformations per piece, for AI

#     def set_points(self, x, y):
#         self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+1,y+1),(x+2,y-1)];
#         self.corners = [(x, y)];

# class C1(Piece):
#     def __init__(self):
#         self.id = 'C1';
#         self.size = 6;
#         self.uniques = 8; # number of unique transformations per piece, for AI

#     def set_points(self, x, y):
#         self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1),(x+2,y+1),(x+3,y+1)];
#         self.corners = [(x, y)];

# class W0(Piece):
#     def __init__(self):
#         self.id = 'W0';
#         self.size = 6;
#         self.uniques = 8; # number of unique transformations per piece, for AI

#     def set_points(self, x, y):
#         self.points = [(x, y),(x+1,y),(x+2,y),(x,y-1),(x+2,y+1),(x+3,y+1)];
#         self.corners = [(x, y)];

# class Z0(Piece):
#     def __init__(self):
#         self.id = 'Z0';
#         self.size = 6;
#         self.uniques = 8; # number of unique transformations per piece, for AI

#     def set_points(self, x, y):
#         self.points = [(x, y),(x+1,y),(x+2,y),(x+2,y+1),(x+2,y+2),(x+3,y+2)];
#         self.corners = [(x, y)];


# class F0(Piece):
#     def __init__(self):
#         self.id = 'F0';
#         self.size = 6;
#         self.uniques = 8; # number of unique transformations per piece, for AI

#     def set_points(self, x, y):
#         self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x,y+1),(x+2,y+1)];
#         self.corners = [(x, y)];

# class F1(Piece):
#     def __init__(self):
#         self.id = 'F1';
#         self.size = 6;
#         self.uniques = 8; # number of unique transformations per piece, for AI

#     def set_points(self, x, y):
#         self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x,y+1),(x+1,y-1)];
#         self.corners = [(x, y)];

# class F2(Piece):
#     def __init__(self):
#         self.id = 'F2';
#         self.size = 6;
#         self.uniques = 8; # number of unique transformations per piece, for AI

#     def set_points(self, x, y):
#         self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x,y+1),(x+2,y-1)];
#         self.corners = [(x, y)];

# class F3(Piece):
#     def __init__(self):
#         self.id = 'F3';
#         self.size = 6;
#         self.uniques = 8; # number of unique transformations per piece, for AI

#     def set_points(self, x, y):
#         self.points = [(x+1, y+1),(x+1,y),(x+2,y),(x+3,y),(x,y+1),(x+1,y+2)];
#         self.corners = [(x, y)];

# class F4(Piece):
#     def __init__(self):
#         self.id = 'F4';
#         self.size = 6;
#         self.uniques = 8; # number of unique transformations per piece, for AI

#     def set_points(self, x, y):
#         self.points = [(x, y-1),(x+1,y),(x+2,y),(x+3,y),(x+1,y-1),(x+1,y+1)];
#         self.corners = [(x, y)];


# class F5(Piece):
#     def __init__(self):
#         self.id = 'F5';
#         self.size = 6;
#         self.uniques = 8; # number of unique transformations per piece, for AI

#     def set_points(self, x, y):
#         self.points = [(x, y-1),(x+1,y),(x+2,y),(x+3,y),(x+1,y-1),(x+2,y+1)];
#         self.corners = [(x, y)];


class I(Piece):
    def __init__(self, color):
        self.size = 5;
        self.uniques = 2; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'I'+str(self.color);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+4,y)];
        self.corners = [(x, y)];
        
class L(Piece):
    def __init__(self, color):
        self.size = 5;
        self.uniques = 8; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'L'+str(self.color);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x,y+1)];
        self.corners = [(x, y)];

class Y(Piece):
    def __init__(self, color):
        self.size = 5;
        self.uniques = 8; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'Y'+str(self.color);

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+1,y+1)];
        self.corners = [(x, y)];

class N(Piece):
    def __init__(self, color):
        self.size = 5;
        self.uniques = 8; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'N'+str(self.color);

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y+1),(x+2,y+1)];
        self.corners = [(x, y)];

class U(Piece):
    def __init__(self, color):
        self.size = 5;
        self.uniques = 8; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'U'+str(self.color);

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1),(x+2,y+1)];
        self.corners = [(x, y)];
        
class V(Piece):
    def __init__(self, color):
        self.size = 5;
        self.uniques = 8; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'V'+str(self.color);

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1),(x,y+2)];
        self.corners = [(x, y)];

class P(Piece):
    def __init__(self, color):
        self.size = 5;
        self.uniques = 8; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'P'+str(self.color);

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1),(x+1,y+1)];
        self.corners = [(x, y)];
        
# class F(Piece):
#     def __init__(self):
#         self.id = 'F';
#         self.size = 5;
#         self.uniques = 8; # number of unique transformations per piece, for AI

#     def set_points(self, x, y):
#         self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1),(x+1,y-1)];
#         self.corners = [(x, y)];

class T(Piece):
    def __init__(self, color):
        self.size = 5;
        self.uniques = 8; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'T'+str(self.color);

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+1,y+1),(x+1,y+2)];
        self.corners = [(x, y)];
        
# class Z(Piece):
#     def __init__(self):
#         self.id = 'Z';
#         self.size = 5;
#         self.uniques = 4; # number of unique transformations per piece, for AI

#     def set_points(self, x, y):
#         self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1),(x+2,y-1)];
#         self.corners = [(x, y)];
        
class X(Piece):
    def __init__(self, color):
        self.size = 5;
        self.uniques = 8; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'X'+str(self.color);

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+1,y+1),(x+1,y-1)];
        self.corners = [(x, y)];
        
class W(Piece):
    def __init__(self, color):
        self.size = 5;
        self.uniques = 8; # number of unique transformations per piece, for AI
        self.color=color
        self.id = 'W'+str(self.color);

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+1,y+1),(x+2,y+1),(x+2,y+2)];
        self.corners = [(x, y)];