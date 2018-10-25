'''
    Session class - Manages the whole experiment and all other classes
'''

import sys, time, os, yaml
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
        sequenceType: Specifies sequence type (IN-ORDER, LOADED, or RANDOM)
    '''

    def __init__(self):
        '''Initializes classes and begins main loop'''
        options = self.loadConfig()

        self.soundlib = SoundLibrary()
        self.iterations = 0
        self.currentSound = ""
        self.repetitions = options['numRepetitions']
        self.sequenceType = options['sequenceType'].upper()
        self.sequenceName = options['sequenceName']
        self.startTime = None
        self.endTime = None

        self.gui = GUI(None)

    def loadConfig(self):
        '''Loads CONFIG.yml and prepares the parameters for the session'''
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + "/../CONFIG.yml", 'r') as config:
            options = yaml.load(config)
        return options


    def start(self):
        self.gui.focus_set()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.gui.iconbitmap(default=dir_path + "/blank.ico")

        self.promptSession()
        self.gui.createPrompt(self.startSession, self.endSession) # Sets up the view

        self.gui.mainloop()

    def promptSession(self):
        ''' Prompts the experimenter for the Subject ID, Session ID,
            and the number of repetitions
        '''

        while (True):
            self.setRepetitions()
            self.specifySequence()

            participantId = askstring(' ','Please enter Subject ID:')
            if participantId == None:
                sys.exit()
            sessionId = askstring(' ','Please enter Session ID:')
            if sessionId == None:
                sys.exit()
            
            sequence = self.sequenceName if self.sequenceType == 'LOADED' else self.sequenceType

            answer = askquestion(' ','Subject: ' + participantId + ', Session: ' + sessionId +
                                 ', Repetitions: ' + str(self.repetitions) +
                                 ', Sequence: ' + sequence + '\nIs this correct?')
            if answer == "yes":
                break

        self.data = Data(participantId, sessionId) # Data collection object
    
    def setRepetitions(self):
        '''Prompts the user for a specific number of repetitions if none was specified'''
        while self.repetitions == None or self.repetitions < 1:
            self.repetitions = askinteger(' ','Invalid repetitions specified in CONFIG.yml.'
                                            ' Please enter the number of repetitions:')
            if self.repetitions == None:
                sys.exit()
            elif self.repetitions < 1:
                showwarning(' ','Integer must have a non-negative '
                            'non-zero value.')
    
    def specifySequence(self):
        '''Prompts the user for a sequence type if none was specified'''
        if self.sequenceType == None or self.sequenceType == "LOADED" and self.sequenceName == None:
            self.sequenceName = "None"
            inorder = askquestion(' ', 'No sequence specified in CONFIG.yml.'
                                    ' Should the sounds be played in-order?')
            if inorder == "yes":
                self.sequenceType = "IN-ORDER"
            else:
                while (True):
                    loadseq = askquestion(' ', 'Then should a sequence be loaded?')
                    if loadseq == "yes":
                        self.sequenceName = askstring(' ','Please specify the filename'
                                            ' containing the sequence.')
                        seqname = self.soundlib.loadSequence(self.sequenceName)
                        if len(self.soundlib.sequence) > 0:
                            self.sequenceType = "LOADED"
                            break
                    elif loadseq == "no":
                        self.sequenceType = "RANDOM"
                        break

    def startSession(self, event):
        '''Prompts the user for input, loops a sound and then waits for a
            response.
        '''
        self.startTime = time.time()
        self.gui.createEntryBox()
        self.gui.setLabel("\n\n\n\n\n\n\n\nPlease type what word(s) you hear "
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
            self.gui.setLabel("\n\n\n\n\n\n\n\nThank you for participating!"
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
        '''Sets the next sound based on the sequence type'''
        if (self.sequenceType == "LOADED"):
            self.currentSound = self.soundlib.playSequence(self.iterations)
        elif (self.sequenceType == "IN-ORDER" or self.sequenceType == "IN ORDER"):
            self.currentSound = self.soundlib.playInOrder(self.iterations)
        else:
            # Treat the sequenceType as random
            self.currentSound = self.soundlib.playRandom()
