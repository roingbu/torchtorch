# -*- coding: utf-8 -*-
# @Time    : 2021/8/11 上午9:24
# @Author  : KevinW
# @File    : split_data.py
# @Software: PyCharm

#对 head 文件夹进行拆分,分为 train.txt 和 val.txt
import os
import random

images_path = "data/vocbu-11-29/JPEGImages"  # TODO:
xmls_path = "data/vocbu-11-29/Annotations"  # TODO:
train_val_txt_path = "data/vocbu-11-29/ImageSets/Main/"  # TODO:
val_percent = 0.25  # TODO:

if not os.path.exists(train_val_txt_path):
    os.makedirs(train_val_txt_path)
images_list = os.listdir(images_path)
random.shuffle(images_list)

#划分训练集和验证的数量
train_images_count = int((1-val_percent)*len(images_list))
val_images_count = int(val_percent*len(images_list))
#
#生成训练集的 train.txt 文件
train_txt = open(os.path.join(train_val_txt_path, "train.txt"), "w")
train_count = 0
for i in range(train_images_count):
    text = images_list[i].split(".jpg")[0] + "\n"
    train_txt.write(text)
    train_count += 1
print("train_count: " + str(train_count))
train_txt.close()

#生成验证集的 val.txt 文件
val_txt = open(os.path.join(train_val_txt_path, "val.txt"), "w")
val_count = 0
for i in range(val_images_count):
    text = images_list[train_images_count + i].split(".jpg")[0] + "\n"
    val_txt.write(text)
    val_count+=1
print("val_count: " + str(val_count))
val_txt.close()


