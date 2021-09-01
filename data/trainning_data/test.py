
import os
import joblib


DATA_DIR = os.getcwd()
route='Z12'
sav_path = os.path.join(os.path.join(os.path.join(DATA_DIR, "data"), "trainning_data"),route+'.sav')

clf = load(sav_path) 
print(clf)

import sys

print(sys.path)


