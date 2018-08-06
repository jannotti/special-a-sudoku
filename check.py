def digits(s):
  d=[]
  for ch in s:
    if ch.isdigit():
      d.append(int(ch))
    else:
      d.append(None)
  return d

def board(d):
  for row in range(9):
    a = d[row*9:(row+1)*9]
    b.append(string_int(a))
  return b

def row_ok (digits,r):
    for row in range(9):
        mylist = []
        for k in b:
            if k not in mylist:
                mylist.append(k)
            else:
                if type(k) == int:
                    return True
        return False

def box_ok (board,b):
    myset = []
    lst = []
    for row in range(4):
        for row in board:
            a = d[row*3:(row+1)*3]
            b.append(row_int(a))
    for row in board:
        lst.append(row[co])
    return not repeat_int(lst)
    for col in range(4):
        for col in lst:
            c = d[col*3:(col+1)*3]
            d.append(col_int(c))
    return not repeat_int(bc)

print(row_ok(["12345_"],1))
print(row_ok([[1,2,None,2],[1,2,3,4],[1,2,2,3]],3))
