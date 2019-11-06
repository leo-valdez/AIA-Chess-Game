import pygame,time


pygame.init()
pygame.font.init()
display_width,display_height,piece_size = 600,600,75
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Chess Game')
#rook=5,knight=3,bishop=3,queen=9,king=99999,pawn=1
whitepieces = [ pygame.image.load( 'Chess_image/Chess_tile_rl.png' ),pygame.image.load( 'Chess_image/Chess_tile_nl.png' ),pygame.image.load( 'Chess_image/Chess_tile_bl.png' ),pygame.image.load( 'Chess_image/Chess_tile_ql.png' ),pygame.image.load( 'Chess_image/Chess_tile_kl.png' ),pygame.image.load( 'Chess_image/Chess_tile_pl.png' ) ]
blackpieces = [ pygame.image.load( 'Chess_image/Chess_tile_rd.png' ),pygame.image.load( 'Chess_image/Chess_tile_nd.png' ),pygame.image.load( 'Chess_image/Chess_tile_bd.png' ),pygame.image.load( 'Chess_image/Chess_tile_qd.png' ),pygame.image.load( 'Chess_image/Chess_tile_kd.png' ),pygame.image.load( 'Chess_image/Chess_tile_pd.png' ) ]
grey_image = pygame.image.load('Chess_image/grey.png')
chessBoard = pygame.image.load('Chess_image/chess_board.png')
BoardLayout = [['br1','bh1','bb1','bq','0','bb2','bh2','br2'],
               ['bp1','bp2','bp3','bp4','bp5','bp6','bp7','bp8'],               
               ['bk','0','0','0','0','0','0','0'],
               ['0','0','0','0','0','0','0','0'],
               ['0','0','0','0','0','0','0','0'],
               ['0','wr1','0','0','0','0','0','0'],
               ['wp1','wp2','wp3','wp4','wp5','wp6','wp7','wp8'],
               ['0','wh1','wb1','wq','wk','wb2','wh2','wr2']]
#dictionary to hold positions of the pieces of two users
position_black = { 'br1':[0,0],'bh1':[75,0],'bb1':[75*2,0],'bq':[75*3,0],'bk':[75*4,0],'bb2':[75*5,0],'bh2':[75*6,0],'br2':[75*7,0],'bp1':[0,75],'bp2':[75*2,75],'bp3':[75*3,75],'bp4':[75*4,75],'bp5':[75*5,75],'bp6':[75*6,75],'bp7':[75*7,75] }
position_white = { 'wr1':[0,75*7],'wh1':[75,75*7],'wb1':[75*2,75*7],'wq':[75*3,75*7],'wk':[75*4,75*7],'wb2':[75*5,75*7],'wh2':[75*6,75*7],'wr2':[75*7,75*7],'wp1':[0,75*6],'wp2':[75,75*6],'wp3':[75*2,75*6],'wp4':[75*3,75*6],'wp5':[75*4,75*6],'wp6':[75*5,75*6],'p7':[75*6,75*6] }
white,black,grey = (255,255,255),(0,0,0),(83,83,83,50)
Exit = False
clock = pygame.time.Clock()
#draws Chessboard
#Initial printing of Boards and chess pieces
def drawBoard():
    gameDisplay.blit(chessBoard,(0,0))
    for i in range (0,8):
        for j in range (0,8):
            if BoardLayout[i][j] is not '0' and BoardLayout[i][j][0] is 'b':
                if BoardLayout[i][j][1] is 'r':
                    gameDisplay.blit(blackpieces[0], (j*piece_size,i*piece_size))
                elif BoardLayout[i][j][1] is 'h':
                    gameDisplay.blit(blackpieces[1], (j*piece_size,i*piece_size))
                elif BoardLayout[i][j][1] is 'b':
                    gameDisplay.blit(blackpieces[2], (j*piece_size,i*piece_size))
                elif BoardLayout[i][j][1] is 'q':
                    gameDisplay.blit(blackpieces[3], (j*piece_size,i*piece_size))
                elif BoardLayout[i][j][1] is 'k':
                    gameDisplay.blit(blackpieces[4], (j*piece_size,i*piece_size))
                elif BoardLayout[i][j][1] is 'p':
                    gameDisplay.blit(blackpieces[5], (j * piece_size, i * piece_size))
            elif BoardLayout[i][j] is not '0' and BoardLayout[i][j][0] is 'w':
                if BoardLayout[i][j][1] is 'r':
                    gameDisplay.blit(whitepieces[0], (j*piece_size,i*piece_size))
                elif BoardLayout[i][j][1] is 'h':
                    gameDisplay.blit(whitepieces[1], (j*piece_size,i*piece_size))
                elif BoardLayout[i][j][1] is 'b':
                    gameDisplay.blit(whitepieces[2], (j*piece_size,i*piece_size))
                elif BoardLayout[i][j][1] is 'q':
                    gameDisplay.blit(whitepieces[3], (j*piece_size,i*piece_size))
                elif BoardLayout[i][j][1] is 'k':
                    gameDisplay.blit(whitepieces[4], (j*piece_size,i*piece_size))
                elif BoardLayout[i][j][1] is 'p':
                    gameDisplay.blit(whitepieces[5], (j * piece_size, i * piece_size))
            else:
                continue

    pygame.display.update()

                
