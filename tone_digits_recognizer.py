"""tone-digits-recognizer
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sys

# Fast Fourier Transform
def FFT(x):
  # getting the length of the data
  N = len(x)

  # initializing an array with all zeros and of type complex 
  X = np.zeros(N, complex)
  if N <= 1:
      return x                        
  try:
    # recursive manner 
    # Calculating FFT for even points or samples
    even = FFT(x[0::2])
    # Calculating FFT for odd points or samples
    odd = FFT(x[1::2])
    # Lambda functions to help in calculation
    lambda1 =lambda a : a/N
    lambda2 = lambda b: b + N // 2 
    # for loop for calculating the FFT
    for i in range(N // 2):
        l1 =  lambda1(i)
        l2 =  lambda2(i)
        
        # W_N
        W_N = np.exp(-2j * np.pi *l1 )
        
        #W_N/2
        W_N_div_2= np.exp(-2j * np.pi * l2/ N)
        
        #calculating x[i] and x[i+N/2] 
        X[i] = even[i] + W_N * odd[i]
        X[i + N // 2] = even[i] + W_N_div_2 * odd[i]
    return X
  except: 
    # N should be a power of 2
    if N % 2 > 1:
        raise ValueError("x size should be a power of 2")


# Function responsible to display the number in the wav file
def display_number(d_count,digits_freqs):
  # output sequence
  digits_seq = []
  for i in range (0,d_count):
    if digits_freqs[i] == digits['*']:
        #print("The tone is *")
        digits_seq.append('*')
    elif digits_freqs[i] == digits['#']:
        #print("The tone is #")
        digits_seq.append('#')
    else:
      for j in range(len(digits)):
        if digits_freqs[i] == digits[f'{j}']:    
            #print(f"The tone is {j}")
            digits_seq.append(j)
            break
  print("As A list")  
  print(digits_seq)
  print("As A number")
  print(*digits_seq)

# dictionary containing the frequencies of the 
# digits in the telephone digits keypad

digits = {
    '0':[1336,941],
    '1':[1209,697],
    '2':[1336,697],
    '3':[1477,697],
    '4':[1209,770],
    '5':[1336,770],
    '6':[1477,770],
    '7':[1209,852],
    '8':[1336,852],
    '9':[1477,852],
    "*":[1209,941],
    "#":[1477,941]
}

# taking the audio file as an input
audiofile = sys.argv[1]

# get the sampling rate and data from the wav file
fs,data = wavfile.read(audiofile)

#plt.figure(figsize=(15,5))
#plt.plot(data)
#plt.show()

# considering the digits [0.1] and the pauses[0.1]
sample_period = 0.1+0.1
freq_s = int(sample_period * fs)



#digits_count
d_count = int(len(data)/freq_s)

## digits frequencies ##

# low frequencies of the digits, according to DTMF
low_frequencies = [697,770,852,941]

#high frequencies of the digits, according to DTMF
high_frequencies = [1209,1336,1477]

step= 0 

#List that will contain the hi and lo frequencies of each digit
digits_freqs =[] 


for i in range (1,d_count+1):

  # Getting the frequencies  f_m = m * Fs/N for each digit
  fs_over_N = fs/data[step:800+step].shape[0]
  m = np.empty(data[step:800+step].shape[0],dtype =int)
  x = (data[step:800+step].shape[0]-1)//2+ 1
  f1 = np.arange(0,x,dtype= int)
  f2 = np.arange(-(data[step:800+step].shape[0]//2),0,dtype = int)
  m[:x] = f1
  m[x:]= f2
  f_m = m * fs_over_N

  #using the FFT from our implementation
  magnitudes= FFT(data[step:800+step])
  
 # plt.figure(figsize=(15,5))
 # plt.plot(np.absolute(magnitudes))
 # plt.title('FFT')
 # plt.xlabel('Frequency(Hz)')
 # plt.ylabel('magnitude')
 # plt.show()
  step+=freq_s
  
  ##  Low Frequency spike ####
  #returns the index of the first number greater or = than the min freq in the DTMF LOW freqs which is 697
  min = np.where(f_m >= np.min(low_frequencies)) [0][0]
  #returns the index of the first number greater or =than the max freq in the DTMF LOW freqs which is 941
  max = np.where(f_m >= np.max(low_frequencies)) [0][0]

  # now that we have the indices of the range of frequencies in the acceptable range of the DTMF low freqs
  # we create a list with all these values
  freq = f_m[min:max]

  # now we get all the magnitudes that we got from the fft calculation based on the range of freqs
  # in the acceptable range of the DTMF low freqs
  mag = abs(magnitudes.real[min:max])

 # plt.figure(figsize=(15,5))
 # plt.stem(mag,use_line_collection=True)
 # plt.title('Low frequency component part')
 # plt.xlabel('Frequency(Hz)')
 # plt.ylabel('magnitude')

 # plt.show()
  # get index of max magnitude in range of DTMF low freqs
  imax_mag_lo = np.where(mag == np.max(mag))[0][0]
  
  # we get the frequency component with the highest mag (First Spike)
  lo = freq[imax_mag_lo]

  for i in low_frequencies:
    if abs(lo-i) < 30:
      lo = i
  
  #High Frequency spike ##

  #returns the index of the first number greater than or = the min freq in the DTMF HIGH freqs which is 1209
  min = np.where(f_m >= np.min(high_frequencies))[0][0]
  #returns the index of the first number greater than or = the max freq in the DTMF HIGH freqs which is 1477
  max = np.where(f_m >= np.max(high_frequencies))[0][0]
 
  # now that we have the indices of the range of frequencies in the acceptable range of the DTMF HIGH freqs
  # we create a list with all these values
  freq = f_m[min:max]
  
  # now we get all the magnitudes that we got from the fft calculation based on the range of freqs
  # in the acceptable range of the DTMF HIGH freqs
  mag = abs(magnitudes.real[min:max])

  #plt.figure(figsize=(15,5))
  #plt.stem(mag,use_line_collection=True)
  #plt.title('High frequency component part')
  #plt.xlabel('Frequency(Hz)')
  #plt.ylabel('magnitude')

  #plt.show()
  # get index of max magnitude in range of DTMF High freqs
  imax_mag_hi = np.where(mag==np.max(mag))[0][0]

  # we get the frequency component with the highest mag (Second Spike)
  hi = freq[imax_mag_hi]


  for i in high_frequencies:
    if abs(hi-i) < 30:
      hi = i

  digits_freqs.append([hi,lo])


#Display the number
display_number(d_count,digits_freqs)