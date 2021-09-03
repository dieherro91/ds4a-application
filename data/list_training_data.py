
#In this file are the functions releated to the training data.

import os
from pages import homes
from pickle import load
import gzip

#This function compere the list of routes from de database an the route files in the trainnin_data folder
def list_routes_available_predictc(ZoneValue):
    DATA_DIR = os.getcwd()
    sav_path = os.path.join(os.path.join(DATA_DIR, "data"), "trainning_data")
    list_files=[]
    list_files=os.listdir(sav_path)

    list_files_available=[]
    for item in list_files:
        if (item!= '.gitignore' and item != '__init__.py' and item != '__init__.py'):
            list_files_available.append(item[:-8])
    
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


#this function return a list with the predicted passengers from the "df" information for the "route" selected
def prediction_evaluation(df,route):
    DATA_DIR = os.getcwd()
    sav_path = os.path.join(os.path.join(os.path.join(DATA_DIR, "data"), "trainning_data"),route+'.json.gz')
    with gzip.open(sav_path, 'rb') as sav_file:
        randon_forest_model = load(sav_path)
    
    list_output_prediction=randon_forest_model.predict(df)
    return list_output_prediction

#