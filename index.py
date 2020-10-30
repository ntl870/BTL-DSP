# ---------------------------------------BAI TAP NHOM --------------------------------------------------

# '/media/ntl2000/Data/Study/XLTH/Python/BTL/Resources/TinHieuMau/lab_female.wav'

# -------------------------------------LIBRARY-----------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write

# ----------------------------------------------FUNCTION-------------------------------------------
# chuyen audio sang tan so lay mau Fs2


def chiakhung(Fs, data):  # khoang chia 20ms
    dur = len(data) / Fs  # thoi gian tin hieu am thanh
    t = np.arange(0, dur, 0.02)  # chia khoang bien do 20ms
    E = np.zeros(len(t), dtype=np.float64)  # khoi tao mang E
    n1 = 0
    # xac dinh tuong doi 1 khoang chia gap bao nhieu thoi gian lay mau ( = 0.02/T)
    x = int(0.02*Fs)
    for n in range(len(E)):
        while ((n*x + n1) < len(data)):
            E[n] += data[n*x + n1]**2
            n1 += 1
            if (n1 == x):
                n1 = 0
                break
    return E


def Normalized1(energy, min, max):  # Normalize method 1
    for i in range(0, len(energy)):  # For loop to normalize LIST energy
        energy[i] = (energy[i]-min)/(max-min)


def GetThreshold(E):    #Get Threshold of E
    E1 = np.sort(E)
    max = maxl = 0
    for i in range(len(E1)-1):
        if (E1[i+1]-E1[i]) > max:
            max = E1[i+1]-E1[i]
            maxl = E1[i]
    return maxl


def GetEdge(E):         # Get the edges
    voiced = np.zeros(len(E), dtype=np.float64)
    unvoiced = np.zeros(len(E), dtype=np.float64)
    res = np.zeros(len(E), dtype=np.float64)
    for i in range(0, len(E)-1):
        if(E[i] > 0.01):
            voiced[i] = 1
        else:
            unvoiced[i] = 1

    for i in range(1, len(E)-1):
        if voiced[i] == unvoiced[i-1]:
            res[i-1] = 1
    return res


# --------------------------------------------------MAIN------------------------------------------------------
Fs, data = read('/media/ntl2000/Data/Study/XLTH/Python/BTL/Resources/TinHieuMau/lab_female.wav')
print(data)


E = chiakhung(Fs, data)

# ------Normalize E---------

min = min(E)
max = max(E)
Normalized1(E, min, max)



E1 = np.zeros(len(E), dtype=np.float64)

for i in range(0, len(E1)-1):
    E1[i] = E[len(E)-i-1]
 # khoi tao mang E
x = np.zeros(len(E), dtype=np.float64)


arrayX = np.linspace(0, len(E), len(E))

plt.figure()

plt.plot(arrayX, E, color="r")
plt.stem(arrayX, GetEdge(E))


plt.xlabel('sample index')
plt.ylabel('amplitude')
plt.title('waveform of test audio')
plt.show()
