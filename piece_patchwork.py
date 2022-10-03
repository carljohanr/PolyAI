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

    # Flip the board; any flip is valid for the board.
    def flip(self, orientation):
        def flip_h(pt):
            x1 = self.refpt[0];
            x2 = pt[0];
            x1 = (x1 - (x2 - x1));
            return (x1, pt[1]);

        if orientation == 'h':
            self.points = [flip_h(pt) for pt in self.points];


'''
Define 17 shapes in Isle of Cats base game
'''


# big_pieces = [[[1,0,0],[1,1,1],[1,0,1]],[[1,1,1,1],[0,1,0,0],[0,1,0,0]],[[1,1,1,0],[0,1,1,1]],\
#             [[0,1,1],[1,1,1],[0,0,1]],[[0,1,0,0],[1,1,1,1],[0,1,0,0]],[[0,1,1,1],[1,1,0,1]],\
#           [[0,1,0],[1,1,1],[0,1,0]],[[1,1,1],[0,1,0],[0,1,0]],[[1,1,1,1,1]],\
#               [[0,1,1],[1,1,0],[1,0,0]],[[1,1,1],[1,0,0],[1,0,0]],[[1,1,1],[1,0,1]],[[1,1,1],[1,1,0]],\
#         [[0,1,1,1],[1,1,0,0]],[[1,1,1,1],[0,1,0,0]],[[1,1,1,1],[1,0,0,0]],[[1,1,0],[0,1,1]]]


class A(Piece):
    def __init__(self):
        self.size = 2;
        self.cost=2
        self.time=1
        self.income=0
        self.id = 'A';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y)];

class B(Piece):
    def __init__(self):
        self.size = 3;
        self.cost=1
        self.time=3
        self.income=0
        self.id = 'B';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x,y+1)];
        
        
class C(Piece):
    def __init__(self):
        self.size = 3;
        self.cost=3
        self.time=1
        self.income=0
        self.id = 'C';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x,y+1)];
        
        
class D(Piece):
    def __init__(self):
        self.size = 3;
        self.cost=2
        self.time=2
        self.income=0
        self.id = 'D';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y)];
        
class E(Piece):
    def __init__(self):
        self.size = 4;
        self.cost=3
        self.time=2
        self.income=1
        self.id = 'E';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+1,y+1),(x+2,y+1)];
        
class F(Piece):
    def __init__(self):
        self.size = 5;
        self.cost=2
        self.time=2
        self.income=0
        self.id = 'F';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1),(x+1,y+1)];

class G(Piece):
    def __init__(self):
        self.size = 7;
        self.cost=1
        self.time=4
        self.income=1
        self.id = 'G';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+4,y),(x+2,y-1),(x+2,y+1)];
        
class H(Piece):
    def __init__(self):
        self.size = 6;
        self.cost=0
        self.time=3
        self.income=1
        self.id = 'H';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+2,y-1),(x+2,y+1)];


class I(Piece):
    def __init__(self):
        self.size = 4;
        self.cost=6
        self.time=5
        self.income=2
        self.id = 'I';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x,y+1),(x+1,y+1)];
        
class J(Piece):
    def __init__(self):
        self.size = 6;
        self.cost=4
        self.time=2
        self.income=0
        self.id = 'J';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+1,y+1),(x+2,y+1),(x+3,y+1)];
        
class K(Piece):
    def __init__(self):
        self.size = 4;
        self.cost=2
        self.time=2
        self.income=0
        self.id = 'K';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+1,y+1)];
        
class L(Piece):
    def __init__(self):
        self.size = 6;
        self.cost=1
        self.time=5
        self.income=1
        self.id = 'L';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x,y+1),(x+3,y+1)];
        
class M(Piece):
    def __init__(self):
        self.size = 4;
        self.cost=3
        self.time=3
        self.income=1
        self.id = 'M';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y)];



class N(Piece):
    def __init__(self):
        self.size = 5;
        self.cost=7
        self.time=1
        self.income=1
        self.id = 'N';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+4,y)];

