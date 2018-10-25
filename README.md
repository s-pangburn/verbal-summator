verbal-summator
===============
![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)
![version](https://img.shields.io/github/release/s-pangburn/verbal-summator.svg?colorB=brightgreen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository is a framework that is being used for Psychology experiments at the University of the Pacific.

The experiments surround some undeveloped theories proposed by psychologist B.F. Skinner early on in his career regarding [verbal summation](http://psycnet.apa.org/record/1936-04586-001) and the measurement of verbal behavior. However, the original experiment was conducted using recordings painstakingly timed on a phonograph, quite outdated technology by modern standards.

The hope for this project is to modernize Skinner's original methodology, making the source easily accessible so that more experiments along these lines can be conducted and adjusted with relative ease.

## Setup

**Make sure you are running Python 2.7**

After cloning the repository, navigate to the directory in your terminal and run `pip install -r requirements.txt`

Once that's finished, navigate to the parent directory of the `verbal-summator` folder and run `python verbal-summator`.

### IMPORTANT FILES

Name | Description
----------|-----------
SOUNDS/ | All sounds for sequencing and playback will be chosen from this folder. Just place all sound files here. **Only .wav and .ogg files are supported at this time.**
CONFIG.yml | Allows you to tweak the constraints of the experiment (number of reps, order of sounds, etc.) If options are not provided here, the program will prompt you for them.
INTRO.txt | Contains text for the first prompt the participant will see.
DATA.csv | Will contain all data output from the session exported in spreadsheet (CSV) format. Compatible with both Google Sheets and Microsoft Excel.
SEQUENCE.txt | Sample file for specifying a sound sequence. **NOTE: The sequence is specified according to the absolute number of the file in the folder (The first file is "1", second is "2", etc.) This was by request.**

<br>Any questions can be mailed to Stephen Pangburn at stephen.pangburn.ii@gmail.com
