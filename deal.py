import numpy as np
import os
import re

class Load():
    def __init__(self,file_name,img_name):
        self.path = os.path.dirname(__file__)                                           # 获取当前文件工作目录
        self.path_data = os.path.join(self.path,str(file_name))                         # 获取数据所在目录
        if not os.path.exists(str(img_name)):                                           # 判断用于存储图片的文件夹是否存在，若没有则新建一个
            os.mkdir(str(img_name))
        self.path_img = os.path.join(self.path,str(img_name))
        self.files = os.listdir(self.path_data)                                             # 获取路径下的所有文件
        self.file_name = []
        self.data = []

    def read(self):
        for file in self.files:                                 
            if not os.path.isdir(file):                                           # 判断是否为文件夹，非文件夹才读取
                if os.path.splitext(file)[1] == '.TXT' or os.path.splitext(file)[1] == '.txt':                           #判断是否为所要求的‘.txt’后缀名文件
                    self.file_name.append(os.path.splitext(file)[0])                   # 将不带后缀名的文件名载入列表
                    file = os.path.join(self.path_data,file)                           # 获取文件夹下每个txt文件的路径
                    f = open(file)                                                # 打开txt文件
                    data_inner = {'force':[],'distance':[]}                       # 在data列表中创建字典，存储数据
                    self.data.append(data_inner)
                    try:
                        for line in f.readlines()[90:]:                               # 读取每个txt文件中的89行后的第二第三列数据
                            temp = re.sub(r"\s+","",line)                             # 将每行中所有多余空格去掉
                            temp = temp.split(',')                                    # 以逗号为分隔符将逗号数据存储成一个列表
                            data_inner.setdefault("force",[]).append(float(temp[1]))
                            data_inner.setdefault("distance",[]).append(float(temp[2]))
                    except IndexError:
                        file = os.path.join(self.path_data,file)                           # 获取文件夹下每个txt文件的路径
                        f = open(file)
                        del self.data[-1]
                        data_inner = {'force':[],'distance':[]}                       # 在data列表中创建字典，存储数据
                        self.data.append(data_inner)
                        try:
                            for line in f.readlines()[150:]:                               # 读取每个txt文件中的89行后的第二第三列数据
                                temp = re.sub(r"\s+","",line)                             # 将每行中所有多余空格去掉
                                temp = temp.split(',')                                    # 以逗号为分隔符将逗号数据存储成一个列表
                                data_inner.setdefault("force",[]).append(float(temp[1]))
                                data_inner.setdefault("distance",[]).append(float(temp[2]))
                        except IndexError:
                            file = os.path.join(self.path_data,file)                           # 获取文件夹下每个txt文件的路径
                            f = open(file)
                            del self.data[-1]
                            data_inner = {'force':[],'distance':[]}                       # 在data列表中创建字典，存储数据
                            self.data.append(data_inner)
                            for line in f.readlines()[190:]:                               # 读取每个txt文件中的89行后的第二第三列数据
                                temp = re.sub(r"\s+","",line)                             # 将每行中所有多余空格去掉
                                temp = temp.split(',')                                    # 以逗号为分隔符将逗号数据存储成一个列表
                                data_inner.setdefault("force",[]).append(float(temp[1]))
                                data_inner.setdefault("distance",[]).append(float(temp[2]))
        step = 3
        data_img =[self.data[i:i+step] for i in range(0,len(self.data),step)]               #每个试件分为三组，这三组试件的数据要求画在同一个组内
        self.lab_name = [self.file_name[i:i+step] for i in range(0,len(self.file_name),step)]
        return data_img

    def get_name(self):
        return self.lab_name



class KK():
    def __init__(self,value1,value2):    #初始定义及转化
        self.aa = value1
        self.bb = value2
        for i in range(len(self.aa)):
            C = [1]
            C.insert(0,self.aa[i])
            self.aa[i] = C
        self.A = np.array(self.aa)
        self.B = np.array(self.bb)


    def k(self):    #求斜率k和b
        try:
            x = np.matmul(np.matmul(np.linalg.inv(np.matmul(self.A.T,self.A)),self.A.T),self.B)
            return x
        except:
            return [1,1]

    def ask_xx(self):
        self.xx = []
        for i in range(len(self.aa)):
            del self.aa[i][1]
            self.xx.append(self.aa[i][0])
        return self.xx


    def x0(self):    #求截距
        c = -self.k()[1]/(self.k()[0])
        return c

    def new_value(self,aa,bb):
        aa.insert(0,self.x0())
        aa = [i-self.x0() for i in aa]
        bb.insert(0,0)
        return aa,bb





class Del():
    def __init__(self,con,vau1,vau2):
        self.const = con
        self.xx = vau1
        self.yy = vau2
        self.sum = self.xx[-1] - self.xx[0]
        self.ax = []
        self.bx = []
        self.cx = []
        self.dx = []
        self.ay = []
        self.by = []
        self.cy = []
        self.dy = []
        self.ex = []
        self.ey = []
        for i in self.xx:
            if self.yy[self.xx.index(i)] >= 0.1:
                if i>=self.xx[0] and i<(0.2*self.sum + self.xx[0]):
                    self.ax.append(i)
                    self.ay.append(self.yy[self.xx.index(i)])
                elif i>=(0.2*self.sum + self.xx[0]) and i<(0.4*self.sum + self.xx[0]):
                    self.bx.append(i)
                    self.by.append(self.yy[self.xx.index(i)])
                elif i>=(0.4*self.sum + self.xx[0]) and i<(0.6*self.sum + self.xx[0]):
                    self.cx.append(i)
                    self.cy.append(self.yy[self.xx.index(i)])
                elif i>=(0.6*self.sum + self.xx[0]) and i<(0.8*self.sum + self.xx[0]):
                    self.dx.append(i)
                    self.dy.append(self.yy[self.xx.index(i)])
                else:
                    self.ex.append(i)
                    self.ey.append(self.yy[self.xx.index(i)])

    def new(self):
        self.vv =[]
        self.new_x = []
        self.new_y = []
        kb = KK(self.bx,self.by)
        self.bx = kb.ask_xx()
        kc = KK(self.cx,self.cy)
        self.cx = kc.ask_xx()
        kd = KK(self.dx,self.dy)
        self.dx = kd.ask_xx()
        self.new_x = []
        self.new_y = []
        if kb.k()[0]> (-1*self.const):
            self.new_x = self.ax + self.bx
            self.new_y = self.ay + self.by
            if kc.k()[0]> (-1*self.const):
                self.new_x = self.new_x + self.cx
                self.new_y = self.new_y +self.cy
                if kd.k()[0]> (-1*self.const):
                    self.new_x = self.new_x + self.dx
                    self.new_y = self.new_y +self.dy                
        else:
            self.new_x = self.ax
            self.new_y = self.ay
        return self.new_x,self.new_y

 








