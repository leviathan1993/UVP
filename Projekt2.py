
from tkinter import *

import random

import string #za oznacevanje polj (A1,...)

from functools import partial

import time

import tkinter.messagebox

class Battleship():
    
    def __init__(self, master):
        self.st_vrstic = int(input("Stevilo vrstic: "))
        self.st_stolpcev = int(input("Stevilo stolpcev: "))
        self.dol_ladje = int(input("Max dolzina: "))
        self.seznam_ladij=("Enterprise", "Titanik", "Triglav","Rdeči Oktober")
        if self.dol_ladje > self.st_vrstic or self.dol_ladje>self.st_stolpcev:
            
            tkinter.messagebox.showinfo("Window Title", "Predolge ladje!")
            
            return None

        # Glavni menu
        self.menu = Menu(master)
        master.config(menu=self.menu) # Dodamo menu

        # Naredimo podmenu "File"
        file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=file_menu)
        def odpri_txt():
            Koordinate = str()
            with open("file.txt","r") as f:
                for i in f:
                    Koordinate += i
            tkinter.messagebox.showinfo("Zgodovina", Koordinate)

        def resitve():
            koordinate = str()
            inv_map = {}
            for k, v in self.locations_dict.items():
                inv_map[v] = inv_map.get(v, [])
                inv_map[v].append(k)
            for i in inv_map.keys():
                for j in inv_map[i]:
                

                    koordinate += str(i) + ":" + str(self.seznam_polj[j-1]) + "\n"
            
                
            tkinter.messagebox.showinfo("Rešitve",koordinate)
            

        
        # Dodamo izbire v file_menu
        file_menu.add_command(label="Zgodovina",command=odpri_txt)
        file_menu.add_command(label="Rešitve", command=resitve)
        file_menu.add_separator() # To doda separator v menu
        file_menu.add_command(label="Quit", command=master.destroy)

        # Naredimo podemnu "Edit"
        edit_menu = Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=edit_menu)

        # Dodamo izbire v edit_menu. Te izbire ne delajo ničesar,
        # ker nismo nastavili command=...
        """edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Paste")
        edit_menu.add_command(label="Delete")"""
               
        # Najprej naredimo grafični element Frame, ki služi kot
        # "skladisce", v katerega postavimo gumbe in napise
        self.frame = Frame(master) # Ta okvir je vsebovan v master-ju
        self.frame.grid()          # To dejansko naredi vsebino vidno
        self.a = master

        #Odpremo datoteko samo zato da se prepiše na novo,
        #če je že prej bila uporabljena
        with open("file.txt", "w") as f:
            pass
        
        self.initial_board(master)
        self.add_ships()
        master.attributes("-topmost", True)
        
    
    def button_pushed(self, button_num, text):
        f = open("file.txt", "a")
            
        #print(button_num,self.locations_dict)
        self.buttons_list[button_num].config(bg="red")
        if button_num in self.locations_dict:
            f.write(text+" ZADETEK! \n")
            
            self.description.set("Zadel si "+self.locations_dict[button_num])
            self.buttons_list[button_num].config(bg="green")
            if button_num in self.locations2_dict: self.locations2_dict.pop(button_num)
        else:
            self.description.set("Zgrešil si!")
            f.write(text+" Pogrešio si :( \n")
        for i in self.seznam_ladij:
            if i not in self.locations2_dict.values():
                self.description.set("U sank muh %s" % i)
                ladje = list(self.seznam_ladij)
                ladje.remove(i)
                self.seznam_ladij = tuple(ladje)
                
                
        if self.locations2_dict == {}:
            print("ZMAGA??!!")
            self.a.destroy()

    
    def initial_board(self,master):
        
        self.buttons_list = []
        but_num=0
        crke_polj=string.ascii_uppercase[:self.st_vrstic]
        #za vsako vrstico izbere drugo crko
        #pravilne_resitve = []


        #Naredimo seznam Polj npr. {A:{1,2,3,4}}
        self.seznam_polj = list()
        for row_num in crke_polj:
            for col_num in range(1,self.st_stolpcev+1):
                self.seznam_polj.append(str(row_num)+str(col_num))
                text = row_num+str(col_num)
                b=Button(self.frame, text=row_num+str(col_num),
                            bg="white", width=3, 
                            command=partial(self.button_pushed,but_num,text))
                self.buttons_list.append(b)#editor adds crap here
                ##              should be append(lower case B)/>
                b.grid(row=crke_polj.index(row_num), column=col_num)
                but_num += 1
 
        ## Kaj se je zgodilo
        self.description = StringVar()
        Label(self.frame, textvariable=self.description,
                 fg="red").grid(row=9, column=0,
                 columnspan=5, sticky="ew")
 
        ## exit

        Button(text="Exit", bg="yellow",
                  command=master.destroy).grid(row=10, column=1,
                  columnspan=3, sticky="ew")

    def add_ships(self):
        #Ladje doda v random stevilke
        #doda lokacijo v slovar
        def navpicno_ali_vodoravno():
            return random.choice([True,False])
        def dolzina_ladje(n):
            return random.randint(1,n)
        
        izbire = []
        for i in range(self.st_vrstic*self.st_stolpcev):
            izbire.append(i)
        self.locations_dict={}

        

        crke_polj = string.ascii_uppercase[:self.st_vrstic]
        #seznam_ladij=("Enterprise", "Titanik", "Triglav","Rdeči Oktober")
        for stevilo, ime in enumerate(self.seznam_ladij):
            gd = navpicno_ali_vodoravno()
            dolzina = dolzina_ladje(self.dol_ladje)
        #zdaj izberemo eno stevilo iz OMEJENEGA stevila iz "izbire", omejeno je 
        #toliko, da mu lahko pristejemo dolzino v desno ali navzdol,da bo se
        #vedno na plosci
        #True == navpicno, False == vodoravno
            
            if gd == False:
                seznam=[]
                for i in izbire:
                    if i%self.st_stolpcev+dolzina<=self.st_stolpcev:
                        seznam.append(i)
                
                
                
                #paziti moram, da se "key" ne ponovi, se pravi, da
                          #je vsak "key" v seznamu "izbire"
                while True:
                    st = random.choice(seznam)
                    seznam2=[]
                    for i in range(dolzina):
                        
                        key = st + i
                        if key not in izbire:
                            #Ce key ni v "izbire" se zanka zakljuci
                            #in gremo nov krog, kjer upamo da bo nakljucno
                            #izbrano stevilo, ki se ne prekriva z drugimi
                            seznam2=[]
                            break
                        seznam2.append(key)
                        
                    if seznam2==[]:
                        pass
                    else:
                        for key in seznam2:
                            self.locations_dict[key]=ime
                            izbire.remove(key)
                            
                        break
            #enako v primeru, ce je ladja navpicna oz. vodoravna 
            
            elif gd == True:
                seznam=[]
                for i in izbire:
                    if i / self.st_stolpcev + dolzina > self.st_vrstic:
                        break
                    else:
                        seznam.append(i)

                while True:
                    seznam2 = []
                    st = random.choice(seznam)
                    
                    for i in range(dolzina):
                        
                        key = st + i*self.st_stolpcev
                        if key not in izbire:
                            #Ce key ni v "izbire" se zanka zakljuci
                            #in gremo nov krog, kjer upamo da bo nakljucno
                            #izbrano stevilo, ki se ne prekriva z drugimi
                            seznam2=[]
                            break
                        seznam2.append(key)
                        
                    if seznam2==[]:
                        pass
                    else:
                        for key in seznam2:
                            self.locations_dict[key]=ime
                            izbire.remove(key)
                            
                        break

        for x,y in self.locations_dict.items():
            print(x,y)
        #naredimo dodaten slovar, ki je isti kot self.locations_dict
        #da se bo igra zakljucila, ko bo zmanjkalo moznih gumbov
        self.locations2_dict = dict(self.locations_dict)
root = Tk()

BS=Battleship(root)
root.mainloop()
