# Application with the objective of showing realtime whether there is movement in the building or not.
import os.path
import sys
import subprocess
import argparse
from ProcData import generateCSV, obtainData

from models.mlp_model import MLP_Model
from utils import config as MLP_config

def load_MLP_config():
    argparser = argparse.ArgumentParser()


def capture(device_ip, duration, dir, captureName):
    capture = subprocess.Popen("sudo timeout " + str(duration) + " tcpdump -i wlan0 -n host " + str(
        device_ip) + " -w " + dir + str(captureName) + ".pcap", shell=True, stdout=subprocess.PIPE)
    capture.wait()

def monitoring(ip, interval, dir):
    # Start the capture.
    #capture(ip, interval, dir, 'test')
    # Process the captured data
    # TODO: Here we need to process the data in a way that the model understands it, \
    #  the first approach was to generate the csv and then read csv etc. However, we think \
    #  that we can do it avoiding the creation of new files. By doing the processing \
    #  and storing it directly as the expected format. \
    #  Would need to take a look at the code to do this. So I Write a commentary :)

    #Autocreate a list with my directory name.
    ''''
    list_dir = generateCSV.list_queries(dir)
    list_files = []
    files = generateCSV.list_files(dir)
    list_files.extend(files)
    print("Files in directory: ", list_files)
    generateCSV.generateCSV(list_files, ip)
    '''
    # Load the model
    config = MLP_config.process_config('config/mlp_config.yml')
    model = MLP_Model(config)
    model.load()

    # Obtain Classification
    # Assuming we have the data in an array of samples.
    samples=[]
    labels=[] # This should be void or all to 0, does not matter.
    prediction = model.predict(samples, labels)

    # Show the results
    # TODO: Here the idea is to show the results. \
    #  We talked about storing the 5 past results in a list and then output based on them. \
    #  I'll leave this until I have the current results etc.

    # TODO: The idea is to have this as a realtime so we would put everything \
    #  In an infinite loop and that's it... \
    #  In a loop the model load is done only ONCE


# Main Idea:
#   Load Model
#   Capture Data.
#   Process captured data so model understands.
#   Load Model.
#   Predict.
def main():
    if len(sys.argv) < 2:
        print("Usage: app.py <IPToCapture> <secondsOfCapture> <pathToStoreCaptures>")
        return

    # Configure environment
    ip=sys.argv[1]
    interval=sys.argv[2]
    dir=sys.argv[3]

    if not os.path.exists(dir):
        os.mkdir(dir)

    # Perform the monitoring
    monitoring(ip, interval, dir)

    # After monitoring delete the data.
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f)) # This will fail if it encounters a directory but we should not have any dir.




if __name__ == "__main__":
    main()
