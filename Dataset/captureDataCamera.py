import sys
import os
from datetime import datetime
import subprocess

def tcpdump(dir_query, time, type_mov, device_ip, iterations):
        # Capture network traffic
        for i in range(iterations):
            print('Capturing packets...')
            capture = subprocess.Popen("sudo timeout " + str(time) + " tcpdump -i wlan0 -n host " + str(
                device_ip) + " -w " + dir_query + type_mov + str(i) + ".pcap", shell=True, stdout=subprocess.PIPE)
            capture.wait()
            print('Packet Capture Completed')


def generateDirectory():
        # Create the directories where the traffic captures will be saved
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
        ~Input arguments~
        #camera_ip: IoT device IP address
        #itr: number of traffic captures. (-1) inf
        #time: traffic capture interval (seconds)
        #mov: movement (1) no-movement (0)
        '''
        if len(sys.argv) < 4:
                print("Usage: captureDataCamera.py <camera_ip> <itr> <time> <mov>")
                return 1

        # Variables
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

        # Preparation
        path = generateDirectory()
        tcpdump(path, time, type_mov, camera_ip, itr)


if __name__ == "__main__":
		main()  
