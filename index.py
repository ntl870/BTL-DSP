#---------------------------------------BAI TAP NHOM --------------------------------------------------

#-------------------------------------LIBRARY-----------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read,write

#----------------------------------------------FUNCTION-------------------------------------------
#chuyen audio sang tan so lay mau Fs2
def chiakhung(Fs,data): #khoang chia 20ms
    dur = len(data) / Fs  # thoi gian tin hieu am thanh
    t = np.arange(0, dur, 0.02) #chia khoang bien do 20ms
    E = np.zeros(len(t), dtype= np.int64) #khoi tao mang E
    n1 = 0
    x = int(0.02*Fs) # xac dinh tuong doi 1 khoang chia gap bao nhieu thoi gian lay mau ( = 0.02/T)
    for n in range(len(E)):
        while ((n*x + n1)< len(data)):
            E[n] += (data[n*x + n1]*data[n*x + n1])
            n1+=1
            if (n1 ==x) :
                n1 =0
                break
    return E


#--------------------------------------------------MAIN------------------------------------------------------
Fs,data = read('Resources/lab_female.wav')
print(len(data))
E = chiakhung(Fs,data)

plt.figure()
plt.plot(E)
plt.xlabel('sample index')
plt.ylabel('amplitude')
plt.title('waveform of test audio')
plt.show()