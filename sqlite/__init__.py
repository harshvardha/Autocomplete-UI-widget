import os
import sys
DIRECTORY = None
if(getattr(sys,"frozen",False)):
    DIRECTORY = os.path.join(os.path.dirname(sys.executable),"autoComplete")
else:
    DIRECTORY = os.path.join(__file__)
#autoCompleteAlgorithm = os.path.join(DIRECTORY,"autoCompleteAlgorithm")
#databaseManager = os.path.join(DIRECTORY,"databaseManager")
#wordDictionary = os.path.join(DIRECTORY,"wordDictionary")
