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
from Configuracao_banco import *

def criacaoTables():

 
    i=0

    ini = time.time()
    
    arquivo_query='create table arquivo(Sistema varchar(100),data date,timeStamp varchar(100),Minuto time,Segundo time,elapsed int,label varchar(200),responseCode varchar(100),responseMessage varchar(900),threadName varchar(200),dataType varchar(100),success varchar(100),failureMessage varchar(100),bytes int,sentBytes int,grpThreads int,allThreads int,URL varchar(1000),Latency int,IdleTime int,Connect int);'
    arquivo_tabulado_query='create table arquivo_tabulado(Sistema varchar(100),data date,timeStamp bigint,Minuto time,Segundo time,elapsed int,label varchar(200),responseCode varchar(10),responseMessage varchar(900),threadName varchar(200),dataType varchar(50),success varchar(100),failureMessage varchar(50),bytes int,sentBytes int,grpThreads int,allThreads int,URL varchar(1000),Latency int,IdleTime int,Connect int);'
    tempos_de_resposta_query='create table tempos_de_resposta(hora time,Sistema varchar(50),elapsed int,label varchar(200),qtdlabel int,responseCode varchar(10),success varchar(100),qtdsuccess int,allThreads int,p95 float,p99 float);'

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
        
        print("")
        print("Tabela arquivo Criada")
        cursor.execute(arquivo_query)
        print("")
        print("Tabela arquivo_tabulado Criada")
        cursor.execute(arquivo_tabulado_query)
        print("")
        print("Tabela tempos de resposta Criada")
        cursor.execute(tempos_de_resposta_query)
        print("")
        
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
    
    criacaoTables()
    
    fim = time.time()
    
    tempo_total=(fim-ini)/60
    
    print("")
    print ("Tempo total (minutos): ", tempo_total)