import pygame
pygame.init()
Width, Height = 400, 500
Score = 0
class Cubes():
    def __init__(self,x,y,w,color):
        self.x,self.y = x,y
        self.w,self.c = w,color
    def Generate(self,surf):
        pygame.draw.rect(surf,self.c,(self.x,self.y,self.w,self.w))
        pygame.draw.rect(surf,(255,255,255),(self.x,self.y,self.w,self.w),1)
class Shape():
    delta = [0,18,36,54]
    def __init__(self,x,y,piece,pos,color):
        self.x,self.y = x,y
        self.delta_y = 0
        self.piece, self.c = piece, color
        self.dead = False
        self.output = []
        self.pos, self.collide = pos, False
        if self.collide: self.collide = False
    def Execute(self,surf):
        while len(self.output) > 0: self.output.pop(0)
        for i in range(len(self.piece[self.pos])):
            if self.piece[self.pos][i] == 1: self.output.append(Cubes(self.x+self.delta[i%4],self.y+self.delta[i//4],18,self.c))
        for o in self.output: o.Generate(surf)
    def Movement(self, board):
        for o in self.output:
            if o.y + o.w >= 470:
                self.collide = True
                break
        for row in board:
            for b in row:
                for o in self.output:
                    if b.x == o.x and b.y == o.y+o.w:
                        self.collide = True
                        if self.y <= 20: self.dead = True
                        break
        if not(self.collide):
            self.y += 18
        else:
            self.x = 74
            self.y = 20
            self.delta = 0
    def Rotate(self,board):
        keys = pygame.key.get_pressed()
        next_piece = None
        if keys[pygame.K_UP]:
            index = self.pos + 1
            if index >= 4: index = 0
            next_piece = self.piece[index]
            if not self.Wall_Detection(next_piece) and not self.Neighbor_Detection(next_piece,board):
                self.pos += 1
        elif keys[pygame.K_DOWN]:
            index = self.pos + 1
            if index <= -1: index = 3
            next_piece = self.piece[index]
            if not self.Wall_Detection(next_piece) and not self.Neighbor_Detection(next_piece, board):
                self.pos -= 1
        if keys[pygame.K_LEFT] and not self.walls(True,False):
            if not self.neighbors(True,False,board): self.x -= 18
        elif keys[pygame.K_RIGHT] and not self.walls(False,True):
            if not self.neighbors(False,True,board): self.x += 18
        if self.pos >= 4: self.pos = 0
        elif self.pos <= -1: self.pos = 3
    def neighbors(self,left,right,board):
        for row in board:
            for b in row:
                for o in self.output:
                    if left:
                        if o.x == b.x + b.w and o.y + o.w == b.y: return True
                    else:
                        if o.x + o.w == b.x and o.y + o.w == b.y: return True
        return False
    def walls(self,left,right):
        for o in self.output:
            if left:
                if o.x <= 20: return True
            else:
                if o.x + o.w >= 200: return True
        return False
    def Wall_Detection(self, piece):
        next_output_coords = []
        delta = [0, 18, 36, 54]
        for i in range(len(piece)):
            if piece[i] == 1: next_output_coords.append(self.x + delta[i%4])
        for cords in next_output_coords:
            if cords < 20 or cords + 18 > 200: return True
        return False
    def Neighbor_Detection(self, piece, board):
        next_output_coords = []
        delta = [0, 18, 36, 54]
        for i in  range(len(piece)):
            if piece[i] == 1: next_output_coords.append([self.x+delta[i%4],self.y+delta[i//4]])
        for cords in next_output_coords:
            for rows in board:
                for b in rows:
                    if cords[0] == b.x and cords[1] == b.y: return True
        return False
#Shapes
#T Shape
t1 = [0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0]
t2 = [0,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0]
t3 = [0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0]
t4 = [0,1,0,0,0,1,1,0,0,1,0,0,0,0,0,0]
t_piece, t_color = [t1,t2,t3,t4], (255,0,255)
#S Shape
s1 = [0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0]
s2 = [1,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0]
s3 = [0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0]
s4 = [0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,0]
s_piece, s_color = [s1,s2,s3,s4], (0,255,0)
#L Shape
l1 = [0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0]
l2 = [1,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0]
l3 = [0,0,0,0,1,1,1,0,1,0,0,0,0,0,0,0]
l4 = [0,1,0,0,0,1,0,0,0,1,1,0,0,0,0,0]
l_piece, l_color = [l1,l2,l3,l4], (255,128,0)
#J Shape
j1 = [1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0]
j2 = [0,1,0,0,0,1,0,0,1,1,0,0,0,0,0,0]
j3 = [0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0]
j4 = [0,1,1,0,0,1,0,0,0,1,0,0,0,0,0,0]
j_piece, j_color = [j1,j2,j3,j4], (0,0,255)
#Box Shape
b1 = [0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0]
b_piece, b_color = [b1,b1,b1,b1], (255,255,0)
#I Shape
i1 = [0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0]
i2 = [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0]
i3 = [0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0]
i4 = [0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0]
i_piece, i_color = [i1,i2,i3,i4], (0,255,255)
#Z Shape
z1 = [1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0]
z2 = [0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0]
z3 = [0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0]
z4 = [0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0]
z_piece, z_color = [z1,z2,z3,z4], (255,0,0)