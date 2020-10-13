# br41n-hackathon

This project aims to classify, in real time, whether a hand is closed or open based on 7 channels EEG. The classification is then sent to a Unity hand model.

## Classification

We have based our training on two different datasets. First one is the dataset published with a paper written by Hohyun Cho, Minkyu Ahn, Sangtae Ahn, named "EEG datasets for motor imagery brain–computer interface" (see [here](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5493744/?report=classic)). The dataset consists of 52 recordings for one suject each. The corresponding dataset can be found [here](ftp://parrot.genomics.cn/gigadb/pub/10.5524/100001_101000/100295/mat_data/).

## Real time streaming to Unity

Here's the repository where the hand modelization and control was made: https://github.com/paulbaniqued/EMG-LSL. The script which received data from the OpenBCI GUI (v.4.1.7, https://github.com/OpenBCI/OpenBCI_GUI), classified epochs, and send back prediction to Unity is here: https://github.com/conorato/br41n-hackathon/blob/main/Br41n.io/hand_motion_detection.py
