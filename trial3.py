import pygame, time, chess, random, threading, copy
from collections import Counter  # For counting elements in a list effieciently.

pygame.init()
pygame.font.init()
display_width, display_height, piece_size = 600, 600, 75
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Chess Game')
whitepieces = [pygame.image.load('Chess_image/Chess_tile_rl.png'), pygame.image.load('Chess_image/Chess_tile_nl.png'),
               pygame.image.load('Chess_image/Chess_tile_bl.png'), pygame.image.load('Chess_image/Chess_tile_ql.png'),
               pygame.image.load('Chess_image/Chess_tile_kl.png'), pygame.image.load('Chess_image/Chess_tile_pl.png')]
blackpieces = [pygame.image.load('Chess_image/Chess_tile_rd.png'), pygame.image.load('Chess_image/Chess_tile_nd.png'),
               pygame.image.load('Chess_image/Chess_tile_bd.png'), pygame.image.load('Chess_image/Chess_tile_qd.png'),
               pygame.image.load('Chess_image/Chess_tile_kd.png'), pygame.image.load('Chess_image/Chess_tile_pd.png')]
# Initialize the board:
BoardLayout = [['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'],  # 8
               ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],  # 7
               [0, 0, 0, 0, 0, 0, 0, 0],  # 6
               [0, 0, 0, 0, 0, 0, 0, 0],  # 5
               [0, 0, 0, 0, 0, 0, 0, 0],  # 4
               [0, 0, 0, 0, 0, 0, 0, 0],  # 3
               ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw'],  # 2
               ['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw']]  # 1
# a      b     c     d     e     f     g     h
BL = [['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'],  # 8
      ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],  # 7
      [0, 0, 0, 0, 0, 0, 0, 0],  # 6
      [0, 0, 0, 0, 0, 0, 0, 0],  # 5
      [0, 0, 0, 0, 0, 0, 0, 0],  # 4
      [0, 0, 0, 0, 0, 0, 0, 0],  # 3
      ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw'],  # 2
      ['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw']]  # 1
# a      b     c     d     e     f     g     h

# Store the piece square tables here so they can be accessed globally by pieceSquareTable() function:
pawn_table = [0, 0, 0, 0, 0, 0, 0, 0,
              50, 50, 50, 50, 50, 50, 50, 50,
              10, 10, 20, 30, 30, 20, 10, 10,
              5, 5, 10, 25, 25, 10, 5, 5,
              0, 0, 0, 20, 20, 0, 0, 0,
              5, -5, -10, 0, 0, -10, -5, 5,
              5, 10, 10, -20, -20, 10, 10, 5,
              0, 0, 0, 0, 0, 0, 0, 0]
knight_table = [-50, -40, -30, -30, -30, -30, -40, -50,
                -40, -20, 0, 0, 0, 0, -20, -40,
                -30, 0, 10, 15, 15, 10, 0, -30,
                -30, 5, 15, 20, 20, 15, 5, -30,
                -30, 0, 15, 20, 20, 15, 0, -30,
                -30, 5, 10, 15, 15, 10, 5, -30,
                -40, -20, 0, 5, 5, 0, -20, -40,
                -50, -90, -30, -30, -30, -30, -90, -50]
bishop_table = [-20, -10, -10, -10, -10, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 5, 5, 10, 10, 5, 5, -10,
                -10, 0, 10, 10, 10, 10, 0, -10,
                -10, 10, 10, 10, 10, 10, 10, -10,
                -10, 5, 0, 0, 0, 0, 5, -10,
                -20, -10, -90, -10, -10, -90, -10, -20]
rook_table = [0, 0, 0, 0, 0, 0, 0, 0,
              5, 10, 10, 10, 10, 10, 10, 5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              -5, 0, 0, 0, 0, 0, 0, -5,
              0, 0, 0, 5, 5, 0, 0, 0]
queen_table = [-20, -10, -10, -5, -5, -10, -10, -20,
               -10, 0, 0, 0, 0, 0, 0, -10,
               -10, 0, 5, 5, 5, 5, 0, -10,
               -5, 0, 5, 5, 5, 5, 0, -5,
               0, 0, 5, 5, 5, 5, 0, -5,
               -10, 5, 5, 5, 5, 5, 0, -10,
               -10, 0, 5, 0, 0, 0, 0, -10,
               -20, -10, -10, 70, -5, -10, -10, -20]
