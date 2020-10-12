from pylsl import StreamInlet, resolve_stream
from scipy import signal
import scipy
import numpy as np
import pylab as pl

#global parameters
srate = 250
epoch_len = srate

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

# initiate the signal with a first sample
sample, timestamp = inlet.pull_sample()

#the data and the time vector
data = [sample[0]]
timevec = [0]

while True:

    # get a new sample
    sample, timestamp = inlet.pull_sample()
    
    #New datas are added to the buffers
    data.append(sample[0])
    timevec.append(len(timevec)/srate)

    if(len(data) == epoch_len):
        print()