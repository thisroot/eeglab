import pickle
import numpy as np
import scipy.signal as spsig


def load_data(pathload):
    with open(pathload + 'data.pkl', 'rb') as input_load:
        data_load = pickle.load(input_load)
    with open(pathload + 'states.pkl', 'rb') as input_load:
        states_load = pickle.load(input_load)
    return data_load, states_load


def redef_epoch(ep_len, data, events_list, sfreq, ignore):
    new_epochs = []
    new_labels = []
    for event in range(1, len(events_list)):
        if ignore is not None and events_list[event - 1, 2] == ignore:
            pass
        else:
            cur_pos = events_list[event - 1, 0]
            while cur_pos + sfreq * ep_len < events_list[event, 0]:
                new_epochs.append(data[:, int(cur_pos):int(cur_pos + sfreq * ep_len)])
                new_labels.append(int(events_list[event - 1, 2]))
                cur_pos += sfreq * ep_len
    return np.array(new_epochs), np.array(new_labels)


def def_events(states_vec):
    events = [[0, 0, states_vec[0, 0]]]
    for i in range(1, len(states_vec[0])):
        if states_vec[0, i] != states_vec[0, i - 1]:
            events.append([i, states_vec[0, i - 1], states_vec[0, i]])
    return np.array(events)


def data_prep(data, sfreq, fmin, fmax):
    [b_high, a_high] = spsig.butter(4, float(fmin) / (sfreq / 2), 'high')
    [b_low, a_low] = spsig.butter(4, float(fmax) / (sfreq / 2), 'low')

    chunk_high = spsig.lfilter(b_high, a_high, data)
    chunk_low = spsig.lfilter(b_low, a_low, chunk_high)
    return chunk_low
