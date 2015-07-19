try:
    import Tkinter as tk     ## Python 2.x
except ImportError:
    import tkinter as tk     ## Python 3.x

import random
from functools import partial

class Battleship():
    def __init__(self):
        self.top = tk.Tk()
        self.initial_board()
        self.add_ships()
        self.top.mainloop()

    def add_ships(self):
        """ add ships to a random square number
            use random.shuffle as randint can return the same number
            when called multiple times

            add location to a dictionary whose key is the 
            button number pointing to the description
        """
        choices=[]
        for i in range(25):
            choices.append(i)
        random.shuffle(choices)
        self.locations_dict={}
        vsota=0
        for ctr, lit in enumerate(("Battleship", "Destroyer", "Row Boat")):
            
            for i in range(3):
                vsota+=1
                
                key=choices[vsota]
                self.locations_dict[key]=lit
                print (lit, key)     ## for testing
                

    def button_pushed(self, button_num):
        self.buttons_list[button_num].config(bg="lightgray")
        if button_num in self.locations_dict:
            self.description.set("UU you touch my tralala "+self.locations_dict[button_num])
        else:
            self.description.set("Oh my ding ding dong")

    def initial_board(self):
        """  25 buttons numbered 0-->24
             each button object saved in the list, buttons_list
             creates a 5X5 matrix of buttons
        """
        self.buttons_list = []
        but_num=0
        for row_num in range(5):
            for col_num in range(6):
                b=tk.Button(self.top, text=str(but_num),
                            bg="white", width=3, 
                            command=partial(self.button_pushed, but_num))
                self.buttons_list.append(b)#editor adds crap here
                ##              should be append(lower case B)/>
                b.grid(row=row_num, column=col_num)
                but_num += 1

        ## label to say what has happened
        self.description = tk.StringVar()
        tk.Label(self.top, textvariable=self.description,
                 fg="red").grid(row=9, column=0,
                 columnspan=5, sticky="ew")

        ## exit button
        tk.Button(text="Exit", bg="yellow",
                  command=self.top.quit).grid(row=10, column=1,
                  columnspan=3, sticky="ew")

BS=Battleship() 
