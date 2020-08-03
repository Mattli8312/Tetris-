import pygame, random
from Tetris import Shapes
pygame.init()
save_piece = True
game_over = False
dictionary = {}
for i in range(26):
    dictionary.update({470-18*i:i})
class Fonts():
    def __init__(self,x,y,size,color,txt):
        self.x,self.y = x,y
        self.f = pygame.font.SysFont("BahnSchrift",size,True)
        self.txt = self.f.render(txt, True,color)
    def Write(self,surf):
        surf.blit(self.txt, (self.x,self.y))
def Background(surf):
    Title = Fonts(Shapes.Width//2+10, 20, 60, (0,255,255),"Tetris")
    ScoreBoard = Fonts(Shapes.Width//2+20, 80, 30, (255,255,255),  "Score:" + str(Shapes.Score))
    Controls = Fonts(330, 150, 15, (255,255,255), "Controls")
    Left = Fonts(330,170,15,(255,255,255), "<: left")
    Right = Fonts(330,190,15,(255,255,255),">: right")
    Up = Fonts(330,210,15,(255,255,255),"^: Up")
    Down = Fonts(330,230,15,(255,255,255), "\/: Down")
    Save = Fonts(330,250,15,(255,255,255), "s: Save")
    Words = [Title,ScoreBoard,Controls,Left,Right,Up,Down,Save]
    pygame.draw.rect(surf,(255,255,255),(20,20,180,450),5)
    x = y = 20
    for i in range(11):
        pygame.draw.line(surf,(255,255,255),(x,y),(x,y+450))
        x += 18
    x = 20
    for j in range(26):
        pygame.draw.line(surf,(255,255,255),(x,y),(x+180,y))
        y += 18
    for w in Words: w.Write(surf)
def Create_Board(rows):
    board = []
    for i in range(rows+1):
        board.append([])
    return board
def shift_rows(board,i):
    count = 0
    for j in range(i-1,-1,-1):
        if len(board[j]) == 0: count += 1
    for b in board[i]:
        b.y += 18 * count
        board[i-count].append(b)
    while len(board[i]) > 0: board[i].pop(0)
    return board
def delete_rows(board):
    for i in range(len(board)):
        if len(board[i]) >= 10:
            while len(board[i]) > 0: board[i].pop(0)
        elif i > 0 and len(board[i-1]) == 0:
            board = shift_rows(board,i)
    return board
def Rows_deleted(board):
    count = 0
    for rows in board:
        if len(rows) >= 10: count += 1
    Shapes.Score += count * 100
def Update_Board(current,next,board,surf):
    global save_piece, game_over
    current.Rotate(board)
    current.Movement(board)
    if current.dead: game_over = True
    if current.collide:
        for c in current.output:
            board[dictionary[c.y+c.w]].append(c)
        next.x, next.pos = current.x, current.pos
        current = next
        next = Selection(74,20,0)
        Rows_deleted(board)
        board = delete_rows(board)
        save_piece = True
    current.Execute(surf)
    return current, next, board
def Selection(x,y,pos):
    p_num = random.randint(0,6)
    if p_num == 0: Piece = Shapes.Shape(x,y,Shapes.t_piece,pos,Shapes.t_color)
    elif p_num == 1: Piece = Shapes.Shape(x,y,Shapes.s_piece,pos,Shapes.s_color)
    elif p_num == 2: Piece = Shapes.Shape(x,y,Shapes.l_piece,pos,Shapes.l_color)
    elif p_num == 3: Piece = Shapes.Shape(x,y,Shapes.j_piece,pos,Shapes.j_color)
    elif p_num == 4: Piece = Shapes.Shape(x,y,Shapes.i_piece,pos,Shapes.i_color)
    elif p_num == 5: Piece = Shapes.Shape(x,y,Shapes.z_piece,pos,Shapes.z_color)
    else: Piece = Shapes.Shape(x,y,Shapes.b_piece,pos,Shapes.b_color)
    return Piece
def ShowNextPiece(surf, Next):
    Next_Txt = Fonts(220,150,15,(255,255,255),"Next Piece")
    Next_Txt.Write(surf)
    pygame.draw.rect(surf, (255,255,255), (220,180,100,100), 2)
    for i in range(5):
        pygame.draw.line(surf,(255,255,255),(220+i*20,180),(220+i*20,280))
        pygame.draw.line(surf,(255,255,255),(220,180+i*20),(320,180+i*20))
    delta = [0,20,40,60]
    for i in range(len(Next.piece[0])):
        if Next.piece[0][i] == 1:
            pygame.draw.rect(surf,Next.c,(240+delta[i%4],200+delta[i//4],20,20))
            pygame.draw.rect(surf,(255,255,255),(240+delta[i%4],200+delta[i//4],20,20),1)
def SavedPiece(Current, Next, Saved, surf):
    global save_piece
    Sve_Txt =  Fonts(220,290,15,(255,255,255),"Saved Piece")
    Sve_Txt.Write(surf)
    keys = pygame.key.get_pressed()
    delta = [0, 20, 40, 60]
    if keys[pygame.K_s] and save_piece:
        if Saved == None:
            Saved = Current
            Current = Next
            Next = Selection(74,20,Current.pos)
        else:
            holder = Current
            Current = Saved
            Saved = holder
        Current.y, save_piece = 20, False
    if Saved != None:
        for i in range(len(Saved.piece[0])):
            if Saved.piece[0][i] == 1:
                pygame.draw.rect(surf, Saved.c, (240 + delta[i % 4], 340 + delta[i // 4], 20, 20))
    pygame.draw.rect(surf, (255, 255, 255), (220, 320, 100, 100), 2)
    for i in range(5):
        pygame.draw.line(surf, (255, 255, 255), (220 + i * 20, 320), (220 + i * 20, 420))
        pygame.draw.line(surf, (255, 255, 255), (220, 320 + i * 20), (320, 320 + i * 20))
    return Current, Next, Saved
def GameOver(surf):
    Game = Fonts(60,220,30,(255,255,255),"Game")
    Over = Fonts(60,260,30,(255,255,255),"Over")
    Game.Write(surf)
    Over.Write(surf)
def main():
    global game_over
    win = pygame.display.set_mode((Shapes.Width, Shapes.Height))
    pygame.display.set_caption("Tetris")
    Current = Selection(74,20,0)
    Next = Selection(74,20,0)
    Saved = None
    Board = Create_Board(25)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(15)
        if not game_over:
            pygame.time.delay(100)
            win.fill((0,0,0))
            Background(win)
            Current, Next, Board = Update_Board(Current, Next, Board, win)
            Current, Next, Saved = SavedPiece(Current, Next, Saved, win)
            if Current.dead: game_over = True
            ShowNextPiece(win,Next)
            for row in Board:
                for b in row:
                    b.Generate(win)
        else: GameOver(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()
main()