king_table = [-30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -30, -40, -40, -50, -50, -40, -40, -30,
              -20, -30, -30, -40, -40, -30, -30, -20,
              -10, -20, -20, -20, -20, -20, -20, -10,
              20, 20, 0, 0, 0, 0, 20, 20,
              20, 30, 10, 0, 0, 10, 30, 20]
king_endgame_table = [-50, -40, -30, -20, -20, -30, -40, -50,
                      -30, -20, -10, 0, 0, -10, -20, -30,
                      -30, -10, 20, 30, 30, 20, -10, -30,
                      -30, -10, 30, 40, 40, 30, -10, -30,
                      -30, -10, 30, 40, 40, 30, -10, -30,
                      -30, -10, 20, 30, 30, 20, -10, -30,
                      -30, -30, 0, 0, 0, 0, -30, -30,
                      -50, -30, -30, -30, -30, -30, -30, -50]

chessBoard = pygame.image.load('Chess_image/chess_board.png')
white, black, grey, red = (255, 255, 255), (0, 0, 0), (83, 83, 83, 50), (255, 0, 0)
Exit = False
clock = pygame.time.Clock()
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)
board = chess.Board()


class num_moves:
    i = 0

    def incr(self):
        self.i += 1

    def disp(self):
        print("num of moves : ", self.i)

    def geti(self):
        return self.i


def drawBoard():
    global board
    gameDisplay.blit(chessBoard, (0, 0))
    for i in range(0, 8):
        for j in range(0, 8):
            if chess.Board.piece_at(board, square=(i * 8) + j) is not None:
                if chess.Board.piece_at(board, square=(i * 8) + j).color is chess.WHITE:
                    if chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.PAWN:
                        gameDisplay.blit(whitepieces[5], ((7 - j) * piece_size, i * piece_size))
                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.ROOK:
                        gameDisplay.blit(whitepieces[0], ((7 - j) * piece_size, i * piece_size))
                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.KNIGHT:
                        gameDisplay.blit(whitepieces[1], ((7 - j) * piece_size, i * piece_size))
                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.BISHOP:
                        gameDisplay.blit(whitepieces[2], ((7 - j) * piece_size, i * piece_size))
                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.QUEEN:
                        gameDisplay.blit(whitepieces[3], ((7 - j) * piece_size, i * piece_size))
                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.KING:
                        gameDisplay.blit(whitepieces[4], ((7 - j) * piece_size, i * piece_size))

                if chess.Board.piece_at(board, square=(i * 8) + j).color is chess.BLACK:

                    if chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.PAWN:

                        gameDisplay.blit(blackpieces[5], ((7 - j) * piece_size, i * piece_size))

                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.ROOK:

                        gameDisplay.blit(blackpieces[0], ((7 - j) * piece_size, i * piece_size))

                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.KNIGHT:

                        gameDisplay.blit(blackpieces[1], ((7 - j) * piece_size, i * piece_size))

                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.BISHOP:

                        gameDisplay.blit(blackpieces[2], ((7 - j) * piece_size, i * piece_size))

                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.QUEEN:

                        gameDisplay.blit(blackpieces[3], ((7 - j) * piece_size, i * piece_size))

                    elif chess.Board.piece_at(board, square=(i * 8) + j).piece_type == chess.KING:

                        gameDisplay.blit(blackpieces[4], ((7 - j) * piece_size, i * piece_size))

    pygame.display.update()

    pygame.display.update()


# Function to Print the Value of the current positon Eg. a5,e6 etc
def print_pos(mouse_pointer):
    mouse_pointer[0] = chr(104 - mouse_pointer[0])
    mouse_pointer[1] += 1
    pointer = str(mouse_pointer[0]) + str(mouse_pointer[1])
    return pointer


def text_objects(text, color, size):
    if size == 'small':
        textSurface = smallfont.render(text, True, color)
    elif size == 'medium':
        textSurface = medfont.render(text, True, color)
    elif size == 'large':
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurface, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurface, textRect)


def game_intro():
    intro = True

    while intro:
        gameDisplay.fill(white)
        message_to_screen("Chess", black, -40, "large")
        message_to_screen("Press q to Quit", red, 40)
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


def game_ex(b):
    ex = True

    while ex:
        gameDisplay.fill(white)
        message_to_screen("Game Over", black, -40, "large")
        message_to_screen("Player Won", red, 40)
        if b:
            player='White'
        else:
            player='Black'
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


