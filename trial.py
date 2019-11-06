import pygame, time,copy


pygame.init()
pygame.font.init()
display_width, display_height, piece_size = 600, 600, 75
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Chess Game')
# rook=5,knight=3,bishop=3,queen=9,king=99999,pawn=1
whitepieces = [pygame.image.load('Chess_image/Chess_tile_rl.png'), pygame.image.load('Chess_image/Chess_tile_nl.png'),
               pygame.image.load('Chess_image/Chess_tile_bl.png'), pygame.image.load('Chess_image/Chess_tile_ql.png'),
               pygame.image.load('Chess_image/Chess_tile_kl.png'), pygame.image.load('Chess_image/Chess_tile_pl.png')]
blackpieces = [pygame.image.load('Chess_image/Chess_tile_rd.png'), pygame.image.load('Chess_image/Chess_tile_nd.png'),
               pygame.image.load('Chess_image/Chess_tile_bd.png'), pygame.image.load('Chess_image/Chess_tile_qd.png'),
               pygame.image.load('Chess_image/Chess_tile_kd.png'), pygame.image.load('Chess_image/Chess_tile_pd.png')]
grey_image = pygame.image.load('Chess_image/grey.png')
chessBoard = pygame.image.load('Chess_image/chess_board.png')
BoardLayout = [['br1', 'bh1', 'bb1', 'bq', 'bk', 'bb2', 'bh2', 'br2'],
               ['bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'],
               ['0', '0', '0', '0', '0', '0', '0', '0'],
               ['0', '0', '0', '0', '0', '0', '0', '0'],
               ['0', '0', '0', '0', '0', '0', '0', '0'],
               ['0', '0', '0', '0', '0', '0', '0', '0'],
               ['wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
               ['wr1', 'wh1', 'wb1', 'wq', 'wk', 'wb2', 'wh2', 'wr2']]

temp=[] #USed to store the previous move
white, black, grey,red = (255, 255, 255), (0, 0, 0), (83, 83, 83, 50),(255,0,0)
white_check=False
black_check=False
Exit = False
player=1
clock = pygame.time.Clock()
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)


# draws Chessboard

