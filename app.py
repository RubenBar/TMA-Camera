# Application with the objective of showing realtime whether there is movement in the building or not.
import os.path
import sys
import subprocess


def capture(device_ip, duration, dir, captureName):
    capture = subprocess.Popen("sudo timeout " + str(duration) + " tcpdump -i wlan0 -n host " + str(
        device_ip) + " -w " + dir + str(captureName) + ".pcap", shell=True, stdout=subprocess.PIPE)
    capture.wait()

def monitoring(ip, interval, dir):
    # Start the capture.
    capture(ip, interval, dir, 'test')
    # Process the captured data
    # TODO: Here we need to process the data in a way that the model understands it, \
    #  the first approach was to generate the csv and then read csv etc. However, we think \
    #  that we can do it avoiding the creation of new files. By doing the processing \
    #  and storing it directly as the expected format. \
    #  Would need to take a look at the code to do this. So I Write a commentary :)

    # Load the model

    # Obtain Classification

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