def undo():
    global board
    board.pop()


def possible_moves(pos):
    l = list(board.legal_moves);
    li = []
    for i in range(0, 8):
        for j in range(0, 8):
            p = print_pos([i, j])
            s = pos + p
            if chess.Move.from_uci(s) in board.legal_moves:
                li.append(p)
    return li, s


def display_possible_moves(pos):
    lis, notuse = possible_moves(pos)
    print(lis)
    drawBoard()
    # piece_size=75
    for i in lis:
        # gameDisplay.blit(grey_image, ((104-ord(i[0])) * piece_size, (ord(i[1])-49) * piece_size))
        s = pygame.Surface((piece_size, piece_size), pygame.SRCALPHA)
        s.fill((93, 93, 93, 128))
        gameDisplay.blit(s, [((104 - ord(i[0])) * piece_size), (ord(i[1]) - 49) * piece_size])
        pygame.display.update()
    pygame.display.update()
    return lis, notuse


############################################################################################################################################################################################################################
def ai(played_moves):
    global board
    global board1
    choice = 'negamax'
    if choice == 'random':
        global board
        moves = list(board.legal_moves)
        if len(moves) != 0:
            mov = random.choice(moves)
            board.push(mov)
        else:
            game_ex(board.turn)
    # checkmate game end diplay bit game END!!

    elif choice == 'negamax':
        bestMoveReturn = []
        moves = getPossibleMoves()
        Value = negamax(random.choice(moves), 2, -1000000, 1000000, -1, bestMoveReturn, played_moves)
        if len(Value) != 0:

            board1 = board
            BL = copy.deepcopy(BoardLayout)

            print("Value = ", str(Value))
            Value[0] = abs(Value[0] - 7)
            Value[1] = abs(Value[1] - 7)
            ##        pushing=get_str(Value)
            ##        print(pushing)
            pushing = abs((Value[0] - 7) * 8) + Value[1]

            for obj in list(board.legal_moves):
                if pushing == (obj.to_square):
                    break
            print("\tMOVE : ")
            print(obj)
            board.push(obj)
        ##        board1.push(obj)

        return

    elif choice == 'alpha':
        boardvalue = init_evaluate_board()

        mov = selectmove(5)
        print(mov)

    # elif choice == 'xxx':


##        score=evaluate(played_moves)
##
##        mx = score.max()
##        idx = score.index(mx)
##        pcs = allMoves[idx]
##        board.push(pcs)


