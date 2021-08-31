import psycopg2, psycopg2.extras




DB = 'masivo_sitp'
USER = 'postgres'
PORT =5432
PASSWORD = '4ng3lDS4A*83'
HOST='ds4a-83rds2.ckmtgfcimlii.us-east-2.rds.amazonaws.com'
#######################################CONECTION DATA######################################################################
def conn():
    conn = psycopg2.connect(database=DB,user=USER,password=PASSWORD,host=HOST, port=PORT)
    return conn