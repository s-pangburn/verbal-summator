'''
    GUI Class - handles drawing text to the screen and taking user input
'''
import tkSimpleDialog, tkMessageBox
from Tkinter import Tk, StringVar, Label, Entry, END
from data import Data
from soundlib import SoundLibrary
from time import sleep

class Slide(Tk):
    
    def __init__(self, parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        

    def initialize(self):
        self.grid()
        self.fullscreen()
        
        self.library = SoundLibrary()
        self.currentSound = ""
        self.iterations = 0
        self.repetitions = 0
        
        self.promptSession()
        self.createLabel()
        
        self.update()
        
        
    def fullscreen(self):
        self.geometry("%dx%d+0+0" % (self.winfo_screenwidth(), 
                                     self.winfo_screenheight()))
        self.overrideredirect(1) #Removes borders
        self.resizable(False, False)
        self.configure(background = "black")
        self.focus_set()
        self.bind("<Escape>", self.endSession)
        
    def promptSession(self):
        while (True):
            ID = tkSimpleDialog.askstring(' ','Please enter Subject ID:')
            if ID == None:
                self.destroy()
            sess = tkSimpleDialog.askstring(' ','Please enter Session ID:')
            if sess == None:
                self.destroy()
                
            while self.repetitions < 1:
                self.repetitions = tkSimpleDialog.askinteger(' ','Please enter the number of repetitions:')
                if self.repetitions == None:
                    self.destroy()
                elif self.repetitions < 1:
                    tkMessageBox.showwarning(' ', "Integer must have a non-negative non-zero value.")
                    
            answer = tkMessageBox.askquestion(' ','Subject: '+ID+', Session: '+sess+', Repetitions: '+str(self.repetitions)+'\nContinue?')
            if answer == "yes":
                break
            
        self.data = Data(ID, sess) #Data collection object
        

    def createLabel(self):
        self.labelVariable = StringVar()
        self.label = Label(self, textvariable=self.labelVariable, 
                      anchor="center", fg="white", bg="black", 
                      font="Arial 24 bold", wraplength=1100)
        self.label.grid(column=0, row=0, padx=20, pady=20)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.changeLabel(self.loadIntro(), self.startSession)
        
        
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

        
    def startSession(self, event):
        self.createEntryBox()
        self.changeLabel("\n\n\n\n\n\n\n\nPlease type what word(s) you hear and press ENTER to continue.", self.advanceSession)
        self.iterations+=1
        self.greyScreen()
        
        self.currentSound = self.library.playRandom() #TODO: Extract more specific method
        

    def iterate(self):
        self.library.stopAllSounds()
        self.greyScreen()
        if self.iterations == self.repetitions:
            self.changeLabel("\n\n\n\n\n\n\n\nThank you for participating! \nPlease inform the researcher that you are finished.", self.endSession)
            self.entry.destroy()
        else:
            self.iterations += 1
            self.currentSound = self.library.playRandom() #TODO: Extract more specific method


    def advanceSession(self, event):
        self.data.add(self.currentSound, self.entry.get())
        self.entry.delete(0, END)
        
        self.iterate()
        

    def endSession(self, event):
        answer = tkMessageBox.askquestion(' ','End session?')
        if answer == "yes":
            if self.iterations > 0:
                self.data.recordData()
            self.destroy()