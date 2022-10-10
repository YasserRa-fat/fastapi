import sys
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app.calculations import add

def test_add():
    print("testing function")
     
    assert  add(1,2) == 3
    
    