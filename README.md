verbal-summator
===============
![version](https://img.shields.io/github/release/s-pangburn/verbal-summator.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*Implemented in Python 2.7, requires PyGame for cross-platform sound support*

This repository is a framework that is being used for Psychology experiments at the University of the Pacific.

The experiments surround some undeveloped theories proposed by B.F. Skinner early on in his career. It is still in active development, and is not working as intended yet.

In the end, the hope for this project is making the source easily accessible in order to encourage more experiments along these lines.

## Setup

**Make sure you are running Python 2.7**

After cloning the repository, navigate to the directory in your terminal and run `pip install -r requirements.txt`

Once that's finished, navigate to the parent directory of the `verbal-summator` folder and run `python verbal-summator`.

### IMPORTANT FILES

Name | Description
----------|-----------
SOUNDS/ | All sounds for sequencing and playback will be chosen from this folder. Just place all sound files here. **Only .wav and .ogg files are supported at this time.**
INTRO.txt | Contains text for the first prompt the participant will see.
DATA.txt | Will contain all data output from the session.
SEQUENCE.txt | Sample file for specifying a sound sequence. **NOTE: The sequence is specified according to the absolute number of the file in the folder (The first file is "1", second is "2", etc.) This was by request.**

<br>Any questions can be mailed to Stephen Pangburn at stephen.pangburn.ii@gmail.com
