#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 17:44:53 2018

@author: yolandazeng
"""

#Three obvious funtions
#merge row, col, and box to one list, and check the number of elements in the list 

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 16:41:30 2018

@author: yolandazeng
"""

def string_int(s):
    l = []
    for char in s:
        if char.isdigit():
            l.append(int(char))
        else:
            l.append(None)
    return l


def board_row(s):
    b_row = []
    for row in range(9):
        r = s[row*9:(row+1)*9]
        b_row.append(string_int(r))
    return b_row      
#separate the long list into 9 lists(representing rows) within a big list

def repeat_int(lst):
    for x in lst:
        lst1 = lst[::]
        lst1.remove(x)
        if type(x) == int and x in lst1:
            return True
    return False

#make the board into board list
 
def row_ok(board,r):  
    b_row = board_row(s)
    return repeat_int(b_row[r])


def board_col(s):
    b_col = []
    b_col_lst = []
    for col in range(9):
        for row in range(9):
            b_row = board_row(s)
            c = b_row[row][col]
            b_col.append(c)
    for i in range(9):
        lst = b_col[i*9:(i+1)*9]
        b_col_lst.append(lst)

    return b_col_lst


def col_ok(board,col):
    b_col = board_col(s)
    return repeat_int(b_col[col])


def board_box(board,box_number):
    box_individual = []
    
    centers_dic = {0:(1,1),1:(4,1),2:(7,1),3:(1,4),4:(4,4),5:(7,4),6:(1,7),7:(4,7),8:(7,7)}
          
    #center is the coordinate of the center of the box; use box number to locate the coordinate
    center = centers_dic[box_number]
    row = int(center[0])
    col = int(center[1])
    board = board_row(s)
    box_individual.extend([board[col-1][row-1], 
                            board[col][row-1], 
                            board[col+1][row-1],
                            board[col-1][row], 
                            board[col][row], 
                            board[col+1][row], 
                            board[col-1][row+1], 
                            board[col][row+1], 
                            board[col+1][row+1]])
    return box_individual


def box_ok(board, box_number):
    b_box = board_box(board, box_number)
    return repeat_int(b_box)

def matches(pattern,lst):
    if len(pattern) != len(lst):
        return False
    for (p,l) in zip(pattern,lst):
        if p != None and p != l:
            return False 
    return True 


    
#three obvious functions, test the number of elements in each row, col, and box, if 8, then report the index number            


def obvious_row(board, r):
    board = board_row(s)
    for r in range(9):
        set_full = {1,2,3,4,5,6,7,8,9}
        r_set = set(board[r])
        r_intersection = r_set.intersection(set_full)
        if len(r_intersection) == 8:
            return board[r].index(None)
    return False 

def obvious_col(board, c):
    board = board_col(s)
    for c in range(9):
        set_full = {1,2,3,4,5,6,7,8,9}
        c_set = set(board[c])
        c_intersection = c_set.intersection(set_full)
        if len(c_intersection) == 8:
            return board[c].index(None)
    return False

def obvious_box(board, box_number):
    for box_number in range(9):
        set_full = {1,2,3,4,5,6,7,8,9}
        box_set = set(board_box(board, box_number))
        box_intersection = box_set.intersection(set_full)
        if len(box_intersection) == 8:
            return board[box_number].index(None)
    return False

