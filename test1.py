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

def dau(x):
    if (x > 0):
        return 1
    if (x < 0):
        return -1


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
            if (data[n*x + n1] * data[n*x + n1 + 1] < 0):
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

def GetEdges(E):         # Get the edge
    res = []
    for i in range(0, len(E)-1):
        if(E[i+1] > 0.0 and E[i] == 0.0):
            res.append(i)
        elif(E[i-1] > 0.0 and E[i] == 0.0):
            res.append(i)

    u = 0
    while(u < len(res)):
        temp = res[u]
        for k in range(1, 13):
            if temp + k in res:
                res.remove(temp + k)
        u += 1

    temp = []
    for i in range(0, len(res)):
        for k in range(1, 10):
            if E[res[i] + k] != 0 and E[res[i] - k] != 0:
                temp.append(res[i])

    temp = list(dict.fromkeys(temp))

    for i in range(0, len(temp)):
        res.remove(temp[i])

    return res


# def GetEdgeMA(E):         # Get the edge
#     res = []
#     zcr = ZCRframe(Fs, data)
#     for i in range(0, len(E)-1):
#         if(E[i+1] > 0.15 and E[i] < 0.15):
#             res.append(i)
#         elif(E[i-1] > 0.15 and E[i] < 0.15):
#             res.append(i)

#     u = 0
#     while(u < len(res)):
#         temp = res[u]
#         for k in range(1, 8):
#             if temp + k in res:
#                 res.remove(temp + k)
#         u += 1

#     temp = []
#     for i in range(0, len(res)):
#             if E[res[i] + 6] < 0.15 and E[res[i] - 6] > 0.15:
#                 temp.append(res[i])
#             elif E[res[i] + 6] > 0.15 and E[res[i] - 6] < 0.15:
#                 temp.append(res[i])

#     temp = list(dict.fromkeys(temp))



#     return temp


# # --------------------------------------------------MAIN------------------------------------------------------
Fs, data = read('./Resources/TinHieuMau/LA025.wav')


avg = 0
for i in range(len(data)):
    avg += abs(data[i]/len(data))

altdata = np.zeros(len(data))
for i in range(len(data)):
    altdata[i] = data[i] - avg


E = chiakhung(Fs, data)
E = Normalized1(E, min(E), max(E))
altE = np.zeros(len(E))
for i in range(0,len(E)):
    if E[i] <= 0.01:
        altE[i] = 0
    else:
        altE[i] = E[i]



zcr = ZCRframe(Fs,altdata)
zcr = Normalized1(zcr, min(zcr), max(zcr))





MA = CalculateMA(Fs, data)
MA = Normalized1(MA, min(MA), max(MA))
altMA = np.zeros(len(MA))
for i in range(0,len(MA)):
    if MA[i] <= 0.1:
        altMA[i] = 0
    else:
        altMA[i] = MA[i]

realEdgesE = []
realEdgesZCR = []
realEdgesMA = []

for i in range(0, len(GetEdges(altE))):
    realEdgesE.append(GetEdges(altE)[i]*int(0.02*Fs))

for i in range(0, len(GetEdges(altMA))):
    realEdgesZCR.append(GetEdges(altMA)[i]*int(0.02*Fs))

for i in range(0, len(GetEdges(zcr))):
    realEdgesMA.append(GetEdges(zcr)[i]*int(0.02*Fs))



plt.figure()


plt.subplot(2, 3, 1)
plt.plot(MA, color="r")
plt.vlines(GetEdges(altMA), 0, 1)
plt.subplot(2, 3, 4)
plt.plot(data, color="r")
plt.vlines(realEdgesMA, -max(data), max(data))

plt.subplot(2, 3, 2)
plt.plot(E, color="r")
plt.vlines(GetEdges(altE), 0, 1)
plt.subplot(2, 3, 5)
plt.plot(data, color="r")
plt.vlines(realEdgesE, -max(data), max(data))

plt.subplot(2, 3, 3)
plt.plot(zcr, color="r")
plt.vlines(GetEdges(zcr), 0, 1)
plt.subplot(2, 3, 6)
plt.plot(data, color="r")
plt.vlines(realEdgesZCR, -max(data), max(data))


plt.show()
