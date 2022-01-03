# TMA-Camera


## How to capture data?
```
python captureDataCamera.py <camera_ip> <num_it> <time> <mov/no_mov>
i.e. python captureDataCamera.py 192.168.4.5 1 10 0
```

## How to process data?
```
python3 generateCSV.py <dir_data> <camera_ip>
i.e. python3 generateCSV.py data/ 192.168.4.5
```

## How to execute App:
We need to download the model from this google drive link: https://drive.google.com/file/d/18eWYMcsb8MUyu20JqGdaLEho8ufvTZ-u/view?usp=sharing And then move it to TMA-Camera\Keras\ModeloCNN\models\save

We need to do this because GitHub does not allow us to upload files with certain sizeg 


