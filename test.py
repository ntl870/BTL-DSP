# # ---------------------------------------BAI TAP NHOM --------------------------------------------------

# # '/media/ntl2000/Data/Study/XLTH/Python/BTL/Resources/TinHieuMau/lab_female.wav'
# #  'D:\Study\XLTH\Python\BTL\Resources\TinHieuMau\lab_female.wav'

# # -------------------------------------LIBRARY-----------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write



# # ----------------------------------------------FUNCTION-------------------------------------------
# # chuyen audio sang tan so lay mau Fs2



# chuan hoa
def Normalize(energy, min, max):
    res = []
    for i in range(0, len(energy)):
        res.append((energy[i] - min) / (max - min))
    return res


def CalculateSTE(Fs, data):  # khoang chia 20ms
    dur = len(data) / Fs  # thoi gian tin hieu am thanh
    t = np.arange(0, dur, 0.02)  # chia khoang bien do 20ms
    E = np.zeros(len(t))  # khoi tao mang E
    n1 = 0
    # xac dinh tuong doi 1 khoang chia gap bao nhieu thoi gian lay mau ( = 0.02/T)
    x = int(0.02 * Fs)
    for n in range(len(E)):
        while ((n * x + n1) < len(data)):
            E[n] += data[n * x + n1] ** 2
            n1 += 1
            if (n1 == x):
                n1 = 0
                break
    return E


def GetSign(x):
    if (x> 0):
        return 1
    if (x< 0):
        return -1
    if (x== 0):
        return 0

#Hàm tính ZCR
def CalculateZCR(Fs, data):  # khoang chia 20ms
    dur = len(data) / Fs  # thoi gian tin hieu am thanh
    t = np.arange(0, dur, 0.02)  # chia khoang bien do 20ms
    ZCR = np.zeros(len(t), dtype=np.float64)  # khoi tao mang ZCR
    n1 = 0
    # xac dinh tuong doi 1 khoang chia gap bao nhieu thoi gian lay mau ( = 0.02/T)
    x = int(0.02 * Fs)
    for n in range(len(ZCR)):
        while ((n * x + n1) < len(data) - 1):
            if (data[n * x + n1]* data[n * x + n1 + 1] > 0):
                ZCR[n] += 1
            n1 += 1
            if (n1 == x):
                n1 = 0
                break
    return ZCR

# Hàm tính MA
def CalculateMA(Fs, data):  # khoang chia 20ms
    dur = len(data) / Fs  # thoi gian tin hieu am thanh
    t = np.arange(0, dur, 0.02)  # chia khoang bien do 20ms
    E = np.zeros(len(t))  # khoi tao mang E
    n1 = 0
    # xac dinh tuong doi 1 khoang chia gap bao nhieu thoi gian lay mau ( = 0.02/T)
    x = int(0.02 * Fs)
    for n in range(len(E)):
        while ((n * x + n1) < len(data)):
            E[n] += abs(data[n * x + n1])
            n1 += 1
            if (n1 == x):
                n1 = 0
                break
    return E

# Hàm tìm biên của các phương pháp dùng ngưỡng
def GetEdges(data, threshold):  
    altData = np.zeros(len(data))
    for i in range(0, len(data)):
        if data[i] <= threshold:
            altData[i] = 0
        else:
            altData[i] = data[i]

    res = []    # Tạo mảng res
    for i in range(0, len(altData)-1):  # Cho i chạy hết qua data
        if(altData[i+1] > 0.0 and altData[i] == 0.0):  # Lấy biên bên trái
            res.append(i)   # Cho biên vào mảng res
        elif(altData[i-1] > 0.0 and altData[i] == 0.0):  # Lấy biên bên phải
            res.append(i)   # Cho biên vào mảng res

# Tại đây khi đã có các biên ta cần lọc những biên bị sai do sự nhiễu giữa các tiếng nói

# Đây là dãy code để lọc những biên ở quá sát nhau trong khoảng 12 đoạn
    u = 0       # Cho biến phụ u = 0
    while(u < len(res)):    # Điều kiện để u trong khoảng độ dài là len(res)
        temp = res[u]   # Cho biến phụ temp bằng res[u]
        for k in range(1, 13):  # Cho biến k chạy từ 1 đến 12
            if temp + k in res:  # Nếu temp + k có trong res thì xóa temp + k bằng hàm .remove
                res.remove(temp + k)
            if temp - k in res:  # Nếu temp - k có trong res thì xóa temp - k bằng hàm .remove
                res.remove(temp - k)
        u += 1  # Tăng biến u lên 1 đơn vị
