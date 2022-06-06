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
import psycopg2.extras
from Configuracao_banco import *

def insercaoNoBanco():

 
    i=0

    ini = time.time()
    
    insert = "INSERT INTO arquivo(Sistema,timeStamp,elapsed,label,responseCode,responseMessage,threadName,dataType,success,failureMessage,bytes,sentBytes,grpThreads,allThreads,URL,Latency,IdleTime,Connect) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="postgres",
                              password="123456",
                              host="localhost",
                              port="5432",
                              database="Arquivo_sem_tabular")




        # Create a cursor to perform database operations
        cursor = connection.cursor()
        
        cursor.execute("SELECT version();")
    
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

        for chunk in pd.read_csv(arquivo, chunksize=5000):
 
            chunk.insert(0, "Sistema", sistema)
        
            
            
                
            for index, row in chunk.iterrows():
                vals = [(str(row.Sistema),row.timeStamp,row.elapsed, str(row.label),row.responseCode, str(row.responseMessage), str(row.threadName), str(row.dataType), str(row.success), str(row.failureMessage),row.bytes, row.sentBytes, row.grpThreads, row.allThreads, str(row.URL), row.Latency, row.IdleTime, row.Connect)]
                psycopg2.extras.execute_batch(cursor,insert,vals)
            connection.commit()
    

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")       



if __name__ == "__main__":

    for file in os.listdir('.'):
        if file.endswith('.csv'):
            arquivo=file
            
    print("Nome do arquivo selecionado: ",arquivo)     
    
    print("")
    
    sistema = input("Entre com o nome do sistema testado: ")
   
    print("")
    
    ini = time.time()
    
    insercaoNoBanco()
    
    fim = time.time()
    
    tempo_total=(fim-ini)/60
    
    print("")
    print ("Tempo total (minutos): ", tempo_total)