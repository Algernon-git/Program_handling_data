import os
import re
from deal import Load
import func as ff
import time

pp = Load("data","image")                  # 指定数据所在文件夹名字"data",并指定将来生成图片所在文件夹名称"image"（自己填写)
pre_data = pp.read()
label_name = pp.get_name()
img_path = pp.path_img
fil_data = ff.deal_data(pre_data)
ff.draw_pict(fil_data,label_name,img_path)