# -------------------------------------------------------

# Sau khi đã lọc những khoảng sát nhau thì các tiếng nói vẫn còn dư những biên còn lại chứ kho
# Block code sau sẽ loại những biên đó
    temp1 = []  # Tạo mảng temp1 rỗng để chứa những phần tử cần xóa
    for i in range(0, len(res)):    # Cho biến i duyệt qua res
        for k in range(1, 13):  # Cho biến k
            if(res[i] - k > 1 and res[i] + k < len(altData) - 1):
                if altData[res[i] + k] > 0 and altData[res[i] - k] > 0:
                    temp1.append(res[i])
                    break

    for i in range(0, len(temp1)):
        res.remove(temp1[i])

# -----------------------------------------------------------
    return res

# hàm tìm biên của phương pháp kết hợp STE và ZCR
def GetEdgesE_ZCR(E,ZCR):
    res = []
    check = True
    for i in range(1, len(E) ):
        if (E[i] > zcr[i] and E[i-1] <zcr[i-1]):
            for k in range(1, 10):
                if (E[i + k] < zcr[i+k]):
                    check = False
            if (check):
                res.append(i)
            check = True
        elif (E[i - 1] > zcr[i-1] and E[i] < zcr[i]):
            for k in range(1, 10):
                if (E[i + k] > zcr[i+k]):
                    check = False
            if (check):
                res.append(i)
            check = True
    u = 0
    while (u < len(res)):
        temp = res[u]
        for k in range(1, 13):
            if temp + k in res:
                res.remove(temp + k)
        u += 1
    
    temp = []
    for i in range(0, len(res)):
        for k in range(1, 13):
            if (res[i] - k > 1 and res[i] + k < len(E) - 1):
                if E[res[i] + k] > 0 and E[res[i] - k] > 0:
                    temp.append(res[i])
    
    temp = list(dict.fromkeys(temp))
    
    for i in range(0, len(temp)):
        res.remove(temp[i])
    return res

#hàm tìm biên thực trên data
def GetRealEdges(edges,Fs):
    res = []
    for i in range(len(edges)):
        res.append(edges[i]*int(0.02*Fs))
    return res

# # --------------------------------------------------MAIN------------------------------------------------------
# đọc file bằng hàm read của scipy
Fs, data = read('./Resources/TinHieuMau/lab_female.wav')
# tính năng lượng ngắn hạn STE
E = CalculateSTE(Fs, data)
#chuẩn hóa STE 
E = Normalize(E, min(E), max(E))
# tìm ZCR
zcr = CalculateZCR(Fs, data)
#chuẩn hóa ZCR
zcr = Normalize(zcr, min(zcr), max(zcr))
#tìm MA
MA = CalculateMA(Fs, data)
#chuẩn hóa MA
MA = Normalize(MA, min(MA), max(MA))

# tìm biên của phương pháp dùng STE và ngưỡng
EdgesE = GetEdges(E,0.02)
# tìm biên của phương pháp dùng MA và ngưỡng
EdgesMA = GetEdges(MA,0.1)
# tìm biên của phương pháp dùng STE và ZCR
EdgesE_ZCR = GetEdgesE_ZCR(E,zcr)


# Hiển thị đồ thị
plt.figure()

# Đồ thị hiển thị kết quả dùng phương pháp MA và ngưỡng
plt.subplot(2, 3, 1)
plt.plot(MA, color="r")
plt.title("MA")
plt.vlines(EdgesMA, 0, 1)
plt.subplot(2, 3, 4)
plt.title("Data MA")
plt.plot(data, color="r")
plt.vlines(GetRealEdges(EdgesMA,Fs), -max(data), max(data))

# Đồ thị hiển thị kết quả dùng phương pháp STE và ngưỡng
plt.subplot(2, 3, 2)
plt.plot(E, color="r")
plt.title("E")
plt.vlines(EdgesE, 0, 1)
plt.subplot(2, 3, 5)
plt.title("Data STE")
plt.plot(data, color="r")
plt.vlines(GetRealEdges(EdgesE,Fs), -max(data), max(data))

# Đồ thị hiển thị kết quả dùng phương pháp kết hợp STE và ZCR
plt.subplot(2,3,3)
plt.plot(zcr, color="r")
plt.plot(E,color= "g")
plt.title("ZCR")
plt.vlines(EdgesE_ZCR, 0, 1)
plt.subplot(2, 3, 6)
plt.title("Data ZCR")
plt.plot(data, color="r")
plt.vlines(GetRealEdges(EdgesE_ZCR,Fs), -max(data), max(data))

plt.show()