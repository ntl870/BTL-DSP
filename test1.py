# # ---------------------------------------BAI TAP NHOM --------------------------------------------------

# # '/media/ntl2000/Data/Study/XLTH/Python/BTL/Resources/TinHieuMau/lab_female.wav'
# #  'D:\Study\XLTH\Python\BTL\Resources\TinHieuMau\lab_female.wav'

# # -------------------------------------LIBRARY-----------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
import copy
import math


# # ----------------------------------------------FUNCTION-------------------------------------------
# # chuyen audio sang tan so lay mau Fs2


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


def Normalized1(energy, min, max):
    res = []
    for i in range(0, len(energy)):
        res.append((energy[i]-min)/(max-min))
    return res

def ZCRframe(Fs, data):  # khoang chia 20ms
    dur = len(data) / Fs  # thoi gian tin hieu am thanh
    t = np.arange(0, dur, 0.02)  # chia khoang bien do 20ms
    ZCR = np.zeros(len(t), dtype=np.float64)  # khoi tao mang ZCR
    n1 = 0
    # xac dinh tuong doi 1 khoang chia gap bao nhieu thoi gian lay mau ( = 0.02/T)
    x = int(0.02*Fs)
    for n in range(len(ZCR)):
        while ((n*x + n1) < len(data)-1):
            if (dau(data[n*x + n1]) != dau(data[n*x + n1 + 1])):
                ZCR[n] += 1
            n1 += 1
            if (n1 == x):
                n1 = 0
                break
    return ZCR

def CalculateMA(Fs, data):  # khoang chia 20ms
    dur = len(data) / Fs  # thoi gian tin hieu am thanh
    t = np.arange(0, dur, 0.02)  # chia khoang bien do 20ms
    E = np.zeros(len(t))  # khoi tao mang E
    n1 = 0
    # xac dinh tuong doi 1 khoang chia gap bao nhieu thoi gian lay mau ( = 0.02/T)
    x = int(0.02*Fs)
    for n in range(len(E)):
        while ((n*x + n1) < len(data)):
            E[n] += abs(data[n*x + n1])
            n1 += 1
            if (n1 == x):
                n1 = 0
                break
    return E



# def GetEdge(E):         # Get the edge
#     voiced = np.zeros(len(E), dtype=np.float64)
#     unvoiced = np.zeros(len(E), dtype=np.float64)
#     res = []
#     for i in range(0, len(E)-1):
#         if(E[i] > 0.0):
#             voiced[i] = 1
#         else:
#             unvoiced[i] = 1

#     for i in range(1, len(E)-1):
#         if voiced[i] == unvoiced[i-1]:
#             res.append(i-1)
#     return res

def GetEdgeZCR(E):         # Get the edge
    res = []
    for i in range(0, len(E)-1):
        if(E[i+1] > 0.0 and E[i] == 0.0):
            res.append(i)
        elif(E[i-1] > 0.0 and E[i] == 0.0):
            res.append(i)

    u = 0
    while(u < len(res)):
        temp = res[u]
        for k in range(1,13):
            if temp + k in res:
                res.remove(temp + k)
        u += 1
    return res

def GetEdgeMA(E):         # Get the edge
    res = []
    for i in range(0, len(E)-1):
       if(E[i+1] > 0.015 and E[i] < 0.015):
            res.append(i)
       elif(E[i-1] > 0.015 and E[i] < 0.015):
            res.append(i)

    u = 0
    while(u < len(res)):
        temp = res[u]
        for k in range(1,10):
            if temp + k in res:
                res.remove(temp + k)
        u += 1
    return res

# # --------------------------------------------------MAIN------------------------------------------------------
Fs, data = read('./Resources/TinHieuMau/studio_male.wav')


avg = 0
for i in range(len(data)):
    avg += abs(data[i]/len(data))

altdata = np.zeros(len(data))
for i in range(len(data)):
    altdata[i] = data[i] - avg


# E = chiakhung(Fs, data)

# ------Normalize E---------


# E = Normalized1(E, min(E), max(E))

 # khoi tao mang E
# x = np.zeros(len(E), dtype=np.float64)


# def calZCRperFrame(data,size):
#     if size == 0:
#         return 0
#     else:
#      count = 0
#      for i in range(0,size):
#         if(data[i-1]*data[i] < 0):
#             count += 1
#      return count


# def calZCRallFrames(data):
#     zcr = []
#     temp = int(0.02*Fs)
#     alt = 0
#     while(temp <= len(data)):
#         zcr.append(calZCRperFrame(data,temp)-calZCRperFrame(data,alt))
#         alt = temp
#         temp = temp + int(0.02*Fs)
#     return zcr

def dau(x):
    if (x> 0):
        return 1
    if (x< 0):  
        return -1


zcr = ZCRframe(Fs,altdata)
minzcr = min(zcr)
maxzcr = max(zcr)
zcr = Normalized1(zcr, minzcr, maxzcr)


realEdges = []


MA = CalculateMA(Fs,data)
MA = Normalized1(MA,min(MA),max(MA))


# Tim cac bien do bo vao mang realEdge
for i in range(0, len(GetEdgeZCR(zcr))):
    realEdges.append(GetEdgeZCR(zcr)[i]*int(0.02*Fs))
# -------------------------------------
print(GetEdgeZCR(zcr))

plt.figure()


plt.subplot(2, 1, 1)
plt.plot(zcr, color="r")
plt.vlines(GetEdgeZCR(zcr), 0, 1)

arrayX = []

for i in range(0, len(data)):
    arrayX.append(i)

plt.subplot(2, 1, 2)
plt.plot(arrayX, data, color="r")
plt.vlines(realEdges, -max(data), max(data))


plt.xlabel('sample index')
plt.ylabel('amplitude')
plt.title('waveform of test audio')
plt.show()