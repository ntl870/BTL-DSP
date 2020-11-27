# # ---------------------------------------BAI TAP NHOM --------------------------------------------------


# # -------------------------------------LIBRARY-----------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write


# # ----------------------------------------------FUNCTION-------------------------------------------
def Normalize(data, min, max):  # Chuẩn hóa data về 0,1
    res = []    # Tạo LIST res rỗng để chứa kết quả
    for i in range(0, len(data)):   # Cho i chạy hết qua data
        res.append((data[i]-min)/(max-min))  # Đẩy kết quả vào LIST res
    return res  # Trả về LIST res cho hàm


def CalculateSTE(Fs, data):
    dur = len(data) / Fs  # Độ dài của tín hiệu âm thanh
    t = np.arange(0, dur, 0.02)  # Chia khoảng 0.02s bằng hàm arange của numpy
    # Tạo mảng E toàn 0 với độ dài của t với hàm zeros của numpy với kiểu dữ liệu là float64
    E = np.zeros(len(t), dtype=np.float64)
    n1 = 0  # Biến n1 phụ để chạy qua mỗi khung
    # Xác định tương đối 1 khoảng chia gặp bao nhiêu thơi gian lấy mẫu ( = 0.02/T)
    x = int(0.02*Fs)  # x là độ dài 1 khung
    for n in range(len(E)):  # Cho biến n chạy hết qua E
        while ((n*x + n1) < len(data)):  # Đảm bảo vẫn ở trong khoảng của data
            E[n] += data[n*x + n1]**2   # Công thức của năng lượng ngắn hạn
            n1 += 1  # Tăng biến n1 lên 1 đơn vị
            if (n1 == x):   # Nếu n1 bằng x thì đang duyệt đến vị trí cuối khung
                n1 = 0  # Đưa n1 = 0 để đến khung tiếp theo
                break   # break để dừng
    return E    # Trả lại E cho hàm


def CalculateZCR(Fs, data):
    dur = len(data) / Fs   # Độ dài của tín hiệu âm thanh
    t = np.arange(0, dur, 0.02)  # Chia khoảng 0.02s bằng hàm arange của numpy
    # Tạo mảng ZCR toàn 0 với độ dài của t với hàm zeros của numpy với kiểu dữ liệu là float64
    ZCR = np.zeros(len(t), dtype=np.float64)
    n1 = 0
    # Xác định tương đối 1 khoảng chia gặp bao nhiêu thơi gian lấy mẫu ( = 0.02/T)
    x = int(0.02*Fs)  # x là độ dài 1 khung
    for n in range(len(ZCR)):  # Cho biến n chạy hết qua E
        while ((n*x + n1) < len(data)-1):  # Đảm bảo vẫn ở trong khoảng của data
            # Công thức tính của ZCR với hàm lấy dấu
            if (data[n*x + n1] * data[n*x + n1 + 1] > 0):
                ZCR[n] += 1  # Tăng lên 1 đơn vị của khung n
            n1 += 1  # Tăng biến n1 lên 1 đơn vị
            if (n1 == x):  # Nếu n1 bằng x thì đang duyệt đến vị trí cuối khung
                n1 = 0  # Đưa n1 = 0 để đến khung tiếp theo
                break  # break để dừng
    return ZCR  # Trả lại ZCR cho hàm


def CalculateMA(Fs, data):
    dur = len(data) / Fs  # Độ dài của tín hiệu âm thanh
    t = np.arange(0, dur, 0.02)  # Chia khoảng 0.02s bằng hàm arange của numpy
    # Tạo mảng MA toàn 0 với độ dài của t với hàm zeros của numpy với kiểu dữ liệu là float64
    MA = np.zeros(len(t))
    n1 = 0
    # Xác định tương đối 1 khoảng chia gặp bao nhiêu thơi gian lấy mẫu ( = 0.02/T)
    x = int(0.02*Fs)  # x là độ dài 1 khung
    for n in range(len(MA)):  # Cho biến n chạy hết qua E
        while ((n*x + n1) < len(data)):  # Đảm bảo vẫn ở trong khoảng của data
            MA[n] += abs(data[n*x + n1])     # Công thức tính của MA
            n1 += 1  # Tăng biến n1 lên 1 đơn vị
            if (n1 == x):  # Nếu n1 bằng x thì đang duyệt đến vị trí cuối khung
                n1 = 0  # Đưa n1 = 0 để đến khung tiếp theo
                break  # break để dừng
    return MA  # Trả lại MA cho hàm


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