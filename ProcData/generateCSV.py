import sys
import os
import pandas as pd
from scapy.all import *
from obtainData import datafile

def list_queries(path):
    #Lista todas las preguntas del directorio "path"
    list_queries = os.listdir(path)
    list_queries.sort()
    list_q = []
    for q in list_queries:
        query_path = os.path.join(path,q) + "/"
        list_q.append(query_path)	
    return list_q


def list_files(query_path):
    #Lista todos los ficheros del directorio "query_path"
    list_files = []
    q_files = os.listdir(query_path)
    list_files.extend(map(lambda f: os.path.join(query_path, f), q_files))	
    return list_files
    
   
def dataframe_columns(d_f):
    #Obtener las columnas 
    col = []
    col.append('query')
    col.append('label')
    length_paq = len(d_f)
    for ind in range(length_paq):
        col.append('feat#'+str(ind+1))
	
    return col
        
        
def getFilename(f):
    #Obtener el nombre del fichero 
    file_name = os.path.basename(f)
    return file_name.split('.',1)[0]
      
      
def generateCSV(list_files, camera_ip):
    #Extraer caracteristicas y generar Cfichero SV 
    csv_path = 'csv/'
    
    #COLUMNAS
    d_f = datafile(list_files[0], camera_ip) 
    df_cols = dataframe_columns(d_f)
    df_csv = pd.DataFrame(columns=df_cols)

    #FILAS   
    count = 1
    for f in list_files:
        print("Num: ", count,"/",len(list_files))
        try:	
            d_f = datafile(f, camera_ip) 
                    
            label = 0 #0: No-Movimiento // 1: Movimiento        
            d_f.insert(0, label)
            
            query_name = getFilename(f)
            d_f.insert(0, query_name)
            try:
                df_csv.loc[-1] = d_f
                df_csv.index = df_csv.index + 1
                count = count + 1 
            except:
                print('Error')
        except:
            print('Error') 

    df_csv.to_csv(csv_path + "data.csv", index=False)


def main():
	print('\n######################################################')
	print('##                                                  ##')
	print('##              PROCESS DATA                        ##')
	print('##                                                  ##')
	print('######################################################\n')
    
	'''
	~Argumentos de entrada~
	#main_path: dpath del CSV con el listado de comandos de voz. 
	#camera_ip: direccion IP dispositivo Amazon Echo
	'''
    
	main_path = sys.argv[1]
	camera_ip = sys.argv[2]
	
	print('\nListando directorios...')
	l_q = list_queries(main_path)
	print('Lista de directorios: ', l_q)

	l_f = []
	for q in l_q:
		l_f.extend(list_files(q))
	print('Lista de ficheros: ', l_f)
		
	print('\nGenerando CSV...')
	generateCSV(l_f, camera_ip)
	print('Fichero CSV generado.')


if __name__ == "__main__":
		main()  