class pieces:
    greySurface=[]
    #possibilities of movement of rook
    def possibleMove(self):
        for gs in self.greySurface:
            pygame.draw.rect(gameDisplay,(220,220,220),[gs[1]*piece_size,gs[0]*piece_size,piece_size,piece_size])
            pygame.display.update()
    def find_ele(self,value):
        flag = False
        for i in range(8):#len(BoardLayout[0])
            for j in range(8):
                x =BoardLayout[i][j].find(value)
                if x != -1:
                    flag=True
                    break
            if(flag):   break
        return [i,j]

    def mov_rook(self, value):
        pos = self.find_ele(value)
        print(pos)
        temp_add = [[1, 0], [-1,0], [0, 1], [0, -1]]
        for i in range(4):
            t_x = pos[0]
            t_y = pos[1]
            while True:
                t_x = t_x + temp_add[i][0]
                t_y = t_y + temp_add[i][1]
                if t_x in range(0, 8) and t_y in range(0, 8) and BoardLayout[t_x][t_y][0] is not value[0]:
                    if BoardLayout[t_x][t_y][0] is not '0':
                        self.greySurface.append([t_x, t_y])
                        break
                    elif BoardLayout[t_x][t_y][0] is '0':
                        self.greySurface.append([t_x, t_y])

                else:
                    break
        print(self.greySurface)
        self.possibleMove()
    def mov_knight(self,value):
        pos = self.find_ele(value)
        print(pos)
        temp_add=[[1,2],[-1,2],[-1,-2],[1,-2],[2,-1],[-2,-1],[2,1],[-2,1]]
        for i in range(8):
            if pos[0]+temp_add[i][0] in range(0,8) and pos[1]+temp_add[i][1] in range(0,8) and BoardLayout[pos[0]+temp_add[i][0]][pos[1]+temp_add[i][1]][0] is not value[0]:
                self.greySurface.append([pos[0]+temp_add[i][0],pos[1]+temp_add[i][1]])
        self.possibleMove()
    def mov_bishop(self,value):
        pos = self.find_ele(value)
        print(pos)
        temp_add=[[1,-1],[-1,1],[1,1],[-1,-1]]
        for i in range(4):
            t_x = pos[0]
            t_y = pos[1]
            while True:
                t_x = t_x + temp_add[i][0]
                t_y = t_y + temp_add[i][1]
                if t_x in range(0,8) and t_y in range(0,8) and BoardLayout[t_x][t_y][0] is not value[0]:
                    if BoardLayout[t_x][t_y][0] is not '0':
                        self.greySurface.append([t_x,t_y])
                        break
                    elif BoardLayout[t_x][t_y][0] is '0':
                        self.greySurface.append([t_x,t_y])
                        
                else:
                    break
        print(self.greySurface)
        self.possibleMove()
    def mov_queen(self,value):
        pos = self.find_ele(value)
        print(pos)
        temp_add=[[1,-1],[-1,1],[1,1],[-1,-1],[0,1],[1,0],[0,-1],[-1,0]]
        for i in range(8):
            t_x = pos[0]
            t_y = pos[1]
            while True:
                t_x = t_x + temp_add[i][0]
                t_y = t_y + temp_add[i][1]
                if t_x in range(0,8) and t_y in range(0,8) and BoardLayout[t_x][t_y][0] is not value[0]:
                    if BoardLayout[t_x][t_y][0] is not '0':
                        self.greySurface.append([t_x,t_y])
                        break
                    elif BoardLayout[t_x][t_y][0] is '0':
                        self.greySurface.append([t_x,t_y])
                        
                else:
                    break
        print(self.greySurface)
        self.possibleMove()
    def mov_king(self,value):
        pos = self.find_ele(value)
        print(pos)
        temp_add=[[1,-1],[-1,1],[1,1],[-1,-1],[0,1],[1,0],[0,-1],[-1,0]]
        for i in range(8):
            if pos[0]+temp_add[i][0] in range(0,8) and pos[1]+temp_add[i][1] in range(0,8) and BoardLayout[pos[0]+temp_add[i][0]][pos[1]+temp_add[i][1]][0] is not value[0]:
                self.greySurface.append([pos[0]+temp_add[i][0],pos[1]+temp_add[i][1]])
        self.possibleMove()





#######################MAIN    
drawBoard()
playerW = pieces()
playerW.mov_rook('wr1')
playerB = pieces()
playerB.mov_king('bk')

while not Exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            
    
    
    
