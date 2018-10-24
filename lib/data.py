'''
    Data object - handles data collection and writing results to file
'''
import os
import csv

class Data():
    '''Stores and manages participant data

    Attributes:
        participantId: Participant ID number (for anonymity)
        sessionId: The number of times the participant has done the experiment
        soundsPlayed: A list of the sounds that have played so far
        responses: A list of all participant responses this session
    '''
    def __init__(self, id = "", session = ""):
        '''Constructor

        Args:
            ID (str): Participant ID number
            session (str): Session ID Number
        '''
        self.participantId = id
        self.sessionId = session
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
        '''Appends all collected data from the session to DATA.csv'''
        dir_path = os.path.dirname(os.path.realpath(__file__))
        needs_header = True if os.path.isfile(dir_path + '/../DATA.csv') == 0 else False

        with open(dir_path + '/../DATA.csv', 'ab') as csv_file:
            fieldnames = [
                'Participant ID', 
                'Session ID', 
                'Iteration',
                'Sound File', 
                'Reported Words', 
                'Latency (secs)', 
                'Number of Loops'
                ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if needs_header: writer.writeheader()
            
            for i in range(len(self.soundsPlayed)):
                writer.writerow({
                    'Participant ID': self.participantId, 
                    'Session ID': self.sessionId, 
                    'Iteration': i + 1,
                    'Sound File': self.soundsPlayed[i], 
                    'Reported Words': self.responses[i], 
                    'Latency (secs)': self.latencies[i], 
                    'Number of Loops': self.numRepetitions[i]
                    })
