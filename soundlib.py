'''
    Sound Library class - imports sounds and stores them for later use
'''
import os
import winsound
import random
import tkMessageBox

class SoundLibrary(object):
    
    '''Manages sound loading, sequencing, and playback
    
    Attributes:
        sounds: A list of the sounds loaded from the SOUNDS folder
        totalSounds: The total number of sounds loaded
        sequence: A list of the index numbers of the sounds in the loaded 
                  sequence (if any)
    '''
    
    def __init__(self):
        '''Loads sounds from folder and initializes attributes'''
        self.sounds = [ f for f in os.listdir("sounds") if f.endswith(".wav") ]
        self.totalSounds = len(self.sounds)
        self.sequence = []

    def loadSequence(self, filename):
        '''Store a sequence of sounds from f into the list soundlib.sequence
        
        Args:
            filename (str): the name of the f to be loaded
        '''
        if not filename.endswith(".txt"):
            filename = filename + ".txt"
        f = open(filename)
        self.sequence = f.readlines()
        self.sequence = [int(i) for i in self.sequence]  #Convert the data to integer values
        f.close()

    def playRandom(self):
        '''Play a random sound from the loaded sequence
        
        If a sequence has not been loaded through loadSequence(), the default 
        sound folder is used.
        '''
        return (self.play(random.randrange(self.totalSounds)))

    def playSequence(self, i):
        '''Play sounds in the order of the loaded sequence
        
        If the sequence ends or no sequence has been loaded, the available 
        sounds are played at random.
        
        Args:
            i (int): The current iteration for data collection
        '''
        if len(self.sequence) == 0 or i >= len(self.sequence):
            x = self.sequence[random.randrange(len(self.sequence))]
        else:
            x = i
        try:
            snd = self.sounds.index(self.sequence[x])
        except ValueError:
            tkMessageBox.showwarning(' ', "Sequence specified a sound (%s) that"
                                          "did not exist." % (self.sequence[x]))
            snd = 0
        return (self.play(snd))

    def play(self, number):
        '''Plays the sound at the specified index in the loaded list
        
        Args:
            number (int): The index of the sound to be played
        '''
        winsound.PlaySound('Sounds\\%s' % self.sounds[number], 
                           winsound.SND_FILENAME | winsound.SND_ASYNC | 
                           winsound.SND_LOOP)
        return self.sounds[number]
    
    def stopAllSounds(self):
        '''Stops all sounds that are currently playing'''
        winsound.PlaySound(None, winsound.SND_FILENAME)