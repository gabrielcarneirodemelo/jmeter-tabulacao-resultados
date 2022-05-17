#!/usr/bin/python
#coding: utf-8

import pandas as pd
import numpy
import time
import os
from datetime import datetime
pd.options.mode.chained_assignment = None  # default='warn'
import psycopg2
from psycopg2 import Error
import re
import pandas.io.sql as sqlio
from Configuracao_banco import *

def tabulacaoNoBanco():
    
    i=0
    sql='select * from arquivo'
    insert = "INSERT INTO arquivo_tabulado(sistema,data,timestamp,minuto,segundo,elapsed,label,responsecode,responsemessage,threadname,datatype,success,failuremessage,bytes,sentbytes,grpthreads,allthreads,url,latency,idletime,connect) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
   
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database="Arquivo_sem_tabular")




        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        #print("PostgreSQL server information")
        #print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        #cursor.execute("select * from arquivo_csv;")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
        
    
        
        arquivo = sqlio.read_sql_query(sql, connection)
        
        for row in arquivo['timestamp']:
            arquivo['data'][i] = datetime.fromtimestamp(int(row)/1000).strftime("%d/%m/%Y %H:%M:%S")
            i=i+1

        for index, row in arquivo.iterrows():
            cursor.execute(insert, (str(row.sistema),row.data,row.timestamp,row.data, row.data,row.elapsed, str(row.label),str(row.responsecode), str(row.responsemessage), str(row.threadname), str(row.datatype), str(row.success), str(row.failuremessage),row.bytes, row.sentbytes, row.grpthreads, row.allthreads, str(row.url), row.latency, row.idletime, row.connect))

        connection.commit()
        
        

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
                
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

if __name__ == "__main__":


    ini = time.time()
    
    tabulacaoNoBanco()
    
    fim = time.time()
    
    tempo_total=(fim-ini)/60
    
    print("")
    print ("Tempo total (minutos): ", tempo_total)