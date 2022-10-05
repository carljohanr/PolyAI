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


# class Pass(Piece):
#     def __init__(self,color):
#         self.size = 0;
#         self.uniques = 1; # number of unique transformations per piece, for AI
#         self.color=color
#         self.id = 'Pass'+str(self.color);
        
#     def set_points(self, x, y):
#         self.points = [];
#         self.corners = [];
    
class G1(Piece):
    def __init__(self,count):
        self.size = 1;
        self.color=1
        self.count = count
        self.score = 0
        self.id = 'G1'+str(self.count);
        
    def set_points(self, x, y):
        self.points = [(x, y)];

class G2(Piece):
    def __init__(self,count):
        self.size = 2;
        self.color=1
        self.count = count
        self.score = 0
        self.id = 'G2'+str(self.count);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1)];


class G3(Piece):
    def __init__(self,count):
        self.size = 3;
        self.color=1
        self.count = count
        self.score = 0
        self.id = 'G3'+str(self.count);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x+1,y)];


class G4(Piece):
    def __init__(self,count):
        self.size = 3;
        self.color=1
        self.count = count
        self.score = 0
        self.id = 'G4'+str(self.count);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x,y+2)];



class A1(Piece):
    def __init__(self,score):
        self.size = 4;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=2
        self.animal = 'Koala'
        self.score = score
        self.id = 'A1'+str(self.score);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x+1,y),(x+2,y)];

class A2(Piece):
    def __init__(self,score):
        self.size = 4;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=3
        self.animal = 'Panda'
        self.score = score
        self.id = 'A2'+str(self.score);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x+1,y+1),(x+1,y+2)];
        
        
class A3(Piece):
    def __init__(self,score):
        self.size = 4;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=4
        self.animal = 'Polar'
        self.score = score
        self.id = 'A3'+str(self.score);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x+1,y+1),(x,y+2)];
        
class A4(Piece):
    def __init__(self,score):
        self.size = 4;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=5
        self.animal = 'Gobi'
        self.score = score
        self.id = 'A4'+str(self.score);
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x+1,y+1),(x+1,y)];
        
        
        
class E1(Piece):
    def __init__(self):
        self.size = 5;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=2
        self.animal = 'Koala'
        self.score = 8
        self.id = 'E1';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x+1,y),(x+2,y),(x+2,y+1)];
        
class E2(Piece):
    def __init__(self):
        self.size = 5;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=2
        self.animal = 'Koala'
        self.score = 7
        self.id = 'E2';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x+1,y),(x+2,y),(x,y+2)];
           
class E3(Piece):
    def __init__(self):
        self.size = 5;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=2
        self.animal = 'Koala'
        self.score = 6
        self.id = 'E3';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x+1,y),(x+2,y),(x+3,y)];

    

class E4(Piece):
    def __init__(self):
        self.size = 5;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=3
        self.animal = 'Panda'
        self.score = 8
        self.id = 'E4';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x+1,y+1),(x+1,y+2),(x+2,y+2)];
        
class E5(Piece):
    def __init__(self):
        self.size = 5;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=3
        self.animal = 'Panda'
        self.score = 7
        self.id = 'E5';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x+1,y+1),(x+1,y+2),(x+1,y+3)];
           
class E6(Piece):
    def __init__(self):
        self.size = 5;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=3
        self.animal = 'Panda'
        self.score = 6
        self.id = 'E6';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x,y+2),(x,y+3),(x+1,y+1)];
        
        
class E7(Piece):
    def __init__(self):
        self.size = 5;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=4
        self.animal = 'Polar'
        self.score = 8
        self.id = 'E7';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x+1,y),(x-1,y),(x,y-1)];
        
class E8(Piece):
    def __init__(self):
        self.size = 5;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=4
        self.animal = 'Polar'
        self.score = 7
        self.id = 'E8';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x,y+2),(x+1,y+1),(x+2,y+1)];
           
class E9(Piece):
    def __init__(self):
        self.size = 5;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=4
        self.animal = 'Polar'
        self.score = 6
        self.id = 'E9';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x,y+2),(x,y+3),(x,y+4)];
        
        
class E10(Piece):
    def __init__(self):
        self.size = 5;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=5
        self.animal = 'Gobi'
        self.score = 8
        self.id = 'E10';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x+1,y+1),(x+2,y+1),(x+2,y+2)];
        
