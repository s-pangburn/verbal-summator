'''
    Sound Library class - imports sounds and stores them for later use
'''
import os
import winsound
import random

class SoundLibrary():
    def __init__(self):
        self.sounds = [ f for f in os.listdir("sounds") if f.endswith(".wav") ]
        self.totalSounds = len(self.sounds)
        self.sequence = []

    def loadSequence(self, filename):
        if not filename.endswith(".txt"):
            filename = filename + ".txt"
        file = open(filename)
        self.sequence = file.readlines()
        self.sequence = [int(i) for i in self.sequence]  #Convert the data to integer values
        file.close()

    def playRandom(self):
        return (self.play(random.randrange(self.totalSounds)))

    def playSequence(self, rand, i):
        if rand or i >= len(self.sequence):
            x = self.sequence[random.randrange(len(self.sequence))]
        else:
            x = i
        return (self.play(x))

    def play(self, number):
        winsound.PlaySound('Sounds\\%s' % self.sounds[number], winsound.SND_FILENAME)
                            #| winsound.SND_ASYNC | winsound.SND_LOOP)
        return self.sounds[number]
    
    def stopAllSounds(self):
        winsound.PlaySound(None, winsound.SND_FILENAME)