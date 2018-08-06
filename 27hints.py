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
    return b                     #change string into lists of rows

def col(board,c):
    lst = []
    for row in board:
        lst.append(row[co])
    return lst                    #creating a list of collomns

def box_of((r,c)):
    return 3*(r//3) + c//3

def constrained(lst):             #obvious hints : count for numbers of different digits
    digits = set(lst)
    digits.remove(None)
    return len(digits) == 8

def constrained_cells(board):
    for row in board:
        for elt in row:
            num=len(row)+len(col)
            if num > 7:
                lst.append(row,col)
