import sys
from pathlib import Path
import pandas as pd
from scapy.all import *

def pcap_converter(pcap_path, echo_ip):
    l_server_ip = ["8.211.20.145", "192.168.1.41", "192.168.1.62"]
    csv_path = 'csv/'
    pcap_file = Path(pcap_path)
    pcap_name = pcap_file.name[0:-5]
    p_list = rdpcap(pcap_path)

    # In this section we indicate the "features" that we are going to use. In this case we have 3 features:
    ####time -> Time between packets
    ####size -> IP frame size
    ####direction -> The address of the packet (outgoing = 1 // incoming = -1)
    echo_df = pd.DataFrame(columns=['time', 'size', 'direction'])

    p_list.reverse()
    echo_packets = []
    for p in p_list:
        # In this section we eliminate those packets that we do not want to show in the CSV file
        # In this case, all TCP packets
        try:
            p[IP].src
            p[UDP]
        except:
            continue
        if (p[IP].src.strip() == echo_ip.strip() or p[IP].dst.strip() == echo_ip.strip()) and (p[IP].src.strip() in l_server_ip or p[IP].dst.strip() in l_server_ip):
            if p[UDP] and p.len < 60: #filter low size packets
                continue
            else:
                echo_packets.append(p)
    p_list = echo_packets

    init_time = p_list[-1].time
    listData = []
    for p in p_list:
        time = p.time - init_time

        if p[IP].src == echo_ip:
            direct = 1
        elif p[IP].dst == echo_ip:
            direct= -1
        else:
            direct = 0

        echo_df.loc[-1] = [time, p.len, direct]
        echo_df.index = echo_df.index + 1

        # Sort, so list starts in non-reverse order, save to csv
        echo_df = echo_df.sort_index()
    
    return echo_df

def traffic_direction(f_features, direction):
    filt_features = []
    
    for feature in f_features:
        if direction == 'incoming' and feature<0:
            filt_features.append(feature)
        elif direction == 'outgoing' and feature>0:
            filt_features.append(feature)
        elif direction == 'standard':
            filt_features.append(feature)
        else:
            continue
        
    return filt_features
    
def equal_lists(f_features, direction):
    if direction == 'standard':
        f_features.extend([0] * (1000 - len(f_features)))
    return f_features


def datafile(pcap_path, echo_ip, method):	
	data_pcap = pcap_converter(pcap_path, echo_ip)
	f_size = data_pcap['size']
	f_direction = data_pcap['direction']
	f_features = f_size*f_direction
	list_features_pcap = traffic_direction(f_features, method)
	list_features_pcap = equal_lists(list_features_pcap, method)
		
	return list_features_pcap


def datafile_main():
	print('\n######################################################')
	print('##                                                  ##')
	print('##              PROCESS DATA                        ##')
	print('##                                                  ##')
	print('######################################################\n')
	
	pcap_path = sys.argv[1]
	camera_ip = sys.argv[2]
	
	data_pcap = pcap_converter(pcap_path, camera_ip)
	f_size = data_pcap['size']
	f_direction = data_pcap['direction']
	f_features = f_size*f_direction
	list_features_pcap = traffic_direction(f_features, 'standard')
	list_features_pcap = equal_lists(list_features_pcap, 'standard')
	print('PCAP: ',len(list_features_pcap))

if __name__ == "__main__":
		datafile_main()  
