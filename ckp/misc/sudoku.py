class SudokuBoard:
    """ For solving 9x9 sudoku puzzles. """

    ROWS = [[(i, j) for j in range(9)] for i in range(9)]
    COLS = [[(i, j) for i in range(9)] for j in range(9)]
    CELLS = [[(3*(i//3)+j//3, 3*(i%3)+(j%3)) for j in range(9)] for i in range(9)]
    BIT_MAP = {1: 1, 2: 2, 4: 3, 8: 4, 16: 5, 32: 6, 64: 7, 128: 8, 256: 9}
    
    __slots__ = ('candi',)
    def __init__(self, candi: list[list[int]]):
        self.candi = candi

    def __str__(self): return "SudokuBoard([\n{}\n])".format("\n".join("\t[{}],".format(", ".join(f"{x:09b}"[::-1] for x in row)) for row in self.candi))

    def copy(self): return SudokuBoard([row[:] for row in self.candi])
    
    def step_groups(self, groups) -> tuple[bool, bool]:
        candi = self.candi
        changed = False
        
        for group in groups:
            allow_mask = 511
            singles = 511
            single_appeared = 0

            for (i, j) in group:
                v = candi[i][j]
                if v.bit_count() == 1:
                    if not allow_mask & v: return changed, True
                    allow_mask &= ~v
                singles &= ~(single_appeared & v)
                single_appeared |= v
                
            singles &= single_appeared
            
            for (i, j) in group:
                pv = candi[i][j]
                if pv.bit_count() <= 1: continue
                v = pv & allow_mask
                if not v: return changed, True
                w = v & singles
                if w:
                    if w.bit_count() > 1: return changed, True
                    v = w
                if v != pv: changed = True
                candi[i][j] = v
    
        return changed, False
    
    def step(self) -> tuple[bool, bool]:
        changed = False
        err = False

        for groups in (self.ROWS, self.COLS, self.CELLS):
            inner_changed, err = self.step_groups(groups)
            changed = changed or inner_changed

            if err: break

        return changed, err

    def update(self) -> bool:
        while True:
            updated, err = self.step()
            if err: return False
            if not updated: return True

    def get_next_boards(self):
        candi = self.candi
        
        for i in range(9):
            row = candi[i]
            for j in range(9):
                x = row[j]
                match x.bit_count():
                    case 0: return []
                    case 1: continue
                    case _:
                        next_boards = []
                        k_mask = 256
                        while k_mask:
                            if (x & k_mask):
                                next_boards.append(next_board := self.copy())
                                next_board.candi[i][j] = k_mask
                            k_mask //= 2
                        return next_boards
        
        return [self]
    
    def to_array(self):
        return [[self.BIT_MAP.get(c) or 0 for c in row] for row in self.candi]

    @staticmethod
    def from_array(A: list[list[int]]):
        return SudokuBoard([[((1<<(x-1)) if x else 511)for x in row] for row in A])

    @staticmethod
    def solve(board):
        stack = [board]
        while stack:
            board = stack.pop()
            if not board.update(): continue

            next_boards = board.get_next_boards()
            if len(next_boards) == 1: return board

            stack.extend(next_boards)