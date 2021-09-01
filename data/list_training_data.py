
#In this file are the functions releated to the training data.

import os
from pages import homes
from joblib import load

def list_routes_available_predictc(ZoneValue):
    DATA_DIR = os.getcwd()
    sav_path = os.path.join(os.path.join(DATA_DIR, "data"), "trainning_data")
    list_files=[]
    list_files=os.listdir(sav_path)

    list_files_available=[]
    for item in list_files:
        if (item!= '.gitignore' and item != '__init__.py'):
            list_files_available.append(item[:-4])
    
    list_db=homes.wer[ZoneValue]
    list_routes_db=[]
    
    for item in list_db:
        list_routes_db.append(item['label'])

    final_list=list(set(list_routes_db) & set(list_files_available))

    list_drop_route=[]
    for item in final_list:
        list_drop_route.append({'label': item , 'value': item})
    
    if (list_drop_route==[]):
        list_drop_route.append({'label': 'Zone not available' , 'value': 'Zonenot available'})
        return list_drop_route

    return list_drop_route