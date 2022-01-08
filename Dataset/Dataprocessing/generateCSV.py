import sys
import os
import pandas as pd
from scapy.all import *
from obtainData import datafile

def list_dirs(path):
    # List all directories in the main directory "path"
    list_dirs = os.listdir(path)
    list_dirs.sort()
    list_d = []
    for q in list_dirs:
        subdir_path = os.path.join(path,q) + "/"
        list_d.append(subdir_path)	
    return list_d


def list_files(subdir_path):
    # List all files in the directory "subdir_path"
    list_files = []
    pcap_files = os.listdir(subdir_path)
    list_files.extend(map(lambda f: os.path.join(subdir_path, f), pcap_files))	
    return list_files


def dataframe_columns(d_f):
    # Get columns
    col = []
    col.append('name')
    col.append('label')
    length_paq = len(d_f)
    for ind in range(length_paq):
        col.append('feat#'+str(ind+1))
	
    return col


def getFilename(f):
    # Get filename
    file_name = os.path.basename(f)
    return file_name.split('.',1)[0]


def generateCSV(list_files, camera_ip):
    # Extract characteristics and generate CSV file
    csv_path = 'csv/'

    # COLUMNS
    d_f = datafile(list_files[0], camera_ip, 'standard') 
    df_cols = dataframe_columns(d_f)
    df_csv = pd.DataFrame(columns=df_cols)

    # ROWS 
    count = 1
    for f in list_files:
        # Iterate for all traffic captures
        print("Num: ", count,"/",len(list_files))
        try:	
            #Get the data -> Calling to 'obtainData'
            d_f = datafile(f, camera_ip, 'standard') 
                    
            label = 1 #0: No-Movement // 1: Movement        
            d_f.insert(0, label)
            
            file_name = getFilename(f)
            d_f.insert(0, file_name)
            try:
                # Insert the data in CSV file
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
	~Input arguments~
	#main_path: path with traffic captures
	#camera_ip: device IP address
	'''

	main_path = sys.argv[1]
	camera_ip = sys.argv[2]

	print('\Listing directories...')
	l_q = list_dirs(main_path)
	print('Directory List: ', l_q)

	print('\nListing files...')
	l_f = []
	for q in l_q:
		l_f.extend(list_files(q))
	print('File List: ', l_f)

	print('\nGenerating CSV...')
	generateCSV(l_f, camera_ip)
	print('Generated CSV file.')


if __name__ == "__main__":
		main()  
