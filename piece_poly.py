# This file was modified from the blokus implementation at
# https://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article=1305&context=cpesp
# Blokus Backend - Claire 

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


# Represents a Polyomino Piece. Each piece has a unique ID and remembers its size so
# player score can be easily calculated. 
class Piece:
    def __init__(self):
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
Define all 21 Blokus Pieces. The IDs are meant to help you think of what the shape looks
like, and I tried my best, but I doubt they're actually helpful.

Ultimately, this implementation is pretty slow compared to other blokus implementations I
saw (using a bit board, or using a mix of 2D arrays), but it's more readable, so it's fine.
'''
class C0(Piece):
    def __init__(self):
        self.id = 'C0';
        self.size = 6;
        self.uniques = 4; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x,y+1),(x+3,y+1)];
        self.corners = [(x, y)];

class D0(Piece):
    def __init__(self):
        self.id = 'D0';
        self.size = 6;
        self.uniques = 4; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+1,y+1),(x+2,y+1)];
        self.corners = [(x, y)];

class X0(Piece):
    def __init__(self):
        self.id = 'X0';
        self.size = 6;
        self.uniques = 4; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+1,y+1),(x+2,y-1)];
        self.corners = [(x, y)];

class C1(Piece):
    def __init__(self):
        self.id = 'C1';
        self.size = 6;
        self.uniques = 8; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1),(x+2,y+1),(x+3,y+1)];
        self.corners = [(x, y)];

class W0(Piece):
    def __init__(self):
        self.id = 'W0';
        self.size = 6;
        self.uniques = 8; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y-1),(x+2,y+1),(x+3,y+1)];
        self.corners = [(x, y)];

class Z0(Piece):
    def __init__(self):
        self.id = 'Z0';
        self.size = 6;
        self.uniques = 8; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+2,y+1),(x+2,y+2),(x+3,y+2)];
        self.corners = [(x, y)];


class F0(Piece):
    def __init__(self):
        self.id = 'F0';
        self.size = 6;
        self.uniques = 8; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x,y+1),(x+2,y+1)];
        self.corners = [(x, y)];

class F1(Piece):
    def __init__(self):
        self.id = 'F1';
        self.size = 6;
        self.uniques = 8; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x,y+1),(x+1,y-1)];
        self.corners = [(x, y)];

class F2(Piece):
    def __init__(self):
        self.id = 'F2';
        self.size = 6;
        self.uniques = 8; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x,y+1),(x+2,y-1)];
        self.corners = [(x, y)];

class F3(Piece):
    def __init__(self):
        self.id = 'F3';
        self.size = 6;
        self.uniques = 8; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x+1, y+1),(x+1,y),(x+2,y),(x+3,y),(x,y+1),(x+1,y+2)];
        self.corners = [(x, y)];

class F4(Piece):
    def __init__(self):
        self.id = 'F4';
        self.size = 6;
        self.uniques = 8; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y-1),(x+1,y),(x+2,y),(x+3,y),(x+1,y-1),(x+1,y+1)];
        self.corners = [(x, y)];


class F5(Piece):
    def __init__(self):
        self.id = 'F5';
        self.size = 6;
        self.uniques = 8; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y-1),(x+1,y),(x+2,y),(x+3,y),(x+1,y-1),(x+2,y+1)];
        self.corners = [(x, y)];


class I(Piece):
    def __init__(self):
        self.id = 'I';
        self.size = 5;
        self.uniques = 2; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+4,y)];
        self.corners = [(x, y)];
        
class L(Piece):
    def __init__(self):
        self.id = 'L';
        self.size = 5;
        self.uniques = 8; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x,y+1)];
        self.corners = [(x, y)];

class Y(Piece):
    def __init__(self):
        self.id = 'Y';
        self.size = 5;
        self.uniques = 8; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+1,y+1)];
        self.corners = [(x, y)];

class N(Piece):
    def __init__(self):
        self.id = 'N';
        self.size = 5;
        self.uniques = 8; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y+1),(x+2,y+1)];
        self.corners = [(x, y)];

class U(Piece):
    def __init__(self):
        self.id = 'U';
        self.size = 5;
        self.uniques = 4; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1),(x+2,y+1)];
        self.corners = [(x, y)];
        
class V(Piece):
    def __init__(self):
        self.id = 'V';
        self.size = 5;
        self.uniques = 8; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1),(x,y+2)];
        self.corners = [(x, y)];

class P(Piece):
    def __init__(self):
        self.id = 'P';
        self.size = 5;
        self.uniques = 8; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1),(x+1,y+1)];
        self.corners = [(x, y)];
        
class F(Piece):
    def __init__(self):
        self.id = 'F';
        self.size = 5;
        self.uniques = 8; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1),(x+1,y-1)];
        self.corners = [(x, y)];

class T(Piece):
    def __init__(self):
        self.id = 'T';
        self.size = 5;
        self.uniques = 4; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+1,y+1),(x+1,y+2)];
        self.corners = [(x, y)];
        
class Z(Piece):
    def __init__(self):
        self.id = 'Z';
        self.size = 5;
        self.uniques = 4; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1),(x+2,y-1)];
        self.corners = [(x, y)];
        
class X(Piece):
    def __init__(self):
        self.id = 'X';
        self.size = 5;
        self.uniques = 4; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+1,y+1),(x+1,y-1)];
        self.corners = [(x, y)];
        
class W(Piece):
    def __init__(self):
        self.id = 'W';
        self.size = 5;
        self.uniques = 4; # number of unique transformations per piece, for AI

    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+1,y+1),(x+2,y+1),(x+2,y+2)];
        self.corners = [(x, y)];