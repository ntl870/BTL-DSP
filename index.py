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
    E = np.zeros(len(t))  # khoi tao mang E
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


def GetThreshold(E):
    E1 = np.sort(E)
    max = maxl = 0
    for i in range(len(E1)-1):
        if (E1[i+1]-E1[i]) > max:
            max = E1[i+1]-E1[i]
            maxl = E1[i]
    return maxl


# --------------------------------------------------MAIN------------------------------------------------------
Fs, data = read('/media/ntl2000/Data/Study/XLTH/Python/BTL/Resources/TinHieuMau/lab_male.wav')
print(data)


E = chiakhung(Fs, data)

# ------Normalize E---------

min = min(E)
max = max(E)
Normalized1(E, min, max)
# --------------------
# Tim nguong
# E1 = []  # khoi tao mang E
# for i in range(0, len(E)):
#     if E[i] <= GetThreshold(E):
#         E1.append(0)
#     else:
#         E1.append(E[i])


plt.figure()
plt.subplot(2, 1, 1)
plt.plot(E)
plt.subplot(2, 1, 2)
plt.plot(data, color="r")

plt.xlabel('sample index')
plt.ylabel('amplitude')
plt.title('waveform of test audio')
plt.show()
