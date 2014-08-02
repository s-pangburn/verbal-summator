'''
Created on Jul 30, 2014

@author: Stephen
'''

import sys
from tkSimpleDialog import askstring, askinteger
from tkMessageBox import showwarning, askquestion
from Tkinter import END
from gui import Slide
from data import Data
from soundlib import SoundLibrary

class Session(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.library = SoundLibrary()
        self.iterations = 0
        self.currentSound = ""
        self.repetitions = 0
        
        self.gui = Slide(None)
        self.gui.focus_set()
        
        self.promptSession()
        self.gui.createLabel(self.startSession, self.endSession)
        
        self.gui.mainloop()
        
    
    def promptSession(self):
        while (True):
            ID = askstring(' ','Please enter Subject ID:')
            if ID == None:
                sys.exit()
            sess = askstring(' ','Please enter Session ID:')
            if sess == None:
                sys.exit()
                
            while self.repetitions < 1:
                self.repetitions = askinteger(' ','Please enter the number of '
                                              'repetitions:')
                if self.repetitions == None:
                    sys.exit()
                elif self.repetitions < 1:
                    showwarning(' ', 'Integer must have a non-negative '
                                'non-zero value.')
                    
            answer = askquestion(' ','Subject: ' + ID + ', Session: ' + sess +
                                 ', Repetitions: ' + str(self.repetitions)+'\n'
                                 'Is this correct?')
            if answer == "yes":
                break
            
        self.data = Data(ID, sess) #Data collection object
        
    def startSession(self, event):
        self.gui.createEntryBox()
        self.gui.changeLabel("\n\n\n\n\n\n\n\nPlease type what word(s) you hear "
                             "and press ENTER to continue.", self.advanceSession)
        self.gui.greyScreen()
        
        self.currentSound = self.library.playRandom() #TODO: Extract more specific method
        

    def iterate(self):
        self.library.stopAllSounds()
        self.gui.greyScreen()
        self.iterations += 1
        if self.iterations == self.repetitions:
            self.gui.changeLabel("\n\n\n\n\n\n\n\nThank you for participating!"
                                 "\nPlease inform the researcher that you are"
                                 "finished.", self.endSession)
            self.gui.entry.destroy()
        else:
            self.currentSound = self.library.playRandom() #TODO: Extract more specific method


    def advanceSession(self, event):
        self.data.add(self.currentSound, self.gui.entry.get())
        self.gui.entry.delete(0, END)
        
        self.iterate()
        

    def endSession(self, event):
        answer = askquestion(' ','End session?')
        if answer == "yes":
            if self.iterations > 0:
                self.data.recordData()
            sys.exit()