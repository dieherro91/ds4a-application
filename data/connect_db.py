import psycopg2, psycopg2.extras
import pandas as pd



DB = 'masivo_sitp_3'
USER = 'postgres'
PORT =5432
PASSWORD = '4ng3lDS4A*83'
HOST='ds4a-83rds.ckmtgfcimlii.us-east-2.rds.amazonaws.com'
#######################################CONECTION DATA######################################################################
def conn():
    conn = psycopg2.connect(database=DB,user=USER,password=PASSWORD,host=HOST, port=PORT)
    return conn
#######################################sidebar dropdown ######################################################################
 