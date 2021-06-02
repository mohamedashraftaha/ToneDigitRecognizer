# ToneDigitRecognizer
The goal of this project is to create a code that receives telephone tone digits and identifies the digits that were selected. 

# Overview of the approach to this project
I created a Python code that receives the wav file containing the tones of the digits, and then we applied signal processing concepts on it and we displayed the output on the screen. Screenshots will be included in this report. Below is a figure to visualize our design to solve this problem.

![image](https://user-images.githubusercontent.com/75078872/120473109-f8239100-c3a6-11eb-936a-9093ecb04f42.png)

# Steps of designing the project
- Dual Tone Multi Frequency (DTMF ):
While inspecting the tone digits and how they work, we came across this important aspect, the Dual Tone Multi Frequency (DTMF). DTMF is the signal that you generate when you press an ordinary telephone's touch keys. DTMF has replaced the ordinary Pulse dialing which is the first type of telephone dialing, and it consisted of short pulses that were used to relay the dialed number. By using DTMF, each keypress on a phone generates tones made of two specific frequencies that will play an important role in us designing our code. These frequencies is represented by the following table: 

![image](https://user-images.githubusercontent.com/75078872/120473425-4cc70c00-c3a7-11eb-87cf-7e0d2f13322a.png)

- Logic of the code
* Started by creating a dictionary representing the frequencies table above in Fig1. As we can see here in this screenshot, each digit is represented with the equivalent high and low frequencies according to Fig1.

![image](https://user-images.githubusercontent.com/75078872/120473564-72541580-c3a7-11eb-9c17-39e50d45b954.png)

*  The next step is to read the input tone digits using the function wavefile.read, from the library scipy.io. Based on the waveform below of an example “#_0123456789#”.wav, included in the submission file, we can observer that the sample period takes 0.1 + other 0.1s for the pauses, so we got the got the samples. Then we divided the size of the data by the number of samples so that we can extract how many digit we have.

![image](https://user-images.githubusercontent.com/75078872/120474173-2eaddb80-c3a8-11eb-9d7c-4473c617b934.png)

*  then created two arrays containing the low_frequencies of the tone digits and high_frequencies based on the table below. 

![image](https://user-images.githubusercontent.com/75078872/120474211-379ead00-c3a8-11eb-85f9-f59d572443a3.png)

*then created a loop with the number of digits that we got, and we extract each digit alone and start to process it alone. Then when we have all the digits we put them in an array and print it. Below is snapshot of the code explaining the logic applied to each digit.
First we get the analysis frequencies Fm for the digit using the equation F_m= m * Fs/N

![image](https://user-images.githubusercontent.com/75078872/120475098-3d48c280-c3a9-11eb-812a-3db09b3f2fb0.png)


* What we do next is that we get the magnitude of the FFT, which take each digit as an input as shown in the below snapshot. This snapshot is of the first digit in “#_0123456789#.wav”. 
As we can see here there are two spikes that we interested in the High frequency one and the low frequency one according to Fig2. ALL the screenshots from the “#” digit as an example

![image](https://user-images.githubusercontent.com/75078872/120474343-5f8e1080-c3a8-11eb-91f7-f6abfc8f6284.png)

* To get the high frequency and low frequency spikes of this digit and compare it to the table in Fig1. We deal with each part alone:ALL the screenshots from the “#” digit as an example
  - Low frequency component
I. We first start with the low frequency component, we get the index, from the frequency analysis,  of the first number greater than or equal  the minimum frequency component in the DTMF low frequencies list which is 697
II. Then we get the index of the first number greater than or equal the maximum frequency component in the DTMF low frequencies list  which is 941
III.Now that we got the indices has the values between 697 and 941 which is the range of the low frequencies, we then create a list with these values -> freq
IV. we then get the magnitudes of the range of the indices that we got

![image](https://user-images.githubusercontent.com/75078872/120474431-7fbdcf80-c3a8-11eb-944f-715ba8805ae1.png)

V.Then we extract the index of the maximum magnitude.
VI. Now we get the value of the maximum magnitude by giving freq[maximum of max magnitude], and that will be the low frequency component of that digit. 
VII. we also create a buffer of difference of 30 between the values so that we can select it to be the low frequency component

  - High frequency component
I. We first get the index, from the frequency analysis,  of the first number greater than or equal  the minimum frequency component in the DTMF High frequencies list which is 1209
II.Then we get the index of the first number greater than or equal the maximum frequency component in the DTMF high frequencies list  which is 1477
III.Now that we got the indices has the values between 1209 and 1477 which is the range of the low frequencies, we then create a list with these values -> freq
IV. we then get the magnitudes of the range of the indices that we got

![image](https://user-images.githubusercontent.com/75078872/120474579-a976f680-c3a8-11eb-869f-10611c558f23.png)

V. Then we extract the index of the maximum magnitude.
VI. Now we get the value of the maximum magnitude by giving freq[maximum of max magnitude], and that will be the high frequency component of that digit. 
VII. we also create a buffer of difference of 30 between the values so that we can select it to be the high frequency component

* We then append the low and high frequency components to a list and append that list to a bigger list that will contain all the values frequency components of all digits at the end. 

digits_freqs.append([hi,lo])

* Finally, we compare the frequency components extracted for each digit with the dictionary that we had at first, and thus being able to identify which digit it is. We then printed to the screen as a list and as a number. Here is a sample output of the code with the example “#_0123456789#.wav”. N.B the “_” is the “*”, we changed the name since we cant save a file name with * as part of the name

![image](https://user-images.githubusercontent.com/75078872/120474728-d6c3a480-c3a8-11eb-99e2-2f65c7333b9e.png)


# References Used 
[1]  Bagchi S., Mitra S.K. (1999) Dual-Tone Multi-Frequency Signal Decoding. In: The Nonuniform Discrete    Fourier Transform and Its Applications in Signal Processing. The Springer International Series in                   Engineering and Computer Science, vol 463. Springer, Boston, MA. https://doi.org/10.1007/978-1-4615-4925-3_6      
[2] https://ptolemy.berkeley.edu/eecs20/week2/dtmf.html

[3] https://www.audiocheck.net/audiocheck_dtmf.php
# To run the code
- The wav file name is taken as an input from the user
- python3 tone_digits_recognizer.py audiofile_name.wav
