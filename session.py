'''
    Session class - Manages the whole experiment and all other classes
'''

import sys, time
from tkSimpleDialog import askstring, askinteger
from tkMessageBox import showwarning, askquestion
from Tkinter import END
from gui import GUI
from data import Data
from soundlib import SoundLibrary

class Session(object):
    '''Initializes the session and calls helper classes

    Subclasses:
        soundlib: object that handles sound playback
        gui: object that handles the view
        data: object that collects and stores data
    Attributes:
        iterations: Tracks the number of trials the participant has completed
        currentSound: filename of the sound that is currently playing
        repetitions: The number of trials the participant must complete
        sequencing: True if a sequence has been requested by the researcher
    '''

    def __init__(self):
        '''Initializes classes and begins main loop'''
        self.soundlib = SoundLibrary()
        self.iterations = 0
        self.currentSound = ""
        self.repetitions = 0
        self.sequencing = False
        self.inOrder = False
        self.startTime = None
        self.endTime = None

        self.gui = GUI(None)
        self.gui.focus_set()

        self.promptSession()
        self.gui.createPrompt(self.startSession, self.endSession) # Sets up the view

        self.gui.mainloop()


    def promptSession(self):
        ''' Prompts the experimenter for the Subject ID, Session ID,
            and the number of repetitions
        '''
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
                    showwarning(' ','Integer must have a non-negative '
                                'non-zero value.')

            inorder = askquestion(' ', 'Should the sounds be played in order?')
            if inorder == "yes":
                self.inOrder = True
                seqname = "In Order"
            else:
                while (True):
                    loadseq = askquestion(' ', 'Then should a sequence be loaded?')
                    if loadseq == "yes":
                        seqfile = askstring(' ','Please specify the filename containing'
                                            ' the sequence.')
                        seqname = self.soundlib.loadSequence(seqfile)
                        if len(self.soundlib.sequence) > 0:
                            self.sequencing = True
                            break
                    elif loadseq == "no":
                        seqname = "None"
                        break

            answer = askquestion(' ','Subject: ' + ID + ', Session: ' + sess +
                                 ', Repetitions: ' + str(self.repetitions) +
                                 ', Sequence: ' + seqname + '\nIs this correct?')
            if answer == "yes":
                break

        self.data = Data(ID, sess) # Data collection object

    def startSession(self, event):
        '''Prompts the user for input, loops a sound and then waits for a
            response.
        '''
        self.startTime = time.time()
        self.gui.createEntryBox()
        self.gui.changeLabel("\n\n\n\n\n\n\n\nPlease type what word(s) you hear "
                             "and press ENTER to continue.", self.advanceSession)
        self.gui.greyScreen()

        self.setCurrentSound()


    def advanceSession(self, event):
        '''Adds response to the database, then clears the session'''
        self.endTime = time.time()

        self.data.add(self.currentSound, self.gui.entry.get(), self.endTime - self.startTime,
                      self.soundlib.getCurrentSoundLength())
        self.gui.entry.delete(0, END)  # Clears the response form

        self.iterate()


    def iterate(self):
        '''Stops the sound, greys the screen, and checks if the session
            is over.
        '''
        self.soundlib.stopAllSounds()
        self.gui.greyScreen()
        self.iterations += 1
        if self.iterations == self.repetitions:
            self.gui.changeLabel("\n\n\n\n\n\n\n\nThank you for participating!"
                                 "\nPlease inform the researcher that you are"
                                 " finished.", self.endSession)
            self.gui.entry.destroy()
        else:
            self.setCurrentSound()
            self.startTime = time.time()


    def endSession(self, event):
        '''Ends the session and records the data'''
        answer = askquestion(' ','End session?')
        if answer == "yes":
            if self.iterations > 0:
                self.data.recordData()
            sys.exit()

    def setCurrentSound(self):
        if (self.sequencing):
            self.currentSound = self.soundlib.playSequence(self.iterations)
        elif (self.inOrder):
            self.currentSound = self.soundlib.playInOrder(self.iterations)
        else:
            self.currentSound = self.soundlib.playRandom()
