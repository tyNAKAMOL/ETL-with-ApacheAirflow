import pandas as pd
import glob2
from sqlalchemy import create_engine

if(__name__=="__main__"):
    folder_path = '/opt/airflow/data/source'
    dataFrame = []
    first_file = True
    for file_path in glob2.glob(f'{folder_path}/raw*.csv'):
        if first_file is True:
            df = pd.read_csv(file_path,sep="|",header=0)
            first_file = False
        else:
            df = pd.read_csv(file_path,skiprows=0,sep="|",)
        dataFrame.append(df)

    merged_df = pd.concat(dataFrame)
    engine = create_engine('postgresql://local:password@postgresLocal:5432/dataPeople', echo=False) #postgresql://username:password@host:port/database
    merged_df.to_sql('source_data', con = engine, if_exists='replace',index_label='id')

# merged_df.to_csv("/opt/airflow/data/sourceFile.csv", index=False)
