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
