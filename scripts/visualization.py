import matplotlib.pyplot as plt
import seaborn as sn
import IPython
import IPython.display as ipd

# plot series
def plot_series(y):
  plt.plot(y);
  plt.title('Signal');
  plt.xlabel('Time (samples)')
  plt.ylabel('Amplitude')

# play sound on the notebook
def play_sound(file):
  return ipd.Audio(file)

# plot and see the melspectograms
def plot_spectrogram(spec, title='Spectrogram (db)', ylabel='freq_bin', aspect='auto', xmax=None):
  fig, axs = plt.subplots(1, 1)
  axs.set_title(title)
  axs.set_ylabel(ylabel)
  axs.set_xlabel('frame')
  im = axs.imshow(spec, origin='lower', aspect=aspect)
  if xmax:
    axs.set_xlim((0, xmax))
  fig.colorbar(im, ax=axs)
  plt.show(block=False)
