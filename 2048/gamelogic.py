# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 15:15:18 2018

@author: 糖糖
"""

import random


# 初始化新遊戲
def new_game(number):
    matrix = []
    for _ in range(number):
        matrix.append([0] * number)  # [0, 0, 0, 0]
    return matrix



# Return Ture if Win, Else False
def win(matrix, number=2048):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == number:
                return True
    return False




# Return False if Lose
def game_state(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i]) - 1):
            if matrix[i][j] == matrix[i][j+1]:
                return True
    return False
    
    
                



# 新的隨機數字
def add_random_number(matrix):
    # List Comprehension
    try:
        (i, j) = random.choice([(i, j) for i in range(len(matrix)) for j in 
                    range(len(matrix[i])) if matrix[i][j] == 0])
        if random.random() <= 0.10:
            matrix[i][j] = 4
        else:
            matrix[i][j] = 2
    except IndexError:
        pass
        
        
# 每一row逆轉矩陣        
def reverse(matrix):
    r = []
    for i in range(len(matrix)):
        reverse_elements = []
        for j in range(len(matrix[i])):
            reverse_elements.append(matrix[i][-j-1])
        r.append(reverse_elements)
    return r
        

# 轉置矩陣
def transpose(matrix):
    t = []
    for i in range(len(matrix)):
        elements = []
        for j in range(len(matrix[i])):
            elements.append(matrix[j][i])
        t.append(elements)
    return t



# 壓縮，去除零後重新加上零
def compressing(matrix):
    compressed = []
    for i in range(len(matrix)):
        count = 0
        new_list = []
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                count += 1
            else:
                new_list.append(matrix[i][j])
        for _ in range(count):
            new_list.append(0)
        compressed.append(new_list)
    return compressed
                

# 合併，及加上零   
def merging(matrix):
    merged = []
    score = 0
    for i in range(len(matrix)):
        li = []
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                pass
            elif j <= (len(matrix[i])-2) and matrix[i][j] == matrix[i][j+1]:
                li.append(matrix[i][j]*2)
                matrix[i][j+1] = 0
                score = score + matrix[i][j]*2
            else:
                li.append(matrix[i][j])
        
        l = len(matrix[i]) - len(li)
        for _ in range(l):
            li.append(0)
        merged.append(li)
    return (merged, score)
    
    
    
#  向左，compress plus merge
def move_left(matrix):
    c = compressing(matrix)
    return merging(c)

        
#  向右
def move_right(matrix):
    r = reverse(matrix)
    c = compressing(r)
    (m, s) = merging(c)
    r_m = reverse(m)
    return (r_m, s)
        
        
#  向上
def move_up(matrix):
    t = transpose(matrix)
    c = compressing(t)
    (m, s) = merging(c)
    t_m = transpose(m)
    return (t_m, s)

#  向下
def move_down(matrix):
    t = transpose(matrix)
    r = reverse(t)
    c = compressing(r)
    (m, s) = merging(c)
    r_m = reverse(m)
    t_m = transpose(r_m)
    return (t_m, s)
        


        
        





