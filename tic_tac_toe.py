


class tic_tac_toe(object):

    def __init__(self, size = 3):
        self.size = size
        self.players = 2
        self.board = [[' ']*self.size for i in range(self.size)]
        self.left_steps = self.size ** 2
        print("Please input the two players' name below")
        self.player_A = 'A' #raw_input("First player's name: ")
        self.player_B = 'B' # raw_input("Second player's name: ")
        self.player_symbol_map = {self.player_A: 'o', self.player_B: 'x'}
        rule = """
                Starting from the first player, input the next move position 
                in the format of row column, e.g. 3 2 means the third row and
                the second column. 
                
                Row and column number is integer between one to three. 

                Press Enter for the next move.
        """
        print(rule)
        self.draw_board()


    def check_input(self, move):
        row, col = move
        if row in range(self.size) and col in range(self.size) and self.board[row][col] == ' ':
            return True
        else:
            return False 

    def ask_for_input(self, player):
        while True:
            move = raw_input("\nFor %s move (represented with %s): " % (player, self.player_symbol_map[player]))
            try:
                row, col = move.strip().split()
                row, col = int(row)-1, int(col)-1
                move = (row, col)
            except:
                raise 
            if self.check_input(move):
                break
            else:
                print("Please input valid move.")        
        self.board[row][col] = self.player_symbol_map.get(player)
        return move


    def draw_board(self):
        row_heading = '  1   2   3  '        
        row_board = ('+{0}'*(self.size)).format('---') + '+'
        print(row_heading)
        for row in range(self.size):
            print(row_board)
            row_display = '|'
            for col in range(self.size):
                row_display += ' {0} |'.format(self.board[row][col])
            print(row_display + ' {0} '.format(row))
        print(row_board)


    def judge(self, player, move):
        row, col = move
        self.left_steps -= 1
        if len(set(self.board[row])) == 1 \
            or len(set(line[col] for line in self.board)) == 1 \
            or (row == col and len(set(self.board[i][i] for i in range(self.size))) == 1) \
            or ((row + col) == (self.size - 1) and len(set(self.board[i][self.size-1-i] for i in range(self.size))) == 1):
            return 'Win'
        elif self.left_steps == 0:
            return 'Draw'
        else:
            return 'No result'


    def run_game(self):
        while True:            
            for player in (self.player_A, self.player_B):
                move = self.ask_for_input(player)
                self.draw_board()
                result = self.judge(player, move)          
                if result == 'Draw':
                    print("Draw! No winner.")
                    return
                elif result == 'Win':
                    print("Player %s wins!" % player)
                    return
                else:
                    continue



if __name__ == '__main__':
    game = tic_tac_toe(4)
    game.run_game()


# '''
#   1   2   3  
# +---+---+---+
# | o | o | x | 1
# +---+---+---+
# | o | o | x | 2
# +---+---+---+
# | o | o | x | 3
# +---+---+---+
# '''