def box_of(row,col):
    return 3*(row // 3) + col // 3

def constrained_cells(board, row):
    for col in range(9):  
        box_number = 3*(row//3) + col // 3
        board1 = board_row(s)
        board2 = board_col(s)
        board3 = board_box(s,box_number)
        if board1[row][col] == None:
            set_full = {1,2,3,4,5,6,7,8,9}
            set_row = set(board1[row]).intersection(set_full)
            set_col = set(board2[col]).intersection(set_full)
            set_box = set(board3).intersection(set_full)
            set_draft = set_row.union(set_col)
            set_whole = set_draft.union(set_box)
            if len(set_whole) == 8:
                return col 
    return False

l1 = [[7, 8, None, None, 9, None, None, None, None], 
     [None, 9, 4, 3, None, None, None, None, None], 
     [None, 1, None, None, 4, None, None, None, 9], 
     [3, None, 1, None, None, 4, 8, 5, None], 
     [None, None, None, 5, None, 8, None, None, None], 
     [None, 5, 8, 7, None, None, 2, None, 4], 
     [9, None, None, None, 7, None, None, 1, None], 
     [None, None, None, None, None, 9, 5, 4, None], 
     [None, None, None, None, 1, None, None, 3, 2]]


def board_from_line(s):
    b_row = []
    for row in range(9):
        r = s[row*9:(row+1)*9]
        b_row.append(string_int(r))
    return b_row      


def board_clone(board_lst):
    clone = []
    for r in range(9):
        row = board_lst[r]
        clone.append(row[::])
    return clone

def board_row_new(board_lst, row):
        return board_lst[row]    

def board_col_new(board_lst, col):
    b_col = []
    for row in board_lst:
        b_col.append(row[col])
    return b_col 

def board_box_new(board_lst,box_number):
    box_individual = []
    
    centers_dic = {0:(1,1),1:(4,1),2:(7,1),3:(1,4),4:(4,4),5:(7,4),6:(1,7),7:(4,7),8:(7,7)}
          
    #center is the coordinate of the center of the box; use box number to locate the coordinate
    center = centers_dic[box_number]
    row = int(center[0])
    col = int(center[1])
    board = board_lst
    box_individual.extend([board[col-1][row-1], 
                            board[col][row-1], 
                            board[col+1][row-1],
                            board[col-1][row], 
                            board[col][row], 
                            board[col+1][row], 
                            board[col-1][row+1], 
                            board[col][row+1], 
                            board[col+1][row+1]])
    return box_individual


def row_ok_new(board_lst,row):  
    b_row = board_row_new(board_lst, row)
    return repeat_int(b_row)

def col_ok_new(board_lst,col):
    b_col = board_col_new(board_lst, col)
    return repeat_int(b_col)

def box_ok_new(board_lst, box_number):
    b_box = board_box_new(board_lst, box_number)
    return repeat_int(b_box)


def board_possible_in_cell(board_lst, row, col):
    box_number = box_of(row, col)

    lst_possible = [0]
    board_clone0 = board_clone(board_lst)
    if board_clone0[row][col] == None:
        for n in range(1,10):
            board_clone0[row][col] = n
            board_clone1 = board_row_new(board_clone0, row)
            board_clone2 = board_col_new(board_clone0, col)
            board_clone3 = board_box_new(board_clone0, box_number)
            
            if not repeat_int(board_clone1):
                if not repeat_int(board_clone2):
                    if not repeat_int(board_clone3):
                        lst_possible.append(n)     
        lst_possible.remove(0)
    return lst_possible 
def possibilities_dict(board_lst):
    possibilities = {}
    for row in range(9):
        for col in range(9):
            possibilities[(row,col)] = board_possible_in_cell(board_lst, row, col)
    return possibilities

def box_position(box_number):
    box = []
    centers_dic = {0:(1,1),1:(4,1),2:(7,1),3:(1,4),4:(4,4),5:(7,4),6:(1,7),7:(4,7),8:(7,7)}
    center = centers_dic[box_number]
    row = int(center[0])
    col = int(center[1])
    box.extend([(col-1, row-1), 
                (col, row-1), 
                (col+1, row-1),
                (col-1, row), 
                (col, row), 
                (col+1, row), 
                (col-1, row+1), 
                (col, row+1), 
                (col+1, row+1)])
    return box


#def naked_singles(row, col):
    #possibilities_clone = possibilities_dict(l)
    #if len(possibilities_clone[(row, col)]) == 1:
        #n = possibilities_clone[(row, col)]
        #print(n)
        #n = n[0]
        #for i in range(9):
            #if n in possibilities_clone[(i, col)]:
                #possibilities_clone[(i, col)].remove(n)
            #if n in possibilities_clone[(row, i)]:
                #possibilities_clone[(row, i)].remove(n)
        #box_number = box_of(row, col)
        #box_coordinates = box_position(box_number)
        #for (r,c) in box_coordinates:
            #if n in possibilities_clone[(r, c)]:
                #possibilities_clone[(r, c)].remove(n)
    #return possibilities_clone

def possibilities_board(possibilities_dic):
    possibilities_clone = possibilities_dic
    possibilities_row = []
    possibilities_row_split = []
    for row in range(9):
        for i in range(9):
            possibilities_row.append(possibilities_clone[(row, i)])
    for r in range(9):
        split = possibilities_row[r*9: (r+1)*9]
        possibilities_row_split.append(split)
        
    return possibilities_row_split

def get_frequency_dict(sequence):
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

def hidden_singles_row(possibilities_dic, enter_number):
    possibilities_row_split = possibilities_board(possibilities_dic)
    frequency_row_lst = []
    for row in range(9):
        row_holds_lst = possibilities_row_split[row]
        row_lst_combined = []
        for i in range(9):
            row_elt = row_holds_lst[i]
            row_lst_combined.extend(row_elt)
        frequency_row_dict = get_frequency_dict(row_lst_combined)
        frequency_row_lst.append(frequency_row_dict.get(enter_number, 0))
    coordinates = []
    for r in range(9):
        if frequency_row_lst[r] == 1:
            for col in range(9):
                if int(enter_number) in possibilities_dic[(r, col)]:
                   coordinates.append((r, col))
        
    return coordinates

def possibilities_board_transpose(possibilities_dic):
    p_board = possibilities_board(possibilities_dic)
    transposed = [None]*len(p_board[0])
    for i in range(len(transposed)):
        transposed[i] = [None]*len(transposed)
    for t in range(len(p_board)):
        for tt in range(len(p_board[t])):
            transposed[t][tt] = p_board[tt][t]
    return transposed

def hidden_singles_col(possibilities_dic, enter_number):
    possibilities_col_split = possibilities_board_transpose(possibilities_dic)
    frequency_col_lst = []
    for col in range(9):
        col_holds_lst = possibilities_col_split[col]
        col_lst_combined = []
        for i in range(9):
            col_elt = col_holds_lst[i]
            col_lst_combined.extend(col_elt)
        frequency_col_dict = get_frequency_dict(col_lst_combined)
        frequency_col_lst.append(frequency_col_dict.get(enter_number, 0))
    coordinates = []
    for c in range(9):
        if frequency_col_lst[c] == 1:
            for row in range(9):
                if int(enter_number) in possibilities_dic[(row, c)]:
                    coordinates.append((row, c))
    return coordinates


def possibilities_board_box(possibilities_dic):
    p_board_box = []
    for n in range(9):
        box_possibilities = []
        for (r, c) in box_position(n):
            box_possibilities.append(possibilities_dic[(r, c)])
        p_board_box.append(box_possibilities)
    return p_board_box 

def hidden_singles_box(possibilities_dic, enter_number):
    possibilities_box_split = possibilities_board_box(possibilities_dic)
    frequency_box_lst = []
    for box in range(9):
        box_holds_lst = possibilities_box_split[box]
        box_lst_combined = []
        for i in range(9):
            box_elt = box_holds_lst[i]
            box_lst_combined.extend(box_elt)
        frequency_box_dict = get_frequency_dict(box_lst_combined)
        frequency_box_lst.append(frequency_box_dict.get(enter_number, 0))
    coordinates = []
    for b in range(9):
        if frequency_box_lst[b] == 1:
            box_possible_coordinates = box_position(b)
            for (r, c) in box_possible_coordinates:
                if int(enter_number) in possibilities_dic[(r, c)]:
                    coordinates.append((r, c))
    return coordinates 