##############################################################################################################def init_evaluate_board():
##############################################################################################################    global boardvalue
##############################################################################################################
##############################################################################################################    wp = len(board.pieces(chess.PAWN, chess.WHITE))
##############################################################################################################    bp = len(board.pieces(chess.PAWN, chess.BLACK))
##############################################################################################################    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
##############################################################################################################    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
##############################################################################################################    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
##############################################################################################################    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
##############################################################################################################    wr = len(board.pieces(chess.ROOK, chess.WHITE))
##############################################################################################################    br = len(board.pieces(chess.ROOK, chess.BLACK))
##############################################################################################################    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
##############################################################################################################    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
##############################################################################################################
##############################################################################################################    material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)
##############################################################################################################
##############################################################################################################    pawnsq = sum([pawn_table[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
##############################################################################################################    pawnsq= pawnsq + sum([-pawn_table[chess.square_mirror(i)]
##############################################################################################################                                    for i in board.pieces(chess.PAWN, chess.BLACK)])
##############################################################################################################    knightsq = sum([knight_table[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
##############################################################################################################    knightsq = knightsq + sum([-knight_table[chess.square_mirror(i)]
##############################################################################################################                                    for i in board.pieces(chess.KNIGHT, chess.BLACK)])
##############################################################################################################    bishopsq= sum([bishop_table[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
##############################################################################################################    bishopsq= bishopsq + sum([-bishop_table[chess.square_mirror(i)]
##############################################################################################################                                    for i in board.pieces(chess.BISHOP, chess.BLACK)])
##############################################################################################################    rooksq = sum([rook_table[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
##############################################################################################################    rooksq = rooksq + sum([-rook_table[chess.square_mirror(i)]
##############################################################################################################                                    for i in board.pieces(chess.ROOK, chess.BLACK)])
##############################################################################################################    queensq = sum([queen_table[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
##############################################################################################################    queensq = queensq + sum([-queen_table[chess.square_mirror(i)]
##############################################################################################################                                    for i in board.pieces(chess.QUEEN, chess.BLACK)])
##############################################################################################################    kingsq = sum([king_table[i] for i in board.pieces(chess.KING, chess.WHITE)])
##############################################################################################################    kingsq = kingsq + sum([-king_table[chess.square_mirror(i)]
##############################################################################################################                                    for i in board.pieces(chess.KING, chess.BLACK)])
##############################################################################################################
##############################################################################################################    boardvalue = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
##############################################################################################################
##############################################################################################################    return boardvalue
##############################################################################################################
##############################################################################################################def evaluate_board():
##############################################################################################################
##############################################################################################################    if board.is_checkmate():
##############################################################################################################        if board.turn:
##############################################################################################################            return -9999
##############################################################################################################        else:
##############################################################################################################            return 9999
##############################################################################################################    if board.is_stalemate():
##############################################################################################################        return 0
##############################################################################################################    if board.is_insufficient_material():
##############################################################################################################        return 0
##############################################################################################################
##############################################################################################################    eval = boardvalue
##############################################################################################################    if board.turn:
##############################################################################################################        return eval
##############################################################################################################    else:
##############################################################################################################        return -eval
##############################################################################################################
##############################################################################################################def quiesce( alpha, beta ):
##############################################################################################################    stand_pat = evaluate_board()
##############################################################################################################    if( stand_pat >= beta ):
##############################################################################################################        return beta
##############################################################################################################    if( alpha < stand_pat ):
##############################################################################################################        alpha = stand_pat
##############################################################################################################
##############################################################################################################    for move in board.legal_moves:
##############################################################################################################        if board.is_capture(move):
##############################################################################################################            make_move(move)
##############################################################################################################            score = -quiesce( -beta, -alpha )
##############################################################################################################            unmake_move()
##############################################################################################################
##############################################################################################################            if( score >= beta ):
##############################################################################################################                return beta
##############################################################################################################            if( score > alpha ):
##############################################################################################################                alpha = score
##############################################################################################################    return alpha
##############################################################################################################
##############################################################################################################def alphabeta( alpha, beta, depthleft ):
##############################################################################################################    bestscore = -9999
##############################################################################################################    if( depthleft == 0 ):
##############################################################################################################        return quiesce( alpha, beta )
##############################################################################################################    for move in board.legal_moves:
##############################################################################################################        make_move(move)
##############################################################################################################        score = -alphabeta( -beta, -alpha, depthleft - 1 )
##############################################################################################################        unmake_move()
##############################################################################################################        if( score >= beta ):
##############################################################################################################            return score
##############################################################################################################        if( score > bestscore ):
##############################################################################################################            bestscore = score
##############################################################################################################        if( score > alpha ):
##############################################################################################################            alpha = score
##############################################################################################################    return bestscore
##############################################################################################################
##############################################################################################################def selectmove(depth):
##############################################################################################################
##############################################################################################################    bestMove = chess.Move.null()
##############################################################################################################    bestValue = -99999
##############################################################################################################    alpha = -100000
##############################################################################################################    beta = 100000
##############################################################################################################    for move in board.legal_moves:
##############################################################################################################        make_move(move)
##############################################################################################################        boardValue = -alphabeta(-beta, -alpha, depth-1)
##############################################################################################################        if boardValue > bestValue:
##############################################################################################################            bestValue = boardValue;
##############################################################################################################            bestMove = move
##############################################################################################################        if( boardValue > alpha ):
##############################################################################################################            alpha = boardValue
##############################################################################################################        unmake_move()
##############################################################################################################    movehistory.append(bestMove)
##############################################################################################################    return bestMove
##############################################################################################################
##############################################################################################################
##############################################################################################################def make_move(mov):
##############################################################################################################    update_eval(mov, board.turn)
##############################################################################################################    board.push(mov)
##############################################################################################################
##############################################################################################################    return mov
##############################################################################################################
##############################################################################################################def unmake_move():
##############################################################################################################    mov = board.pop()
##############################################################################################################    update_eval(mov, not board.turn)
##############################################################################################################
##############################################################################################################    return mov
##############################################################################################################


def get_str(info):
    ypos = info[1]
    if ypos == 0:
        y = 'a'
    if ypos == 1:
        y = 'b'
    if ypos == 2:
        y = 'c'
    if ypos == 3:
        y = 'd'
    if ypos == 4:
        y = 'e'
    if ypos == 5:
        y = 'f'
    if ypos == 6:
        y = 'g'
    if ypos == 7:
        y = 'h'
    return y + str(abs(info[0] - 7))


