import matplotlib.pyplot as plt
import os
import re
from matplotlib.font_manager import FontProperties
from deal import *

def deal_data(init_data):
    data_img = init_data
    for j in range(len(data_img)):                                               # 将以上数据处理后画图
        #plt.title("Distance-force Curve",fontsize = 20)
        a_x = data_img[j][0]['force']                                            # 去除分组后的数据其中一组进行处理
        b_x = data_img[j][1]['force']
        c_x = data_img[j][2]['force']
        a_y = data_img[j][0]['distance']
        b_y = data_img[j][1]['distance']
        c_y = data_img[j][2]['distance']
        aa_y = a_y[int(a_y.index(max(a_y))*0.05):int(a_y.index(max(a_y))*0.1)]   # 对数据值达到峰值前的数据进行提取
        bb_y = b_y[int(b_y.index(max(b_y))*0.05):int(b_y.index(max(b_y))*0.1)]
        cc_y = c_y[int(c_y.index(max(c_y))*0.05):int(c_y.index(max(c_y))*0.1)]
        aa_x = a_x[int(a_y.index(max(a_y))*0.05):int(a_y.index(max(a_y))*0.1)]
        bb_x = b_x[int(b_y.index(max(b_y))*0.05):int(b_y.index(max(b_y))*0.1)]
        cc_x = c_x[int(c_y.index(max(c_y))*0.05):int(c_y.index(max(c_y))*0.1)]

        ka = KK(aa_x,aa_y)                                                       # 对每组中的一条使用KK类方法
        a1 = ka.k()[0]                                                           # 求该条数据的斜率
        ka_x = ka.new_value(a_x[int(a_y.index(max(a_y))*0.05):], a_y[int(a_y.index(max(a_y))*0.05):])[0]    # 调用类中的方法进行处理并求生成新的数据条
        ka_y = ka.new_value(a_x[int(a_y.index(max(a_y))*0.05):], a_y[int(a_y.index(max(a_y))*0.05):])[1]
        if a_y.index(max(a_y)) >= 0.9*len(a_y):
            data_img[j][0]['force'] = ka_x[:ka_y.index(max(ka_y))]
            data_img[j][0]['distance'] = ka_y[:ka_y.index(max(ka_y))]
        else:
            final_aa = Del(a1,ka_x[ka_y.index(max(ka_y)):],ka_y[ka_y.index(max(ka_y)):])   # 对每条数据的峰值后面数据应用Del类进行筛选
            lat_aax = final_aa.new()[0]                                                    # 筛选得到每条数据后的值
            lat_aay = final_aa.new()[1]
            data_img[j][0]['force'] = ka_x[:ka_y.index(max(ka_y))] + lat_aax                                 # 合并峰值前的数据和峰值后的数据生成新的数据条
            data_img[j][0]['distance'] = ka_y[:ka_y.index(max(ka_y))] + lat_aay

        kb = KK(bb_x,bb_y)
        b1 = kb.k()[0]                                        
        kb_x = kb.new_value(b_x[int(b_y.index(max(b_y))*0.05):], b_y[int(b_y.index(max(b_y))*0.05):])[0]
        kb_y = kb.new_value(b_x[int(b_y.index(max(b_y))*0.05):], b_y[int(b_y.index(max(b_y))*0.05):])[1]
        if b_y.index(max(b_y)) >= 0.9*len(b_y):
            data_img[j][1]['force'] = kb_x[:kb_y.index(max(kb_y))]
            data_img[j][1]['distance'] = kb_y[:kb_y.index(max(kb_y))]
        else:
            final_bb = Del(b1,kb_x[b_y.index(max(b_y)):],kb_y[b_y.index(max(b_y)):])
            lat_bbx = final_bb.new()[0]
            lat_bby = final_bb.new()[1]
            data_img[j][1]['force'] = kb_x[:kb_y.index(max(kb_y))] + lat_bbx
            data_img[j][1]['distance'] = kb_y[:kb_y.index(max(kb_y))] + lat_bby

        kc = KK(cc_x,cc_y)
        c1 = kc.k()[0]
        kc_x = kc.new_value(c_x[int(c_y.index(max(c_y))*0.05):], c_y[int(c_y.index(max(c_y))*0.05):])[0]
        kc_y = kc.new_value(c_x[int(c_y.index(max(c_y))*0.05):], c_y[int(c_y.index(max(c_y))*0.05):])[1]
        if c_y.index(max(c_y)) >= 0.9*len(c_y):
            data_img[j][2]['force'] = kc_x[:kc_y.index(max(kc_y))]
            data_img[j][2]['distance'] = kc_y[:kc_y.index(max(kc_y))]
        else:
            final_cc = Del(c1,kc_x[c_y.index(max(c_y)):],kc_y[c_y.index(max(c_y)):])
            lat_ccx = final_cc.new()[0]
            lat_ccy = final_cc.new()[1]
            data_img[j][2]['force'] = kc_x[:kc_y.index(max(kc_y))] + lat_ccx
            data_img[j][2]['distance'] = kc_y[:kc_y.index(max(kc_y))] + lat_ccy

    return data_img


def draw_pict(final_data,lab_name,img_way):
    data_img = final_data
    path = img_way
    for j in range(len(data_img)):
        plt.plot(data_img[j][0]['force'],data_img[j][0]['distance'],color='green',label = lab_name[j][0])
        plt.plot(data_img[j][1]['force'],data_img[j][1]['distance'],color='red',label = lab_name[j][1])
        plt.plot(data_img[j][2]['force'],data_img[j][2]['distance'],color='blue',label = lab_name[j][2])
        plt.legend(loc = 'lower right',facecolor = 'none',borderaxespad =0.1, handlelength = 0.8,handleheight =0.8,frameon=False)    #  设置图例样式
        plt.xlabel("Force",fontsize = 16)
        plt.xlim((0,None))
        plt.ylim((0,None))
        plt.ylabel("Displance",fontsize = 16)
        path_img = path + '/' + (str(lab_name[j][0][:-2]) + '.jpg')
        plt.savefig(path_img,dpi =1280 )

        plt.close()


