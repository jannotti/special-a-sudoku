def digits(s):
    d=[]
    for ch in s:
      if ch.isdigit():
        d.append(int(ch))
      else:
        d.append(None)
    return d

def board_from_line(d):
    b = []
    for row in range(9):
        b.append(digits(d[row*9:(row+1)*9]))
    return b                       #change string into lists of rows

def board_row(b,r):
    return b[r]

def board_col(b,c):
    board = []
    for row in b:
        board.append(row[c])
    return board                    #creating a list of collomns

def board_box(b,box):
    r = box // 3
    a = b[r*3:(r+1)*3]
    c = box % 3
    board = []
    for row in a:
        for col in row[c*3:(c+1)*3]:
            board.append(col)
    return board



print(strategy1(board_from_line("78__9_____943_____1__4__793_1__4857_7_5_8____587__2_49___7__1___7__954_____1_732"),7))