def getPossibleMoves():
    xpos, ypos = 0, 0
    ##    global board1
    possible = []
    for steps in board.legal_moves:
        ypos = int(steps.to_square % 8)
        if int(steps.to_square) < 8 and int(steps.to_square) > -1:
            xpos = 7
        elif int(steps.to_square) < 16 and int(steps.to_square) > 7:
            xpos = 6
        elif int(steps.to_square) < 24 and int(steps.to_square) > 15:
            xpos = 5
        elif int(steps.to_square) < 32 and int(steps.to_square) > 23:
            xpos = 4
        elif int(steps.to_square) < 40 and int(steps.to_square) > 31:
            xpos = 3
        elif int(steps.to_square) < 48 and int(steps.to_square) > 39:
            xpos = 2
        elif int(steps.to_square) < 56 and int(steps.to_square) > 47:
            xpos = 1
        elif int(steps.to_square) < 64 and int(steps.to_square) > 55:
            xpos = 0
        possible.append([xpos, ypos])
    return possible


###########################////////AI RELATED FUNCTIONS\\\\\\\\\\############################
def move_pos(newpos, move):
    global BL
    global board1
    ypos = move[1]
    val = abs((move[0] - 7) * 8) + ypos

    swap = BL[int(move[0])][int(move[1])]
    # This is for swapping the pieces for movement
    BL[int(move[0])][int(move[1])] = '0'
    BL[int(move[0])][int(move[1])] = swap


##    for items in list(board1.legal_moves):
##        if val == items.to_square:
##            break
##    board1.push(items)
##
##    x = random.choice(list(board1.legal_moves))
##    board1.push(x)

##    for pcs in board.legal_moves:
##        if pcs.to_square == val:
# board.push_san(pcs.uci()[2:])
# chess.Board.piece_at(board, val)

def rev_board():
    global BL
    for i in range(3):
        row = BL[i]
        swap = BL[7 - i]
        BL[i] = swap
        BL[7 - i] = row


def negamax(move, depth, alpha, beta, colorsign, bestMoveReturn, played_moves, root=True):
    global BL
    # Access global variable that will store scores of positions already evaluated:
    ##    global searched
    # If the depth is zero, we are at a leaf node (no more depth to be analysed):
    if depth == 0:
        return colorsign * evaluate(played_moves)
    # Generate all the moves that can be played:
    moves = getPossibleMoves()
    # If there are no moves to be played, just evaluate the position and return it:
    if moves == []:
        return colorsign * evaluate(played_moves)
    # Initialize a best move for the root node:
    if root:
        bestMove = random.choice(moves)
    # Initialize the best move's value:
    bestValue = -100000
    # Go through each move:
    for move in moves:
        # Make a clone of the current move and perform the move on it:
        # newpos = position.clone()
        # makemove(newpos,move[0][0],move[0][1],move[1][0],move[1][1])
        # Generate the key for the new resulting position:
        # key = pos2key(newpos)
        # If this position was already searched before, retrieve its node value.
        # Otherwise, calculate its node value and store it in the dictionary:
        ##        if key in searched:
        ##            value = searched[key]
        ##        else:
        newpos = BL
        move_pos(newpos, move)
        # print(BL)
        value = -negamax(newpos, depth - 1, -beta, -alpha, colorsign, [], played_moves, False)
        # searched[key] = value
        # If this move is better than the best so far:
        if value > bestValue:
            # Store it
            bestValue = value
            # If we're at root node, store the move as the best move:
            if root:
                bestMove = move
        # Update the lower bound for this node:5
        alpha = max(alpha, value)
        if alpha >= beta:
            # If our lower bound is higher than the upper bound for this node, there
            # is no need to look at further moves:
            break
    # If this is the root node, return the best move:
    if root:
        # searched = {}
        bestMoveReturn[:] = bestMove
        return bestMoveReturn
    # Otherwise, return the bestValue (i.e. value for this node.)
    return bestValue
