'''
    Data object - handles data collection and writing to file
'''

class Data():
    '''Stores and manages participant data

    Attributes:
        participantID: Participant ID number (for anonymity)
        sessionID: The number of times the participant has done the experiment
        soundsPlayed: A list of the sounds that have played so far
        responses: A list of all participant responses this session
    '''
    def __init__(self, ID = "", session = ""):
        '''Constructor

        Args:
            ID (str): Participant ID number
            session (str): Session ID Number
        '''
        self.participantID = ID
        self.sessionID = session
        self.soundsPlayed = []
        self.responses = []
        self.latencies = []
        self.numRepetitions = []


    def add(self, sound, response, latency, soundLength):
        '''Adds a response to the database

        Args:
            sound (str): the sound that was played
            response (str): the participant's response'''
        self.soundsPlayed.append(sound)
        self.responses.append(response)
        self.latencies.append(latency)
        self.numRepetitions.append(int(round(latency / soundLength)))


    def recordData(self):
        '''Appends all collected data from the session to DATA.txt'''
        file = open("DATA.txt", "a")
        file.write("\nParticipant ID: %s" % self.participantID)
        file.write("\nSession ID: %s \n\n" % self.sessionID)

        for i in range(len(self.soundsPlayed)):
            file.write("Instance #%s: \n" % str(i+1))
            file.write("  Sound played: %s \n" % self.soundsPlayed[i])
            file.write("  Reported word(s): %s \n" % self.responses[i])
            file.write("  Response latency: %s secs\n" % self.latencies[i])
            file.write("  Number of loops: %s \n\n" % self.numRepetitions[i])

        file.write("-------------------------\n")
        file.close()
