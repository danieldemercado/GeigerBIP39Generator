from scipy.io.wavfile import read, write
from datetime import datetime
import numpy as np
import sounddevice as sd
import hashlib
import os
 
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


def get_random_bits(ticks):     # Extracts the random bits from the processed data

    random_bits = ""

    for n in range(2,len(ticks),2):

        t1 = ticks[n-1] - ticks[n-2]
        t2 = ticks[n] - ticks[n-1]

        if t1 > t2:         # If the time betwen the first and second ticks is greater than the time betwen the second and the third:

            random_bits = random_bits + str(0)      # Add a 0 to the random generated bits

        elif t1 < t2:   

            random_bits = random_bits + str(1)      # Else add a 1

    return str(random_bits)


def record_data(time,output_name):  # Records the audio data from the Geiger counter

    fs = 44100      # Sample rate
    seconds = time  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write('./' + output_name + '.wav', fs, myrecording)  # Save as WAV file 


def sha256(input_string):   # Returns the SHA-256 hash (in binary) of an input string of 0's and 1's
    return bin(int(hashlib.sha256(int(input_string, 2).to_bytes((len(input_string) + 7) // 8, byteorder='big')).hexdigest() ,16))[2:]


def get_words(input_bits):  # Returns the BIP39 mnenomic words asociated to the input bits

    word_list_file = open("BIP39_wordlist.txt", "r")    # Reads the BIP39 word list from the file BIP39_wordlist.txt
    word_list = word_list_file.read().splitlines()

    words_binary = [input_bits[i:i+11] for i in range(0, len(input_bits), 11)]  # Breaks the input bits in chuncks of 11 bits each
    words_bip39 = []    # Empty list to store the mnenomic words

    for word_binary in words_binary:    # Adds the mnenomic words to the words_bip39 list
        words_bip39.append(str(int(word_binary, base=2) + 1).zfill(4) + " - " + word_list[int(word_binary, base=2)])

    return words_bip39
    

    

print('\n--- Avaiable mnenomic code lenghts: ---\n')    # All the possible mnenomic code lenghts avaiable for generation
print('   (1) - 12 words (128 + 4 = 132 bits)')
print('   (2) - 15 words (160 + 5 = 165 bits)')
print('   (3) - 18 words (192 + 6 = 198 bits)')
print('   (4) - 21 words (224 + 7 = 231 bits)')
print('   (5) - 24 words (256 + 8 = 264 bits)\n')

valid_mnenomic_lenght_option = False   
while valid_mnenomic_lenght_option == False:    # While structure for selecting the mnenomic code generation options. 
    try:
        mnenomic_lenght_option = int(input('Select a mnemonic code lenght option (number between 1 and 5): '))
    except:
        print('Error. Enter a valid option.\n')
        continue

    if mnenomic_lenght_option > 0 and mnenomic_lenght_option < 6:
        valid_mnenomic_lenght_option = True
        if mnenomic_lenght_option == 1:
            print('-> Selected 12 words (128 + 4 = 132 bits).\n')
            bits_objective = 128
            checksum_lenght = 4
        if mnenomic_lenght_option == 2:
            print('-> Selected 15 words (160 + 5 = 165 bits).\n')
            bits_objective = 160
            checksum_lenght = 5
        if mnenomic_lenght_option == 3:
            print('-> Selected 18 words (192 + 6 = 198 bits).\n')
            bits_objective = 192
            checksum_lenght = 6
        if mnenomic_lenght_option == 4:
            print('-> Selected 21 words (224 + 7 = 231 bits).\n')
            bits_objective = 224
            checksum_lenght = 7
        if mnenomic_lenght_option == 5:
            print('-> Selected 24 words (256 + 8 = 264 bits).\n')
            bits_objective = 256
            checksum_lenght = 8
    else:
        print('Error. Enter a valid option.\n')
del valid_mnenomic_lenght_option, mnenomic_lenght_option

print('Generating (at least) ' + str(bits_objective) + ' random bits from your Geiger counter data:')

random_bits = ''
max_volume = None       # This will be the max sound volume in the recorded data        
while len(random_bits) < bits_objective:    # This generates (from the Geiger counter data) the random bits necesary for the mnenomic
    record_name = 'data'
    record_data(60,record_name)

    random_bits = random_bits + get_random_bits(get_ticks("data.wav"))
    print(datetime.now().strftime("%H:%M:%S") + ' - ' + str(len(random_bits)) + ' random bits generated...')
    os.remove(record_name + '.wav')

    print(max_volume)


print('\n --- Extracting your mnenomic code from the random data --- ') # See "Chapter 5 - Wallets" from the book Mastering Bitcoin (Andreas M. Antonopoulos) 

random_bits = random_bits[0:bits_objective] 
random_bits_hash = sha256(random_bits)
random_bits_and_checksum = random_bits + random_bits_hash[0:checksum_lenght]
words = get_words(random_bits_and_checksum)


print("\nEntropy bits generated:\n" + random_bits + "\n")

print("SHA-256 hash from the entropy bits (in binary):\n" + random_bits_hash + "\n")

print("Entropy bits + checksum:\n" + random_bits_and_checksum + "\n")

print(" --- BIP-39 words --- \n")

for word in words:
    print(word)

print("\n(Assuming that: 0001 - abandon, ..., 2048 - zoo)\n")











