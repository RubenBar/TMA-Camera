# Application with the objective of showing realtime whether there is movement in the building or not.
import os.path
import sys
import subprocess
import argparse
from ProcData import generateCSV, obtainData
from collections import deque

from Keras.ModeloMLP.models.mlp_model import MLP_Model
from Keras.ModeloMLP.utils import config as MLP_config

def load_MLP_config():
    argparser = argparse.ArgumentParser()


def capture(device_ip, duration, dir, captureName):
    filepath = dir+str(captureName)+".pcap"
    capture = subprocess.Popen("sudo timeout " + str(duration) + " tcpdump -i wlan0 -n host " + str(
        device_ip) + " -w " + dir + str(captureName) + ".pcap", shell=True, stdout=subprocess.PIPE)
    capture.wait()
    return filepath


def monitoring(ip, interval, dir):
    # Initialize variables for the prediction:
    prediction_list = [-1] * 5
    # Initializing Circular queue as -1
    predictions = deque(prediction_list, maxlen=5)
    previous_prev = -1
    old_mov_ratio = 0
    mov_ratio = 0

    # Load the model
    model = MLP_Model(None)
    model.load("../Keras/ModeloMLP/models/save/")

    while 1:
        # Start the capture.
        filename = capture(ip, interval, dir+"captures", 'test')

        # Process the captured data
        # files = generateCSV.list_files(dir + "/mov/")
        # data_packets = obtainData.datafile(files[0], ip, 'standard')
        # Delete all 0 packets (at the end)
        data_packets = list(filter(lambda num: num != 0, obtainData.datafile(filename, ip, 'standard')))

        # Obtain Classification
        samples=[]
        labels=[] # This should be void or all to 0, does not matter.
        samples.append(data_packets[:648])
        prediction = model.predict(samples, labels)

        predictions.appendleft(prediction[0])
        # Iterate the list and see if there is more mov or nomov.
        mov = 0
        nomov = 0
        for p in predictions:
            if p != -1:
                if p == 1:
                    mov += 1
                else:
                    nomov += 1
        if nomov > 0:
            mov_ratio = mov/nomov
        else:
            mov_ratio = mov
        if mov > nomov:
            print("There is movement")
        elif nomov > mov:
            print("There is no movement")
        else:
            if prediction[0] == 1:
                print("Movement detected")
            else:
                print("No movement detected")

        if mov_ratio > old_mov_ratio:
            print("Movement detection increasing")
        elif mov_ratio < old_mov_ratio:
            print("Seems that the movement is stopping")
        old_mov_ratio = mov_ratio

        os.remove(filename)
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
    ip = sys.argv[1]
    interval = sys.argv[2]
    dir = sys.argv[3]

    if not os.path.exists(dir):
        os.mkdir(dir)

    # Perform the monitoring
    monitoring(ip, interval, dir)

    # After monitoring delete the data.
    '''for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))  # This will fail if it encounters a directory but we should not have any dir.
    '''



if __name__ == "__main__":
    main()