chess.Board.is
def evaluate(played_moves):
    global BL
    if board.is_checkmate():
        if board.turn == False:
            # Major advantage to black
            return -20000
        if board.turn == True:
            # Major advantage to white
            return 20000
    # Get the board:
    # board = position.getboard()
    Board = BL
    # Flatten the board to a 1D array for faster calculations:
    flatboard = [x for row in Board for x in row]
    # Create a counter object to count number of each pieces:
    c = Counter(flatboard)
    Qw = c['Qw']
    Qb = c['Qb']
    Rw = c['Rw']
    Rb = c['Rb']
    Bw = c['Bw']
    Bb = c['Bb']
    Nw = c['Nw']
    Nb = c['Nb']
    Pw = c['Pw']
    Pb = c['Pb']
    # Note: The above choices to flatten the board and to use a library
    # to count pieces were attempts at making the AI more efficient.
    # Perhaps using a 1D board throughout the entire program is one way
    # to make the code more efficient.
    # Calculate amount of material on both sides and the number of moves
    # played so far in order to determine game phase:
    whiteMaterial = 9 * Qw + 5 * Rw + 3 * Nw + 3 * Bw + 1 * Pw
    blackMaterial = 9 * Qb + 5 * Rb + 3 * Nb + 3 * Bb + 1 * Pb
    numofmoves = played_moves.geti()
    gamephase = 'opening'
    if numofmoves > 40 or (whiteMaterial < 14 and blackMaterial < 14):
        gamephase = 'ending'
    # A note again: Determining game phase is again one the attempts
    # to make the AI smarter when analysing boards and has not been
    # implemented to its full potential.
    # Calculate number of doubled, blocked, and isolated pawns for
    # both sides:
    Dw = doubledPawns('white')
    Db = doubledPawns('black')
    Sw = blockedPawns('white')
    Sb = blockedPawns('black')
    Iw = isolatedPawns('white')
    Ib = isolatedPawns('black')
    # Evaluate position based on above data:
    evaluation1 = 900 * (Qw - Qb) + 500 * (Rw - Rb) + 330 * (Bw - Bb) + 320 * (Nw - Nb) + 100 * (Pw - Pb) + -30 * (
                Dw - Db + Sw - Sb + Iw - Ib)
    # Evaluate position based on piece square tables:
    evaluation2 = pieceSquareTable(flatboard, gamephase)
    # Sum the evaluations:
    evaluation = evaluation1 + evaluation2
    # Return it:
    print("evaluation: " + str(evaluation))
    return evaluation


def pieceSquareTable(flatboard, gamephase):
    # Initialize score:
    score = 0
    # Go through each square:
    for i in range(64):
        if flatboard[i] == 0:
            # Empty square
            continue
        # Get data:
        else:
            flat = flatboard[i]
            piece = flat[0]
        ##            print(flat)
        ##            if len(flat)!=0:
        ##                color = flat[1]
        color = 'w'
        sign = +1
        # Adjust index if black piece, since piece sqaure tables
        # were designed for white:
        if color == 'b':
            i = int((7 - i / 8) * 8 + i % 8)
            sign = -1
        # Adjust score:
        if piece == 'P':
            score += sign * pawn_table[i]
        elif piece == 'N':
            score += sign * knight_table[i]
        elif piece == 'B':
            score += sign * bishop_table[i]
        elif piece == 'R':
            score += sign * rook_table[i]
        elif piece == 'Q':
            score += sign * queen_table[i]
        elif piece == 'K':
            # King has different table values based on phase
            # of the game:
            if gamephase == 'opening':
                score += sign * king_table[i]
            else:
                score += sign * king_endgame_table[i]
    print("piece sqaure table = ", str(score))
    return score


def doubledPawns(color):
    global BoardLayout
    color = color[0]
    # Get indices of pawns:
    listofpawns = lookfor('P' + color)
    # Count the number of doubled pawns by counting occurences of
    # repeats in their x-coordinates:
    repeats = 0
    temp = []
    for pawnpos in listofpawns:
        if pawnpos[0] in temp:
            repeats = repeats + 1
        else:
            temp.append(pawnpos[0])
    return repeats


def blockedPawns(color):
    global BoradLayout
    color = color[0]
    listofpawns = lookfor('P' + color)
    blocked = 0
    # Self explanatory:
    for pawnpos in listofpawns:
        if ((color == 'w' and isOccupiedby(pawnpos[0], pawnpos[1] - 1,
                                           'black'))
                or (color == 'b' and isOccupiedby(pawnpos[0], pawnpos[1] + 1,
                                                  'white'))):
            blocked = blocked + 1
    return blocked


