# ---------------------------------------BAI TAP NHOM --------------------------------------------------

#'/media/ntl2000/Data/Study/XLTH/Python/BTL/Resources/TinHieuMau/lab_female.wav'

# -------------------------------------LIBRARY-----------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write

# ----------------------------------------------FUNCTION-------------------------------------------
# chuyen audio sang tan so lay mau Fs2


def chiakhung(Fs, data):  # khoang chia 20ms
    dur = len(data) / Fs  # thoi gian tin hieu am thanh
    t = np.arange(0, dur, 0.02)  # chia khoang bien do 20ms
    E = np.zeros(len(t))  # khoi tao mang E
    n1 = 0
    # xac dinh tuong doi 1 khoang chia gap bao nhieu thoi gian lay mau ( = 0.02/T)
    x = int(0.02*Fs)
    for n in range(len(E)):
        while ((n*x + n1) < len(data)):
            E[n] += abs((data[n*x + n1]*data[n*x + n1]))
            n1 += 1
            if (n1 == x):
                n1 = 0
                break
    return E


def Normalized1(energy, min, max):  # Normalize method 1
    return (energy-min)/(max-min)
    





# --------------------------------------------------MAIN------------------------------------------------------
Fs, data = read('/media/ntl2000/Data/Study/XLTH/Python/BTL/Resources/TinHieuMau/lab_female.wav')
print(data)
arrayX = []

E = chiakhung(Fs, data)
min = min(E)        #Get min
max = max(E)        #Get max


for i in range(0,len(E)):               #For loop to normalize LIST E
    E[i] = Normalized1(E[i],min,max)    
   

print(E)
plt.figure()
plt.plot(E)
plt.xlabel('sample index')
plt.ylabel('amplitude')
plt.title('waveform of test audio')
plt.show()
