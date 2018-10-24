'''
    Sound Library class - imports sounds and stores them for later use
'''
import os
import winsound
import random
import tkMessageBox
from pygame import mixer

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
        currentPath = os.path.dirname(os.path.realpath(__file__))
        self.sounds = [ f for f in os.listdir(currentPath + "\..\sounds") if f.endswith(".wav") or f.endswith(".ogg")]
        self.totalSounds = len(self.sounds)
        self.currentSound = None
        self.sequence = []

        mixer.init(buffer=1024)  # Smaller buffer size prevents lag

    def loadSequence(self, filename):
        '''Store a sequence of sounds from file into the list soundlib.sequence.
            NOTE that this assumes the sequence is written according to the file's
            numerical value

        Args:
            filename (str): the name of the file to be loaded
        '''
        if not filename.endswith(".txt"):
            filename = filename + ".txt"
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            f = open(dir_path + "/../" + filename)
            self.sequence = f.readlines()
            self.sequence = [(int(i) - 1) for i in self.sequence]  # Convert the data to integer values
            if len(self.sequence) == 0:
                tkMessageBox.showwarning(' ', "The specified sequence is empty.")
            name = f.name
            f.close()
            return name

        except IOError:
            tkMessageBox.showwarning(' ', "The specified file (%s) does not "
                                    "exist." % filename)

    def getCurrentSoundLength(self):
        if self.currentSound == None: return
        return self.currentSound.get_length()

    def playRandom(self):
        '''Play a random sound from the loaded sequence

        If a sequence has not been loaded through loadSequence(), the default
        sound folder is used.
        '''
        return (self.play(random.randrange(self.totalSounds)))

    def playInOrder(self, i):
        '''Play the sounds in the order they show up in the folder

        If the number of iterations passes the number of sounds, the sounds will
        be played randomly.
        '''
        if i >= self.totalSounds:
            return self.playRandom()
        else:
            return self.play(i)

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
            snd = self.sounds[self.sequence[x]]  # Gets the sound filename
            index = self.sounds.index(snd)  # Finds the index of the sound
        except ValueError:
            tkMessageBox.showwarning(' ', "Sequence specified a sound (%s) that "
                                          "did not exist." % (self.sounds[self.sequence[x]]))
            snd = 0
        return (self.play(index))

    def play(self, number):
        '''Plays the sound at the specified index in the loaded list

        Args:
            number (int): The index of the sound to be played
        '''
        currentPath = os.path.dirname(os.path.realpath(__file__))
        # winsound.PlaySound(currentPath + '\sounds\\%s' % self.sounds[number],
        #                    winsound.SND_FILENAME | winsound.SND_ASYNC |
        #                    winsound.SND_LOOP)
        self.currentSound = mixer.Sound(currentPath + '\..\sounds\\%s' % self.sounds[number])
        self.currentSound.play(loops=-1)
        return self.sounds[number]

    def stopAllSounds(self):
        '''Stops all sounds that are currently playing'''
        # winsound.PlaySound(None, winsound.SND_FILENAME)
        mixer.stop()