def isolatedPawns(color):
    global BoradLayout
    color = color[0]
    listofpawns = lookfor('P' + color)
    # Get x coordinates of all the pawns:
    xlist = [x for (x, y) in listofpawns]
    isolated = 0
    for x in xlist:
        if x != 0 and x != 7:
            # For non-edge cases:
            if x - 1 not in xlist and x + 1 not in xlist:
                isolated += 1
        elif x == 0 and 1 not in xlist:
            # Left edge:
            isolated += 1
        elif x == 7 and 6 not in xlist:
            # Right edge:
            isolated += 1
    return isolated


def isOccupiedby(x, y, color):
    global BL
    x, y = int(x), int(y)
    print(BL[y][x])
    if BL[y][x] == 0:
        # the square has nothing on it.
        return False
    else:  # if BL[y][x][1] == color[0]:
        # The square has a piece of the color inputted.
        return True
    # The square has a piece of the opposite color.
    return False


def lookfor(piece):
    listofLocations = []
    for row in range(8):
        for col in range(8):
            if BoardLayout[row][col] == piece:
                x = col
                y = row
                listofLocations.append((x, y))
    return listofLocations


def pos2key(position):
    # Get board:
    board = BoardLayout
    # Convert the board into a tuple so it is hashable:
    boardTuple = []
    for row in board:
        boardTuple.append(tuple(row))
    boardTuple = tuple(boardTuple)
    # Get castling rights:
    rights = [False] * 2
    # Convert to a tuple:
    tuplerights = (tuple(rights[0]), tuple(rights[1]))
    # Generate the key, which is a tuple that also takes into account the side to play:
    key = (boardTuple, position.getplayer(),
           tuplerights)
    # Return the key:
    return key


###########################\\\\\\\\\\AI RELATED FUNCTIONS////////############################
#######################MAIN
def move_piece(mouse_u, mouse_d):
    global BoardLayout
    global BL
    swap = BoardLayout[int(mouse_d[0])][int(mouse_d[1])]
    # This is for swapping the pieces for movement
    BoardLayout[int(mouse_d[0])][int(mouse_d[1])] = '0'
    BoardLayout[int(mouse_u[0])][int(mouse_u[1])] = swap
    print("Board = ")
    for x in BoardLayout:
        print(x)

    swap = BL[int(mouse_d[0])][int(mouse_d[1])]
    # This is for swapping the pieces for movement
    BL[int(mouse_d[0])][int(mouse_d[1])] = '0'
    BL[int(mouse_u[0])][int(mouse_u[1])] = swap

    # swap = BL1[int(mouse_d[0])][int(mouse_d[1])]
    # # This is for swapping the pieces for movement
    # BL1[int(mouse_d[0])][int(mouse_d[1])] = '0'
    # BL1[int(mouse_u[0])][int(mouse_u[1])] = swap


def gameLoop(played_moves):
    drawBoard()
    global board
    gameExit = False
    gameover = False
    mouse_d, mouse_u = [-1, -1], [-1, -1]
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
                        gameLoop(played_moves)
        if board.turn is chess.WHITE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        undo()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down = pygame.mouse.get_pos()
                    md = [int((mouse_down[1]) / 75), int((mouse_down[0]) / 75)]
                    press_flag = 1
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_up = pygame.mouse.get_pos()
                    mu = [int((mouse_up[1]) / 75), int((mouse_up[0]) / 75)]
                    press_up_flag = 1
            if press_flag is 1:
                print('Mouse Button DOwn')
                mouse_d = print_pos([int((mouse_down[0]) / 75), int((mouse_down[1]) / 75)])
                print(mouse_d)
                l, k = display_possible_moves(mouse_d)
            if press_up_flag is 1:
                print('MOuse Butotn UP')
                mouse_u = print_pos([int((mouse_up[0]) / 75), int((mouse_up[1]) / 75)])
                print(mouse_u)

                if mouse_u in l and chess.Move.from_uci(mouse_d + mouse_u) in board.legal_moves:
                    board.push(chess.Move.from_uci(mouse_d + mouse_u))
                    move_piece(mu, md)
                    drawBoard()
                    print(board)
        else:
            ai(played_moves)
            drawBoard()
            played_moves.incr()
            played_moves.disp()
        clock.tick(10)


def main():
    game_intro()
    played_moves = num_moves()
    gameLoop(played_moves)


main()






