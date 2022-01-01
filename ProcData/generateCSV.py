import sys
import os
import pandas as pd
from scapy.all import *
from obtainData import datafile

def list_dirs(path):
    #Lista todos los directorios del directorio main "path"
    list_dirs = os.listdir(path)
    list_dirs.sort()
    list_d = []
    for q in list_dirs:
        subdir_path = os.path.join(path,q) + "/"
        list_d.append(subdir_path)	
    return list_d


def list_files(subdir_path):
    #Lista todos los ficheros del directorio "subdir_path"
    list_files = []
    pcap_files = os.listdir(subdir_path)
    list_files.extend(map(lambda f: os.path.join(subdir_path, f), pcap_files))	
    return list_files
    
   
def dataframe_columns(d_f):
    #Obtener las columnas 
    col = []
    col.append('name')
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
    #Extraer caracteristicas y generar fichero CSV 
    csv_path = 'csv/'
    
    #COLUMNAS
    d_f = datafile(list_files[0], camera_ip, 'standard') 
    df_cols = dataframe_columns(d_f)
    df_csv = pd.DataFrame(columns=df_cols)

    #FILAS   
    count = 1
    for f in list_files:
        #Iterar por todas las capturas de trafico
        print("Num: ", count,"/",len(list_files))
        try:	
            #Obtener los datos -> llamada a obtainData
            d_f = datafile(f, camera_ip, 'standard') 
                    
            label = 1 #0: No-Movimiento // 1: Movimiento        
            d_f.insert(0, label)
            
            file_name = getFilename(f)
            d_f.insert(0, file_name)
            try:
                #Insertar los datos en el CSV
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
	#main_path: path con las capturas de trafico  
	#camera_ip: direccion IP dispositivo
	'''
    
	main_path = sys.argv[1]
	camera_ip = sys.argv[2]
	
	print('\nListando directorios...')
	l_q = list_dirs(main_path)
	print('Lista de directorios: ', l_q)

	print('\nListando ficheros...')
	l_f = []
	for q in l_q:
		l_f.extend(list_files(q))
	print('Lista de ficheros: ', l_f)
		
	print('\nGenerando CSV...')
	generateCSV(l_f, camera_ip)
	print('Fichero CSV generado.')


if __name__ == "__main__":
		main()  