class E11(Piece):
    def __init__(self):
        self.size = 5;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=5
        self.animal = 'Gobi'
        self.score = 7
        self.id = 'E11';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x,y+2),(x-1,y),(x+1,y+1)];
           
class E12(Piece):
    def __init__(self):
        self.size = 5;
        self.uniques = 1; # number of unique transformations per piece, for AI
        self.color=5
        self.animal = 'Gobi'
        self.score = 6
        self.id = 'E12';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x+1,y),(x+1,y+1),(x+2,y)];
        
        
class GR1(Piece):
    def __init__(self):
        self.size = 7;
        self.color=6
        self.animal = 'Grizzly'
        self.score = 10
        self.id = 'GR1';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+2,y),(x+3,y),(x+1,y+1),(x+1,y+2),(x+1,y+3)];

        
class GR2(Piece):
    def __init__(self):
        self.size = 7;
        self.color=6
        self.animal = 'Grizzly'
        self.score = 10
        self.id = 'GR2';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x+1,y),(x+1,y+1),(x+1,y+2),(x+2,y+2),(x+2,y+3),(x+3,y+3)];
        

class GR3(Piece):
    def __init__(self):
        self.size = 7;
        self.color=6
        self.animal = 'Grizzly'
        self.score = 10
        self.id = 'GR3';
        
    def set_points(self, x, y):
        self.points = [(x, y+1),(x+1,y),(x+1,y+1),(x+2,y+1),(x+2,y+2),(x+2,y+3),(x+3,y+2)];
        
class GR4(Piece):
    def __init__(self):
        self.size = 7;
        self.color=6
        self.animal = 'Grizzly'
        self.score = 9
        self.id = 'GR4';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x,y+2),(x,y+3),(x+1,y+1),(x+2,y),(x+2,y+1)];
        
class GR5(Piece):
    def __init__(self):
        self.size = 7;
        self.color=6
        self.animal = 'Grizzly'
        self.score = 9
        self.id = 'GR5';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x,y+2),(x,y+3),(x+1,y),(x+2,y),(x+1,y+3)];
        
        
class GR6(Piece):
    def __init__(self):
        self.size = 7;
        self.color=6
        self.animal = 'Grizzly'
        self.score = 9
        self.id = 'GR6';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x,y+2),(x-1,y+2),(x-1,y+3),(x+1,y+2),(x+1,y+3)];
        
        
class GR7(Piece):
    def __init__(self):
        self.size = 7;
        self.color=6
        self.animal = 'Grizzly'
        self.score = 8
        self.id = 'GR7';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x,y+2),(x+1,y+1),(x+2,y),(x+2,y+1),(x+2,y+2)];
        
        
class GR8(Piece):
    def __init__(self):
        self.size = 7;
        self.color=6
        self.animal = 'Grizzly'
        self.score = 8
        self.id = 'GR8';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x,y+2),(x+1,y),(x+2,y),(x+2,y+1),(x+2,y+2)];
        
        
class GR9(Piece):
    def __init__(self):
        self.size = 7;
        self.color=6
        self.animal = 'Grizzly'
        self.score = 8
        self.id = 'GR9';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x,y+2),(x+1,y),(x+2,y),(x+1,y+2),(x+2,y+1)];
        
        
        
class GR10(Piece):
    def __init__(self):
        self.size = 7;
        self.color=6
        self.animal = 'Grizzly'
        self.score = 7
        self.id = 'GR10';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x,y+2),(x+1,y),(x+1,y+1),(x+1,y+2),(x+2,y+1)];
        
        
class GR11(Piece):
    def __init__(self):
        self.size = 7;
        self.color=6
        self.animal = 'Grizzly'
        self.score = 7
        self.id = 'GR11';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x+2,y+2),(x+1,y),(x+1,y+1),(x+1,y+2),(x+2,y+1)];
        
        
class GR12(Piece):
    def __init__(self):
        self.size = 7;
        self.color=6
        self.animal = 'Grizzly'
        self.score = 7
        self.id = 'GR12';
        
    def set_points(self, x, y):
        self.points = [(x, y),(x,y+1),(x,y+2),(x,y+3),(x+1,y),(x+1,y+1),(x+1,y+3)];