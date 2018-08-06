def index(request):
    context = {
        'boards' : boards,
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

def board_form_grid(b):
    board = []
    for line in b.split("\n"):
      if re.search("[0-9#_]", line):
        digits = []
        for char in line:
          if char.isdigit():
            digits.append(char)
          elif char in "#_ ":
            digits.append("")
        if len(digits) != 9:
          warn("Bad line:", line)
        lines.append(digits)     #baord into digits of integer
    if len(lines) != 9:
      warn(len(lines), "lines")

def digits(s):
  d=[]
  for ch in s:
    if ch.isdigit():
      d.append(int(ch))
    else:
      d.append(None)
  return d                       #change digits into string

def board(d):
    b = []
    for row in range(9):
        b.append(digits(s[row*9:(row+1)*9]))
    return b                     #change string into lists

def repeat_int(board):
    mylist = []
    for k in board:
        if k not in mylist:
            mylist.append(k)
        else:
            if type(k) == int:
                    return True
    return False                  #check for repitition

def row_ok (board,r):
    return not repeat_int(board)

def col(board,c):
    lst = []
    for row in board:
        lst.append(row[co])
    return lst                    #creating a list of collomn

def col_ok (board,col):
    return not repeat_int(col)

def box_ok (board,b):
    set = []
    for x in range(3*(b//3),3*(b//3)+3):
        for y in range(3*(b%3),3*(b%3)+3):
            set.append(board[x][y])
    return not repeat_int(set)    #check for every 3*3 boxes are right

def matches(pattern,lst):
    for i in range(len(pattern)):
        if pattern[i] != None and pattern[i] != lst[i]:
            return False
    return True                   #check for solution whether is right

print(matches([1,2,None,3],[1,2,3,4]))
