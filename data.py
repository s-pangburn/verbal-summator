'''
    Data object - handles data collection and writing to file
'''

class Data():
    def __init__(self, ID = "", session = ""):
        self.participantID = ID
        self.sessionID = session
        self.soundsPlayed = []
        self.responses = []
        

    def add(self, sound, response):
        self.soundsPlayed.append(sound)
        self.responses.append(response)
    

    def recordData(self):
        file = open("Data.txt", "a")
        file.write("\nParticipant ID: %s" % self.participantID)
        file.write("\nSession ID: %s \n\n" % self.sessionID)
        for i in range(len(self.soundsPlayed)):
            file.write("Instance #%s: \n" % str(i+1))
            file.write("  Sound played: %s \n" % self.soundsPlayed[i])
            file.write("  Reported word(s): %s \n\n" % self.responses[i])
        file.write("-------------------------\n")
        file.close()

