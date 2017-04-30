clear
load('states.mat')
fiff_file = 'mne_python_raw.fif';

cfg=[];
for i=2:length(states)
    if states(i)~=states(i-1)
        cfg(end+1,:) = [i];
    end
end
trl=[1 cfg(1)-1 0 states(1)];
for i=1:length(cfg)-1
    trl(end+1,:)=[cfg(i) cfg(i+1)-1 0 states(cfg(i))];
end
trl(end+1,:)=[cfg(end) length(states) 0 states(end)];

% trl = [];
% for i=2:length(states)
%     if states(i)~=states(i-1)
%         trl(end+1, :) = [i i+4900 0 states(i)];
%     end
% end
cfg=[];
cfg.trl=trl;
cfg.dataset = fiff_file;
data1 = ft_preprocessing(cfg);

cfg = [];
cfg.method = 'triangulation';
cfg.feedback      = 'no';
neighbours = ft_prepare_neighbours(cfg, data1);

cfg=[];
cfg.method = 'hjorth';
cfg.neighbours = neighbours;
[data] = ft_scalpcurrentdensity(cfg, data1);

cfg=[];
cfg.trials = data.trialinfo==3;
cfg.trials = cfg.trials';
[data_rest] = ft_selectdata(cfg, data);
hand = 2; % 1 - left, 2 - right
cfg.trials = data.trialinfo==hand;
cfg.trials = cfg.trials';
[data_left] = ft_selectdata(cfg, data);

cfg=[];
cfg.method = 'mtmfft';
cfg.output     = 'pow';
cfg.foi     = [12];
cfg.tapsmofrq = 1;
cfg.pad = 'nextpow2';
[freq_rest] = ft_freqanalysis(cfg, data_rest);
[freq_left] = ft_freqanalysis(cfg, data_left);

freq = freq_rest;
freq.powspctrm=(freq_left.powspctrm-freq_rest.powspctrm)./freq_rest.powspctrm;
cfg=[];
ft_topoplotER(cfg, freq);
if hand == 1
    save('freq_left.mat','freq');
else
    save('freq_right.mat','freq');
end