class Bitmap(object):
    def __init__(self, board):
        self.board = board

    def check_winner(self):
        int_red, int_yellow = self.shape(self.board, 1)
        red_win, yellow_win = self.connected_four(int_red), self.connected_four(int_yellow)

        if red_win[0]: return [1, red_win[1]]
        elif yellow_win[0]: return [-1, yellow_win[1]]
        else: return [0]

    def shape(self, board, player):
        opponent = -1 if player == 1 else 1
        board = [[int(float(x)) for x in y] for y in [board[z:z+7] for z in range(0, len(board), 7)]]
        pos, mask, int_r, int_m = self.get_bitmap(board, player)
        opp_bit = int_r ^ int_m
        opp_bin = '{0:0{1}b}'.format(opp_bit,len(pos))
        int_y = int(opp_bin, 2)
        return int_r,int_y

    def get_bitmap(self, board, player):
        position, mask = '', ''
        for j in range(6, -1, -1):
            mask += '0'
            position += '0'
            for i in range(0, 6):
                mask += ['0', '1'][board[i][j] != 0]
                position += ['0', '1'][board[i][j] == player]

        return position, mask, int(position, 2), int(mask, 2)

    def connected_four(self, position):
        # --
        m = position & (position >> 7)
        if m & (m >> 14):
            return True, '--'
        # \
        m = position & (position >> 6)
        if m & (m >> 12):
            return True, '\\'
        # /
        m = position & (position >> 8)
        if m & (m >> 16):
            return True, '/'
        # |
        m = position & (position >> 1)
        if m & (m >> 2):
            return True, '|'

        return [False]
