from share_fun import load_data, redef_epoch, def_events, data_prep
import numpy as np
import mne
from scipy.signal import welch
import matplotlib.pyplot as plt
from glob import glob

i = glob('D:\\1-st exp\\OL_1_051116\\*\\') # path to record
for pathrec in i:
    srate = 1000
    data_train, states_train = load_data(pathrec)
    print (np.unique(states_train))
    data_train = data_prep(data_train, srate, 6, 35)
    events_tr = def_events(np.array(states_train))
    epochs_tr, labels_tr = redef_epoch(4.5, np.array(data_train), np.array(events_tr), srate, ignore=None)
    right = epochs_tr[labels_tr==2] # left - 1, right - 2
    rest = epochs_tr[labels_tr==3]
    freqs1, psds_right = welch(right, nperseg=1000, fs=1000, noverlap=900, return_onesided=True)
    freqs2, psds_rest = welch(rest, nperseg=1000, fs=1000, noverlap=900, return_onesided=True)
    psds_right_mean = np.mean(psds_right, axis=0)
    psds_rest_mean = np.mean(psds_rest, axis=0)
    #plt.plot(psds_right_mean[7,5:16], 'r')
    #plt.plot(psds_rest_mean[7,5:16], 'g')
    #plt.show()
    psds_diff = (psds_right_mean - psds_rest_mean) / psds_rest_mean
    to_plot = []
    for i in psds_diff[:, 5:16]:
        to_plot.append(i[np.argmax(abs(i))])

    #np.argmin(i)+5 for freq

    ##ch_names=[u'FC6', u'FC4', u'FC2', u'C6', u'C4', u'C2', u'CP4', u'CP2', u'FCz', u'Cz', u'CPz',
    ## u'CP1', u'C1', u'FC1', u'FC3', u'C3', u'CP3', u'FC5', u'C5']

    ch_names=[u'FC5',u'FT7',u'FC3',u'FCz',u'FC4',u'FT8',u'T3',u'C3',
              u'Cz',u'T4',u'C4',u'TP7',u'CP3',u'CPz',u'CP4',u'TP8',u'FC1',u'FC2',
              u'FC6',u'P4',u'C5',u'C1',u'C2',u'C6',u'P3',u'CP5',u'CP1',u'CP2',u'CP6',u'POz']
    to_print = np.argsort(to_plot)
    for i in to_print:
        print to_plot[i], ch_names[i]

    layout = mne.channels.read_layout('EEG1005')
    ch_types = ['eeg'] * 30
    montage = mne.channels.read_montage('standard_1005', ch_names)
    info = mne.create_info(ch_names, sfreq=1000, ch_types=ch_types, montage=montage)
    import mne.io
    data_fif = mne.io.RawArray(data_train,info)
    data_fif.save(pathrec + 'mne_python_raw.fif')
    import numpy, scipy.io
    scipy.io.savemat(pathrec + 'states.mat', mdict={'states': states_train})
