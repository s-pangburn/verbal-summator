'''
Verbal Summator - Python Edition

@author: Stephen Pangburn II
'''

import random
from gui import Slide

def main():
    
    random.seed()
    
    session = Slide(None)
    session.focus_set()
    session.mainloop()
    
    print("Ran the application.")

if __name__ == "__main__":
    main()