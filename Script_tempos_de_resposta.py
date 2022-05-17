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

def temposDeResposta():

 
    i=0
    sql = """select TO_CHAR(TO_TIMESTAMP(timestamp / 1000), 'HH24:MI:SS') as "hora",TO_CHAR(TO_TIMESTAMP(timestamp / 1000), 'dd/mm/yyyy') as "dia", sistema, avg(elapsed) as "elapsed", label, count(label) as "qtdlabel", responsecode, success, count(success) as "qtdsuccess", max(allthreads) as "allthreads", percentile_disc(0.95) within group (order by arquivo_tabulado.elapsed) as "p95", percentile_disc(0.99) within group (order by arquivo_tabulado.elapsed) as "p99" from arquivo_tabulado where sistema = '"""+sistema+"""' group by dia,hora,sistema,responsecode,label,success;"""
    
    insert = "INSERT INTO tempos_de_resposta(hora,sistema,elapsed,label,qtdlabel,responsecode,success,qtdsuccess,allthreads,p95,p99) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    
    print(sistema)
    

    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database="Arquivo_sem_tabular")




        # Create a cursor to perform database operations
        cursor = connection.cursor()
        
        cursor.execute("SELECT version();")
    
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
        
                
        arquivo = sqlio.read_sql_query(sql, connection)
        

        for index, row in arquivo.iterrows():
            cursor.execute(insert, (row.hora, str(row.sistema),row.elapsed, str(row.label),row.qtdlabel,row.responsecode, str(row.success), row.qtdsuccess, row.allthreads, row.p95, row.p99))
            connection.commit()
    

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")       



if __name__ == "__main__":
  
    sistema = input("Entre com o nome do sistema testado: ")
   
    print("")
            
    ini = time.time()
    
    temposDeResposta()
    
    fim = time.time()
    
    tempo_total=(fim-ini)/60
    
    print("")
    print ("Tempo total (minutos): ", tempo_total)