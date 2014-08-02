'''
    GUI Class - handles drawing text to the screen and taking user input
'''
from Tkinter import Tk, StringVar, Label, Entry
from time import sleep

class Slide(Tk):
    
    def __init__(self, parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        

    def initialize(self):
        self.grid()
        self.fullscreen()
        self.update()
        
        
    def fullscreen(self):
        self.geometry("%dx%d+0+0" % (self.winfo_screenwidth(), 
                                     self.winfo_screenheight()))
        self.overrideredirect(1) #Removes borders
        self.resizable(False, False)
        self.configure(background = "black")
        self.focus_set()
        

    def createLabel(self, startFunction, endFunction):
        self.labelVariable = StringVar()
        self.label = Label(self, textvariable=self.labelVariable, 
                      anchor="center", fg="white", bg="black", 
                      font="Arial 24 bold", wraplength=1100)
        self.label.grid(column=0, row=0, padx=20, pady=20)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.changeLabel(self.loadIntro(), startFunction)
        self.bind("<Escape>", endFunction)
        
        
    def createEntryBox(self):
        self.entryVariable = StringVar()
        self.entry = Entry(self, textvariable=self.entryVariable, 
                           font="Arial 24", bd = 0, fg="white", bg="black", 
                           insertbackground = "white", justify = "center")
        self.entry.grid(column=0, row=1, sticky = 'EW')
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.entry.focus_set()
        self.entryVariable.set("")

        
    def loadIntro(self):
        file = open("intro.txt")
        intro = file.readlines()
        intro += "\n\nWhen you are ready, press ENTER to continue."
        file.close()
        
        return ''.join(intro)
    
    
    def changeLabel(self, message, newFunction):
        self.labelVariable.set(message)
        self.bind("<Return>", newFunction)
        
        
    def greyScreen(self):
        GREY = "#888888"
        self.configure(background=GREY)
        self.label.configure(fg=GREY, bg=GREY)
        self.entry.configure(fg=GREY, bg=GREY, insertbackground=GREY)
        self.update()
        sleep(1.5)
        self.configure(background="black")
        self.label.configure(fg="white", bg="black")
        self.entry.configure(fg="white", bg="black", insertbackground="white")
        self.update()

        