from pylsl import StreamInlet, resolve_stream
from scipy import signal
from mne.io import RawArray
from mne import create_info
from mne.time_frequency import psd_welch

import scipy
import numpy as np
import pylab as pl
import joblib

#global parameters
srate = 250
epoch_len = srate

#load classification pipeline
pipeline = joblib.load("./models/rf.joblib")
CHANNELS = ['Cz', 'FC2', 'CP2', 'C4', 'FC6', 'CP6', 'T8']
FREQ_BANDS_RANGE = {
    'DELTA': [0.5, 4.5],
    'THETA': [4.5, 8.5],
    'ALPHA': [8.5, 11.5],
    'SIGMA': [11.5, 15.5],
    'BETA': [15.5, 30]
}

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')
print('got stream')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])
print('got inlet')

# initiate the signal with a first sample
sample, timestamp = inlet.pull_sample()
print('pulled first sample')

#the data and the time vector
data = [sample]
timevec = [0]

print('Starting steaming')

def get_mean_psds(psds_with_freqs, are_relative=False):
    """EEG power band feature extraction.
    Input
    -------
    psds_with_freqs: tuple which contains
            - (nb_epochs, nb_chan=1, nb_freqs) psds amplitudes
            - (nb_freqs,) corresponding frequency values

    are_relative: boolean which indicates if the mean band powers
        for each subband are relative to the total power or not.

    Returns
    -------
    X : numpy array of shape [n_samples, nb_subband=5]
        Transformed data.
    """
    psds = psds_with_freqs[0]
    freqs = psds_with_freqs[1]

    if are_relative:
        psds /= np.sum(psds, axis=-1, keepdims=True)

    X = []
    for fmin, fmax in FREQ_BANDS_RANGE.values():
        psds_band = psds[:, (freqs >= fmin) & (freqs < fmax)].mean(axis=-1)
        X.append(psds_band)

    return np.concatenate(X, axis=0)

while True:

    # get a new sample
    sample, timestamp = inlet.pull_sample()
    #New datas are added to the buffers
    data.append(sample)
    timevec.append(len(timevec)/srate)

    if(len(data) == epoch_len):
        print('Acquired signal with mean: ', np.mean(data))
        data = np.transpose(np.array(data)[:,:len(CHANNELS)])
        raw_array = RawArray(data, info=create_info(sfreq=srate, ch_types='eeg', ch_names=CHANNELS))
        # raw_array.notch_filter(60)
        # raw_array.filter(0.5, 60)

        print(raw_array.n_times)
        psds, freqs = psd_welch(raw_array, fmin=0.5, fmax=30., n_fft=250)
        features = get_mean_psds((psds, freqs))

        print('Hand is: ', pipeline.predict([features]))

        data = []