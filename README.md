# GeigerBIP39Generator
A python 3 script for generating BIP39 mnemonic codes with random data coming from a Geiger counter.

## Index
1. [Disclaimer](#disclaimer)
2. [Requirements](#requirements)
3. [How to use it](#how-to-use-it)

## Disclaimer <a name="disclaimer" />
I am not responsible for any coins lost due to the misuse of this script, nor due to it's use on a compromised computer. The script should be run on a computer that is permanently disconnected from the internet. 

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

1. Clone this repository to your computer:  
  `git clone https://github.com/danieldemercado/GeigerBIP39Generator`
  
   Navigate to the cloned repository:  
   `cd GeigerBIP39Generator`

2. Connect your Geiger counter to the computer as a microphone, using a male to male aux cable. Make sure that the Geiger counter input is selected as your default microphone in your computer settings, and that the counts are being detected.

3. If you are using a different Geiger counter, you will probably need to change the response time of your tube. Open `GeigerBIP39Generator.py` with your favourite editor and locate the funcion `get_ticks`:
    ```python3
    def get_ticks(wav_file):                    # This function reads the .wav file with the Geiger-Muller counter data and returns the times of the counts

        global max_volume

        a = read(wav_file)                      # Read the .wav file

        volume = np.array(np.abs(a[1]),dtype=float)         # Sound volume of the data
        time = np.arange(len(a[1]))/a[0]                    # Time for each data point

        if max_volume == None:                              # Gets the max volume in the data. Different computers might register different max volumes.
            max_volume = np.amax(volume)

        skip_time = 0.000270                                # The time (in seconds) that the Geiger tube needs to return to normal plus a little more (For GMC-300E plus ~ 270 μs) 
        skip_points = int(skip_time * a[0])                 

        ticks = []                                          # Empty list to save the tick's time

        n = 0                                               # While loop for processing the .wav
        while n < len(volume):

            if volume[n] > 0.25*max_volume:                               # If a tick is detected
                ticks.append(time[n])                              # Save its time

                n += skip_points                                   # Skip the data until de tube returns to normal

            n += 3                                          # Resolution of the data analysis. This must be a time smaller than the skip time (i.e.: n/a[0] << skip_time)

        return ticks
    ```

    Change `skip_time = 0.000270` (in seconds) to the response time of your tube plus a little more (for the GQ GMC-300E Plus, the response time is ~240 μs, so 270 μs works fine). You must find the response time of your tube manually, by recording some data and analizing the time width of the counts.
    
    If the response time of your tube is much smaller (bigger) than 270 μs, you will probably also need to increase (reduce) the data analysis resolution by reducing (increasing) the integer number in `n += 3`.
    
4. Run the script with the command: `python3 GeigerBIP39Generator.py`

5. The script will ask you to choose a mnemonic code words length. Choose the one you like.

6. Wait untill the generation process finishes, this might take up to 20 minutes if you are only using background radiation. When this is done, the BIP39 words should be printed to the terminal.

You can check how it works in [this video](https://www.youtube.com/watch?v=Qx44_psG9KI).
