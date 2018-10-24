'''
Verbal Summator - Python Edition

@author: Stephen Pangburn II
'''
import sys
sys.path.insert(0, r'/lib')

import random
from lib.session import Session

def main():
    random.seed()

    session = Session()
    session.start()

if __name__ == "__main__":
    main()