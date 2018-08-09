#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 17:15:35 2018

@author: IreneLi
"""


def board(set2):
    big_list=[]
    for x in range(9):
        list= set2[9*x:9*(x+1)]
        big_list.append(list)
    return big_list

def Place_the_last_number(submitted,number):
    b=0
    for x in range(9):
        if number in submitted[x]:
            b+=1
    if b!=8:
        return False
    else:
        for x in range(9):
            if not number in submitted[x]:
                row=x+1
                break

    d=0
    lst=[]
    for x in range(9):
        for y in range(9):
            lst.append(submitted[y][x])
            print(lst)

    listbylist=board(lst)

    for x in range(9):
        if number in listbylist[x]:
            d+=1

    if d!=8:
        return False
    else:
         for x in range(9):
            if not number in listbylist[x]:

                col=x+1
                break
    coordinate=(row,col)
    return coordinate

def which_number_is_the_last_one(submitted):
    dic={}
    for x in range (1,10):
        if not Place_the_last_number(submitted,x)==False:
            a=x
            dic[a]=Place_the_last_number(submitted,x)
    return dic