class O(Piece):
    def __init__(self):
        self.size = 5;
        self.cost=3
        self.time=4
        self.income=1
        self.id = 'O';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+1,y+1)];



class P(Piece):
    def __init__(self):
        self.size = 6;
        self.cost=7
        self.time=4
        self.income=2
        self.id = 'P';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+1,y+1),(x+2,y+1)];


class Q(Piece):
    def __init__(self):
        self.size = 6;
        self.cost=3
        self.time=6
        self.income=2
        self.id = 'Q';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+1,y+1),(x+2,y+1),(x,y+2),(x+1,y+2)];


class R(Piece):
    def __init__(self):
        self.size = 6;
        self.cost=2
        self.time=1
        self.income=0
        self.id = 'R';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+1,y+1),(x+2,y-1)];


class S(Piece):
    def __init__(self):
        self.size = 4;
        self.cost=4
        self.time=6
        self.income=2
        self.id = 'S';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1)];        


class T(Piece):
    def __init__(self):
        self.size = 5;
        self.cost=5
        self.time=4
        self.income=2
        self.id = 'T';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+1,y-1),(x+1,y+1)];            


class U(Piece):
    def __init__(self):
        self.size = 7;
        self.cost=2
        self.time=3
        self.income=0
        self.id = 'U';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+1,y+1),(x, y+2),(x+1,y+2),(x+2,y+2)];    
        

class V(Piece):
    def __init__(self):
        self.size = 8;
        self.cost=5
        self.time=3
        self.income=1
        self.id = 'V';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1),(x+2,y+1),(x,y+2),(x+1,y+2)];    
        

class W(Piece):
    def __init__(self):
        self.size = 5;
        self.cost=10
        self.time=3
        self.income=2
        self.id = 'W';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x,y+1)];    


class X(Piece):
    def __init__(self):
        self.size = 5;
        self.cost=5
        self.time=5
        self.income=2
        self.id = 'X';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y-1),(x,y+1)];   
        
        
class Y(Piece):
    def __init__(self):
        self.size = 6;
        self.cost=10
        self.time=5
        self.income=3
        self.id = 'Y';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x,y+1),(x+1,y+1)]; 
        
        
class Z(Piece):
    def __init__(self):
        self.size = 6;
        self.cost=1
        self.time=2
        self.income=0
        self.id = 'Z';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x,y-1),(x+3,y+1)]; 
        
class a(Piece):
    def __init__(self):
        self.size = 4;
        self.cost=4
        self.time=2
        self.income=1
        self.id = 'a';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1)]; 
        

class b(Piece):
    def __init__(self):
        self.size = 6;
        self.cost=7
        self.time=2
        self.income=2
        self.id = 'b';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x,y-1),(x,y+1)]; 
        
class c(Piece):
    def __init__(self):
        self.size = 5;
        self.cost=10
        self.time=4
        self.income=3
        self.id = 'c';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+1,y+1),(x+2,y+1),(x+2,y+2)]; 
        

class d(Piece):
    def __init__(self):
        self.size = 5;
        self.cost=1
        self.time=2
        self.income=0
        self.id = 'd';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x,y+1),(x+2,y+1)]; 
        
        
class e(Piece):
    def __init__(self):
        self.size = 5;
        self.cost=2
        self.time=3
        self.income=1
        self.id = 'e';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+2,y+1),(x+3,y+1)]; 
        

class f(Piece):
    def __init__(self):
        self.size = 4;
        self.cost=7
        self.time=6
        self.income=3
        self.id = 'f';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+1,y+1),(x+2,y+1)]; 
        
class g(Piece):
    def __init__(self):
        self.size = 6;
        self.cost=8
        self.time=6
        self.income=3
        self.id = 'g';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x,y+1),(x+1,y+1),(x+2,y+1),(x+2,y+2)]; 
        

class h(Piece):
    def __init__(self):
        self.size = 1;
        self.cost=0
        self.time=0
        self.income=0
        self.id = 'X';
        
    def set_points(self, x, y):
        self.points = [(x, y)]; 