# GeigerBIP39Generator
A python 3 script for generating BIP39 mnemonic codes with random data coming from a Geiger counter

## Index
1. [Requirements](#requirements)
2. [How to use it](#how-to-use-it)

## Requirements <a name="requirements" />
* This script needs `Python3`. I'm running version `3.8.10`, but other versions will likely work.

* Additionally, you will need this modules:
  `scipy`
  `numpy`
  `sounddevice`
  `hashlib`
  `datetime`
  `os`  
  Some of them should come with your Python instalation. 

  You can try to install them with pip:  
  `python3 -m pip install scipy`  
  `python3 -m pip install numpy`  
  `python3 -m pip install sounddevice`  

  This ones should come with your instalation:  
  `python3 -m pip install hashlib`  
  `python3 -m pip install datetime`  
  `python3 -m pip install os`
  
* Finally, you will need a Geiger counter that can be connected to your computer as a microphone (i.e. that has an aux connection). I use a GQ GMC-300E Plus, but other GQ models or brands should work (although you might need to change the response time of your tube, more about this below).

## How to use it <a name="how-to-use-it" />

1. Connect your Geiger counter to the computer as a microphone, using a male to male aux cable. Check that the Geiger counter input is selected as your default microphone in your computer settings.

2. If you are using a different Geiger counter, you will probably need to change the response time of your tube. Open `GeigerBIP39Generator.py` with your favourite editor and locate the funcion `get_ticks`:
```python3
def get_ticks(wav_file):                    # This function reads the .wav file with the Geiger-Muller counter data and returns the times of the counts

    a = read(wav_file)                      # Read the .wav file

    volume = np.array(np.abs(a[1]),dtype=float)         # Volume of the data
    time = np.arange(len(a[1]))/a[0]                    # Time for each data point

    skip_time = 0.000270                                # The time (in seconds) that the Geiger tube needs to return to normal (For GMC-300E plus ~ 270 μs) 
    skip_points = int(skip_time * a[0])                 

    ticks = []                                          # Empty list to save the tick's time

    n = 0                                               # While loop for processing the .wav
    while n < len(volume):
        
        if volume[n] > 0.25:                         # If a tick is detected
            ticks.append(time[n])                        # Save its time

            n += skip_points                             # Skip the data until de tube returns to normal
            
        n += 3               # Resolution of the data analysis. This must be a time smaller than the skip time (i.e.: n/a[0] << skip_time)

    return ticks
```
