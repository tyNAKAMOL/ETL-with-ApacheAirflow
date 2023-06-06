import pandas as pd
from sqlalchemy import create_engine


# def connectionDB():
# host='postgresLocal',
# database='dataPeople',
# user='local',
# password='password',
# port='5432'
if(__name__=="__main__"):
    engine = create_engine('postgresql://local:password@postgresLocal:5432/dataPeople', echo=False) #postgresql://username:password@host:port/database
        # return engine
    # df = pd.read_csv('/opt/airflow/data/stagingFile.csv')
    df = pd.read_sql_table('stating_data',con = engine,schema="public",columns=["First Name","Last Name","Age","Sex"])
    df.to_sql('final_data', con = engine, if_exists='replace',index_label='id')

# df.to_csv("/opt/airflow/data/finalFile.csv", index=False) 

