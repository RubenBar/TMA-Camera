import sys
import os 
from datetime import datetime
import subprocess

def tcpdump(dir_query, time, type_mov, device_ip, iterations):
        #Captura el trafico de red 
        for i in range(iterations):
            print('Capturando paquetes...')
            capture = subprocess.Popen("sudo timeout " + str(time) + " tcpdump -i wlan0 -n host " + str(
                device_ip) + " -w " + dir_query + type_mov + str(i) + ".pcap", shell=True, stdout=subprocess.PIPE)                      
            capture.wait()        
            print('Captura de paquetes finalizado')


def generateDirectory():
        #Crear los directorios donde las capturas de trafico seran guardadas
        now = datetime.now()
        dt_str = now.strftime("%d%m%Y-%H%M%S")
        
	path_dir = 'pcap/' + dt_str
	if not os.path.exists(path_dir):
		os.mkdir(path_dir)
	return path_dir + '/'


def main():
        print('\n######################################################')
        print('##                                                  ##')
        print('##              CAPTURE PACKETS                     ##')
        print('##                                                  ##')
        print('######################################################\n')
        
        '''
        ~Argumentos de entrada~
        #camera_ip: direccion IP dispositivo IoT
        #itr: numero de capturas de trafico. (-1) inf
        #time: intervalo de captura de trafico (segundos)
        #mov: movimiento (1) sin movimiento (0)
        '''
        if len(sys.argv) < 4:
                print "Usage: captureDataCamera.py <camera_ip> <itr> <time> <mov>"
                return 1
                
        #Variables        
        camera_ip = sys.argv[1]
        itr = int(sys.argv[2])	
        time = int(sys.argv[3])
        mov = int(sys.argv[4])
        
        type_mov = ""
        if mov == 1:
               type_mov = "mov" 
        elif mov == 0:
                type_mov = "no_mov"
        else:
                return

        
        #Preparacion         
        path = generateDirectory()
        tcpdump(path, time, type_mov, camera_ip, itr)      


if __name__ == "__main__":
		main()  
