# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 12:15:50 2018

@author: 糖糖
"""
from tkinter import *
from gamelogic import *
from tkinter import ttk
import os
import base64
from io import BytesIO
import time


SIZE = 500
grid_padding = 10

background_color = '#BBADA0'
cell_empty_color = '#CDC1B4'
cell_color_dict = {2:'#EEE4DA', 4:'#EDE0C8', 8:'#F2B179', 16:'#F59563', 32:'#F67C5F', 64:'#F65E3B', 128:'#EDCF72', 256:'#EDCC61', 512:'#EDC850', 1024:"#edc53f", 2048:"#edc22e"}
text_color_dict = {2:'#776E65', 4:'#776E65', 8:'#F9F6F2', 16:'#F9F6F2', 32:'#F9F6F2', 64:'#F9F6F2', 128:'#F9F6F2', 256:'#F9F6F2', 512:'#F9F6F2', 1024:"#f9f6f2", 2048:"#f9f6f2"}
FONT = ("Verdana", 40, "bold")
key_press = {'<Down>': move_down, '<Up>': move_up, '<Right>': move_right, '<Left>':move_left}



class Game(Tk):
    def __init__(self):
        super().__init__()
        self.title('2048')
        self.config(background = background_color)
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        w = int((screenWidth - SIZE -200)/2)
        h = int((screenHeight - SIZE -200)/2)
        self.geometry('+'+str(w)+'+'+str(h))
        self.resizable(width=False, height=False)
        
        self.score = 0
        self.won = False

        self.startFrame = StartFrame(self)
        self.startFrame.grid(row=0,column=0,sticky='nsew')
        self.gameFrame = GameFrame(self)
        self.gameFrame.grid(row=0,column=0,sticky='nsew')  
        self.gameOver = GameOver(self)
        self.gameOver.grid(row=0,column=0,sticky='nsew')

        self.showFrame(self.startFrame)
        
        
    def showFrame(self, frame, restart=False):
        if restart:
            self.score = 0
            self.won = False
        frame.__init__(self)
        frame.grid(row=0,column=0,sticky='nsew')
        frame.tkraise()

    def getScore(self):
        return self.score
    def setScore(self, score):
        self.score += score
    def getWon(self):
        return self.won
    def setWon(self, state):
        self.won = state



class GameFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master.bind('<Key>', self.move)
        self.config(background = background_color)
        
       
        self.v = IntVar()
        self.v.set(self.master.getScore())
        
        
        scoreFrame = Frame(self)
        scoreFrame.grid(row=0,column=0,columnspan=4)
        
        
        s_Label = Label(scoreFrame, text='Score',
                           font=("Verdana", 30),
                           background = background_color,foreground='#EEE4DA')
        s_Label.pack(side=LEFT)
        scoreLabel = Label(scoreFrame, textvariable=self.v,
                           font=("Verdana", 30, 'bold'),
                           background = background_color,foreground='#FFFFFF')
        scoreLabel.pack(side=LEFT)
        
        
#        t_label = Label(scoreFrame, text='Time',
#                        font=("Verdana", 30),
#                        background = background_color,foreground='#EEE4DA')
#        t_label.pack(side=RIGHT)
#        timeLabel = Label(scoreFrame, text=0,
#                          font=("Verdana", 30, 'bold'),
#                          background = background_color,foreground='#FFFFFF')
#       timeLabel.pack(side=RIGHT)
#                        
        
        
        self.cell_list = []
        for i in range(4):
            empty_list = []
            for j in range(4):
                cell = Frame(self,width=SIZE/4,height=SIZE/4)
                cell.grid(row=i+1,column=j,padx=grid_padding,pady=grid_padding)
                l = Label(master=cell, text = '', font=FONT,
                          background=cell_empty_color, justify=CENTER,
                          width=4, height=2)
                l.grid()
                empty_list.append(l)
            self.cell_list.append(empty_list)


                
        self.matrix = new_game(4)
        self.add_number(self.matrix)
        self.add_number(self.matrix)
        self.color_decide(self.matrix, self.cell_list)
        


        
    def color_decide(self, matrix, cell):         
        for i in range(4):
            for j in range(4):
                if matrix[i][j] == 0:
                    cell[i][j].config(text='',
                                  background=cell_empty_color)
                else:
                    cell[i][j].config(text=matrix[i][j],
                            foreground=text_color_dict[matrix[i][j]],
                            background=cell_color_dict[matrix[i][j]])
        
    def add_number(self, matrix):
            add_random_number(matrix)
            
    

    def move(self, event):
        for key in key_press.keys():
            if (str('<') + event.keysym + ('>') == key) and (self.matrix != key_press[str('<') + event.keysym + ('>')](self.matrix)):
                (self.matrix, score) = key_press[str('<') + event.keysym + ('>')](self.matrix)
                self.master.setScore(score)
                self.v.set(self.master.getScore())
                self.color_decide(self.matrix, self.cell_list)                
                # Check Game State if 2048 == Win, Can change 2048 to any number 
                if win(self.matrix, 2048):
                    self.master.setWon(True)
                    self.master.showFrame(self.master.gameOver)
                self.add_number(self.matrix)
                self.color_decide(self.matrix, self.cell_list)
                # Check Game State if No where to Move == Lose
                if len([self.matrix[i][j] for i in range(len(self.matrix)) for j in range(len(self.matrix[i])) if self.matrix[i][j] == 0]) == 0:
                    # Lose will Return False, Else Return True
                    t = transpose(self.matrix)
                    if not game_state(self.matrix) and not game_state(t):
                        self.master.showFrame(self.master.gameOver)
                        


class StartFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        bg = '#FAF8EF'
        self.config(background=bg)
        
        title = Label(self, text='2048',font=("Verdana", 50, 'bold'), foreground='#776E65', background=bg)
        title.place(relx=0.5, rely=0.31, anchor='center')         
        
        sub1 = Label(self, text='Join the numbers and get to the ',
                         font=("Verdana", 20), foreground='#776E65', background=bg)
        sub1.place(relx=0.5, rely=0.45, anchor='center')           
        sub2 = Label(self, text='2048 tile!', font=("Verdana", 20, 'bold'),
                      foreground='#776E65', background=bg)
        sub2.place(relx=0.27, rely=0.52, anchor='center')
        
        path = os.getcwd()
        file = os.path.join(path+'\\ClickToPlay.gif')
        file = file.replace('\\','/')
        
        img = PhotoImage(file=file)
        button = Button(self, image=img, command=lambda:self.master.showFrame(self.master.gameFrame))
        button.image = img # Keep a Reference !!!!!!!!!!!!!!!!!!
        button.place(relx=0.5, rely=0.65, anchor='center')

        
        
        
class GameOver(Frame):
    def __init__(self, master, **kwargs):
        bg = '#FAF8EF'
        super().__init__(master, **kwargs)
        self.config(background = bg)
        # Prevent from continuously getting scores
        self.master.bind('<Key>', self.ignore)

        
        get_won = self.master.getWon()
        state = 'Game Over!'
        if get_won == True:
            state = 'You Win!'
        
        status = Label(self, text=state, 
                      font=("Verdana", 50, 'bold'),
                      background = bg, foreground = '#776E65')
        status.place(relx=0.5, rely=0.3, anchor='center')
        
        score = Label(self, text = 'Score',
                      font=("Verdana", 35),
                      background = bg, foreground = '#8F7A66')
        score.place(relx=0.35, rely=0.53, anchor='center')
        
        get_score = self.master.getScore()    
        s = Label(self, text = get_score,
                  font=("Verdana", 45, 'bold'),
                  background = bg, foreground = '#BBADA0')
        s.place(relx=0.35, rely=0.65, anchor='center')
        
        
        
        img_restart = PhotoImage(data = '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')                     
        b_re = Button(self, image = img_restart ,
                        bd=0,bg=bg,
                        highlightbackground=bg,
                        highlightthickness=0,
                        activebackground=bg,
                        highlightcolor=bg,
                        command = lambda:self.master.showFrame(self.master.gameFrame, restart = True))
        b_re.image = img_restart
        b_re.place(relx=0.65, rely=0.54, anchor='center')
        
        img_exit = PhotoImage(data = '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')
        b_exit = Button(self, image = img_exit ,
                        bd=0,bg=bg,
                        highlightbackground=bg,
                        highlightthickness=0,
                        activebackground=bg,
                        highlightcolor=bg)
        b_exit.image = img_exit
        b_exit.place(relx=0.65, rely=0.66, anchor='center')
        
    def ignore(self, event):
        return 'break'
        
        
        
        
        
        

        
if __name__ == '__main__':
    root = Game()
    root.mainloop()