from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount
import psycopg2
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.utils.dates import days_ago
from airflow.providers.docker.operators.docker import DockerOperator
# from transform import transform
# from load import load

# from test import my_function,func_test

# import pandas as pd
# import glob
# import re


# def connectionDB ():
    # connect = psycopg2.connect(
    #     host='postgresLocal',
    #     database='dataPeople',
    #     user='local',
    #     password='password',
    #     port='5432'
    # )    
    # cur=connect.cursor()
    # cur.execute('CREATE TABLE IF NOT EXISTS detail3 (userid SERIAL PRIMARY KEY, firstname varchar(40), lastname varchar(40), age integer, sex varchar(15));')
    # cur.execute('CREATE TABLE temp_table3 (firstname varchar(40), lastname varchar(40), age integer, sex varchar(15));')
    # cur.execute("COPY temp_table3 FROM '/app/airflow/finalFile.csv' DELIMITER ',' CSV HEADER;")
    # cur.execute("INSERT INTO detail3 (firstname, lastname, age, sex) SELECT firstname, lastname, age, sex FROM temp_table;")
    # connect.commit()
    # cur.close()
    # connect.close()


with DAG(
        dag_id='my_dag', #name
        start_date=days_ago(0),
        schedule_interval="@daily",
        tags=["Test"]
) as dag:

    #connection with python
    # connectDB = PythonOperator(
    #     task_id='python_connectDB',
    #     python_callable=connectionDB,
    # )
    # connectDB

    #connection with PostgresOperator
    # create_table = PostgresOperator(
    #     task_id="detail",
    #     postgres_conn_id="connectPostges",
    #     sql="""
    #         CREATE TABLE IF NOT EXISTS detail2 (
    #         userid SERIAL PRIMARY KEY,
    #         firstname varchar(40),       
    #         lastname  varchar(40),
    #         age   integer,
    #         sex   varchar(15)
    #         )
    #       """
    # )
    # create_tempTable = PostgresOperator(
    #     task_id="temp_table",
    #     postgres_conn_id="connectPostges",
    #     sql="""
    #         CREATE TABLE temp_table (
    #         firstname varchar(40),       
    #         lastname  varchar(40),
    #         age   integer,
    #         sex   varchar(15)
    #         )
    #     """
    # )
    # copy_table = PostgresOperator(
    #     task_id='copy_table',
    #     postgres_conn_id='connectPostges',  # ชื่อ connection ของ PostgreSQL ใน Airflow
    #     sql="COPY temp_table FROM '/app/airflow/finalFile.csv' DELIMITER ',' CSV HEADER;",
    # )
    # insert_data = PostgresOperator(
    #     task_id='insert_data',
    #     postgres_conn_id='connectPostges',  # ชื่อ connection ของ PostgreSQL ใน Airflow
    #     sql="INSERT INTO detail2 (firstname, lastname, age, sex) SELECT firstname, lastname, age, sex FROM temp_table;",
    # )
    # create_table >> create_tempTable >> copy_table >> insert_data

    # task1 = BashOperator(
    #     task_id='Hello',
    #     bash_command='python /app/docker/Hello.py',
    #     dag=dag,
    # )

    task1 = DockerOperator(
    task_id='extract',
    image='my_etl:extract',
    container_name='extract',
    api_version='auto',
    network_mode="airflow_default",
    mount_tmp_dir = False,
    mounts=[Mount(source="C:/Users/beaut/Documents/Airflow/data/source",target="/opt/airflow/data/source",type="bind")],
    docker_url='tcp://docker-proxy:2375',
    command='python extract.py',
    auto_remove=True,
)
    
    task2 = DockerOperator(
    task_id='transform',
    image='my_etl:transform',
    container_name='transform',
    api_version='auto',
    network_mode="airflow_default",
    mount_tmp_dir = False,
    docker_url='tcp://docker-proxy:2375',
    command='python transform.py',
    auto_remove=True,
)
    task3 = DockerOperator(
    task_id='load',
    image='my_etl:load',
    container_name='load',
    api_version='auto',
    network_mode="airflow_default",
    mount_tmp_dir = False,
    docker_url='tcp://docker-proxy:2375',
    command='python load.py',
    auto_remove=True,
)
    # task1 = BashOperator(
    #     task_id='Extract',
    #     bash_command='python /opt/airflow/dags/extract.py',
    #     dag=dag,
    # )
    # task2 = BashOperator(
    #     task_id='Transform',
    #     bash_command='python /opt/airflow/dags/transform.py',
    #     dag=dag,
    # )
    # task3 = BashOperator(
    #     task_id='Load',
    #     bash_command='python /opt/airflow/dags/load.py',
    #     dag=dag
    # )
    # task1
    task1 >> task2 >> task3