def drawBoard():
    gameDisplay.blit(chessBoard, (0, 0))
    for i in range(0, 8):
        for j in range(0, 8):
            if BoardLayout[i][j] is not '0' and BoardLayout[i][j][0] is 'b':
                if BoardLayout[i][j][1] is 'r':
                    gameDisplay.blit(blackpieces[0], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'h':
                    gameDisplay.blit(blackpieces[1], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'b':
                    gameDisplay.blit(blackpieces[2], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'q':
                    gameDisplay.blit(blackpieces[3], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'k':
                    gameDisplay.blit(blackpieces[4], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'p':
                    gameDisplay.blit(blackpieces[5], (j * piece_size, i * piece_size))
            elif BoardLayout[i][j] is not '0' and BoardLayout[i][j][0] is 'w':
                if BoardLayout[i][j][1] is 'r':
                    gameDisplay.blit(whitepieces[0], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'h':
                    gameDisplay.blit(whitepieces[1], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'b':
                    gameDisplay.blit(whitepieces[2], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'q':
                    gameDisplay.blit(whitepieces[3], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'k':
                    gameDisplay.blit(whitepieces[4], (j * piece_size, i * piece_size))
                elif BoardLayout[i][j][1] is 'p':
                    gameDisplay.blit(whitepieces[5], (j * piece_size, i * piece_size))
            else:
                continue

    pygame.display.update()

#Function to Print the Value of the current positon Eg. a5,e6 etc
def print_pos(mouse_pointer):
    mouse_pointer[1]=chr(97+mouse_pointer[1])
    pointer=str(mouse_pointer[1])+str(mouse_pointer[0])
    return pointer

class pieces:
    greySurface = []
    # flag_check=is_check()

    def possibleMove(self):
        for gs in self.greySurface:
            gameDisplay.blit(grey_image,(gs[1] * piece_size, gs[0] * piece_size))
            pygame.display.update()

    def find_ele(self, value):
        flag = False
        for i in range(8):  # len(BoardLayout[0])
            for j in range(8):
                x = BoardLayout[i][j].find(value)
                if x != -1:
                    flag = True
                    break
            if (flag):   break
        if flag is False:
            return [i + 1, j + 1]
        return [i, j]

    def mov_item(self,value):
        self.greySurface=[]
        print(value)
        if value[1] is 'r':
            self.mov_rook(value)
        elif value[1] is 'h':
            self.mov_knight(value)
        elif value[1] is 'b':
            self.mov_bishop(value)
        elif value[1] is 'q':
            self.mov_queen(value)
        elif value[1] is 'k':
            self.mov_king(value)
        elif value[1] is 'p':
            self.mov_pawn(value)
        else:
            print("Haha")

    def mov_pawn(self,value):
        pos = self.find_ele(value)
        if value[0] == 'b' and pos[0] == 1 :
            if BoardLayout[pos[0]+1][pos[1]][0] is '0':
                self.greySurface.append([pos[0]+1, pos[1] ])
            if BoardLayout[pos[0]+2][pos[1]][0] is '0' and BoardLayout[pos[0]+1][pos[1]][0] is '0':
                self.greySurface.append([pos[0]+2, pos[1]])
        if value[0] == 'b'  and pos[0]+1 in range(0,8) and pos[1]+1 in range(0,8) and BoardLayout[pos[0]+1][pos[1]+1][0] is not value[0] and BoardLayout[pos[0]+1][pos[1]+1][0] is not '0' :
            self.greySurface.append([pos[0]+1, pos[1] +1])
        if value[0] == 'b' and pos[0]+1 in range(0,8) and pos[1]-1 in range(0,8) and BoardLayout[pos[0]+1][pos[1]-1][0] is not value[0] and BoardLayout[pos[0]+1][pos[1]-1][0] is not '0' :
            self.greySurface.append([pos[0]+1, pos[1] -1])
        if value[0] == 'b'  and pos[0]+1 in range(0,8) and pos[1]-1 in range(0,8) and pos[0] is not 1 and BoardLayout[pos[0]+1][pos[1]][0] is '0':
            self.greySurface.append([pos[0]+1, pos[1] ])
        if value[0] == 'w' and pos[0] == 6 :
            if BoardLayout[pos[0]-1][pos[1]][0] is '0':
                self.greySurface.append([pos[0]-1, pos[1] ])
            if BoardLayout[pos[0]-2][pos[1]][0] is '0' and BoardLayout[pos[0]-1][pos[1]][0] is '0':
                self.greySurface.append([pos[0]-2, pos[1]])
        if value[0] == 'w' and pos[0]-1 in range(0,8) and pos[1]+1 in range(0,8) and BoardLayout[pos[0]-1][pos[1]+1][0] is not value[0] and BoardLayout[pos[0]-1][pos[1]+1][0] is not '0' :
            self.greySurface.append([pos[0]-1, pos[1] +1])
        if value[0] == 'w' and pos[0]-1 in range(0,8) and pos[1]-1 in range(0,8) and BoardLayout[pos[0]-1][pos[1]-1][0] is not value[0] and BoardLayout[pos[0]-1][pos[1]-1][0] is not '0' :
            self.greySurface.append([pos[0]-1, pos[1] -1])
        if value[0] == 'w' and pos[0] is not 1  and pos[0]-1 in range(0,8) and pos[1] in range(0,8) and BoardLayout[pos[0]-1][pos[1]][0] is '0' :
            self.greySurface.append([pos[0]-1, pos[1] ])



    def mov_rook(self, value):
        pos = self.find_ele(value)
        temp_add = [[1, 0], [-1, 0], [0, 1], [0, -1]]
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

    def mov_knight(self, value):
        pos = self.find_ele(value)
        temp_add = [[1, 2], [-1, 2], [-1, -2], [1, -2], [2, -1], [-2, -1], [2, 1], [-2, 1]]
        for i in range(8):
            if pos[0] + temp_add[i][0] in range(0, 8) and pos[1] + temp_add[i][1] in range(0, 8) and \
                    BoardLayout[pos[0] + temp_add[i][0]][pos[1] + temp_add[i][1]][0] is not value[0]:
                self.greySurface.append([pos[0] + temp_add[i][0], pos[1] + temp_add[i][1]])

    def mov_bishop(self, value):
        pos = self.find_ele(value)
        temp_add = [[1, -1], [-1, 1], [1, 1], [-1, -1]]
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


    def mov_queen(self, value):
        pos = self.find_ele(value)
        temp_add = [[1, -1], [-1, 1], [1, 1], [-1, -1], [0, 1], [1, 0], [0, -1], [-1, 0]]
        for i in range(8):
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

    def mov_king(self, value):
        pos = self.find_ele(value)
        temp_add = [[1, -1], [-1, 1], [1, 1], [-1, -1], [0, 1], [1, 0], [0, -1], [-1, 0]]
        for i in range(8):
            if pos[0] + temp_add[i][0] in range(0, 8) and pos[1] + temp_add[i][1] in range(0, 8) and \
                    BoardLayout[pos[0] + temp_add[i][0]][pos[1] + temp_add[i][1]][0] is not value[0]:
                self.greySurface.append([pos[0] + temp_add[i][0], pos[1] + temp_add[i][1]])

def text_objects(text,color,size):
    if size=='small':
        textSurface=smallfont.render(text,True,color)
    elif size=='medium':
        textSurface=medfont.render(text,True,color)
    elif size=='large':
        textSurface=largefont.render(text,True,color)
    return textSurface,textSurface.get_rect()


def message_to_screen(msg,color,y_displace=0,size = "small"):
    textSurface,textRect=text_objects(msg,color,size)
    textRect.center=(display_width/2),(display_height/2)+y_displace
    gameDisplay.blit(textSurface,textRect)

def game_intro():
    intro = True

    while intro:
        gameDisplay.fill(white)
        message_to_screen("Chess",black,-40,"large")
        message_to_screen("Press q to Quit",red,40)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(15)

def game_ex(player):
    ex = True

    while ex:
        gameDisplay.fill(white)
        message_to_screen("Game Over",black,-40,"large")
        message_to_screen("Player Won",red,40)
        message_to_screen(player, red, 80)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(15)

#Checking checkmate before theplayer moves its positon
def check_mate():
    p=pieces()
    global player,black_check,white_check
    if(player==1):
        v='b'
        v1='w'
    else:
        v='w'
        v1='b'
    all_moves=p.mov_item(v+'p1')+p.mov_item(v+'p2')+p.mov_item(v+'p3')+p.mov_item(v+'p4')+p.mov_item(v+'p4')+\
              p.mov_item(v+'p6')+p.mov_item(v+'p7')+p.mov_item(v+'p8')+p.mov_item(v+'r2')+p.mov_item(v+'h1')+\
              p.mov_item(v+'h2')+p.mov_item(v+'b2')+p.mov_item(v+'b1')+p.mov_item(v+'q')+p.mov_item(v+'k')+\
              p.mov_item(v+'r1')
    pos=p.find_ele(v1+'k')
    if pos in all_moves:
        if player==1:
            white_check=True
        else:
            black_check=True

def get_display(mouse):
    l=[]
    global player
    check_mate()
    if BoardLayout[mouse[0]][mouse[1]][0] is 'w' and player is 1 :
        p=pieces()
        p.mov_item(BoardLayout[mouse[0]][mouse[1]])
        l=p.greySurface
        drawBoard()
        p.possibleMove()
        return l
    elif BoardLayout[mouse[0]][mouse[1]][0] is 'b' and player is 2 :
        p=pieces()
        p.mov_item(BoardLayout[mouse[0]][mouse[1]])
        l=p.greySurface
        drawBoard()
        p.possibleMove()
        return l
    else:
        return l

def move_pieces(mouse_u,mouse_d):
    global temp,BoardLayout
    temp=copy.deepcopy(BoardLayout)
    swap = BoardLayout[mouse_d[0]][mouse_d[1]]
    print('Moving pieces',swap)
    BoardLayout[mouse_d[0]][mouse_d[1]]='0'
    BoardLayout[mouse_u[0]][mouse_u[1]]=swap

def undo():
    global BoardLayout,temp,player
    BoardLayout=copy.deepcopy(temp)
    if player == 1:
        player = 2
    else:
        player = 1
    drawBoard()




        
#######################MAIN
def gameLoop():
    drawBoard()
    gameExit=False
    gameover=False
    mouse_d,mouse_u = [-1,-1],[-1,-1]
    global player
    while not gameExit:
        press_flag = 0
        press_up_flag = 0
        while gameover:
            gameDisplay.fill(white)
            message_to_screen("Game Over", red, -50, "large")
            message_to_screen("Press C to play again and Q to Exit", black, 50)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameover = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameover = False
                    if event.key == pygame.K_c:
                        gameLoop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    undo()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down=pygame.mouse.get_pos()
                press_flag=1
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_up = pygame.mouse.get_pos()
                press_up_flag=1
        if press_flag is 1:
            print('Mouse Button DOwn')
            mouse_d = [int((mouse_down[1]) / 75),int((mouse_down[0]) / 75)]
            print(mouse_d)
            l = get_display(mouse_d)
        if press_up_flag is 1:
            print('MOuse Butotn UP')
            mouse_u= [int((mouse_up[1]) / 75), int((mouse_up[0]) / 75)]
            print(mouse_u)
            #Mouse up prints the coordinates when the mouse button lifts up
            print(l)
            if mouse_u in l:
                #If the entered position is in the list then move the element
                move_pieces(mouse_u,mouse_d)
                drawBoard()
                print(print_pos(mouse_u))
                print(white_check,black_check)

                if player == 1:
                    player=2
                else:
                    player = 1
            else:
                continue

        clock.tick(10)



game_intro()
gameLoop()






