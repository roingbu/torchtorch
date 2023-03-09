# -*- coding: utf-8 -*-
# @Time    : 2021/8/27 上午11:45
# @Author  : kevinW
# @File    : img_aug.py
# @Software: PyCharm

import imgaug.augmenters as iaa
import cv2
import numpy as np
import random
import glob
import os
from imgaug.augmentables.batches import UnnormalizedBatch
import time
import shutil
import xml.etree.ElementTree as ET
import math

def read_more(filenames):
    temp = []
    for filename in filenames:
        img = cv2.imdecode(np.fromfile(filename, dtype=np.uint8), 1)
        h, w, _ = img.shape
        if h < 32 or w < 32:
            ratio = math.ceil(max(32/h, 32/w))
            img = cv2.resize(img, dsize=(w*ratio, h*ratio))
        new_h, new_w, _ = img.shape
        assert new_h >= 32 and new_w >= 32
        temp.append(img)
    return temp

def list_of_groups(init_list, childern_list_len):
    '''
    init_list为初始化的列表，childern_list_len初始化列表中的几个数据组成一个小列表
    :param init_list:
    :param childern_list_len:
    :return:
    '''
    list_of_group = zip(*(iter(init_list),) *childern_list_len)
    end_list = [list(i) for i in list_of_group]
    count = len(init_list) % childern_list_len
    end_list.append(init_list[-count:]) if count !=0 else end_list
    return end_list

# 确定一些图像增强随机参数
rotate = np.random.randint(0, 360)
scale_aff = round(random.uniform(0.8, 1.2), 2)
severity = np.random.randint(1, 4)
scale_dist = round(random.uniform(0.01, 0.025), 2)
over_num = round(random.uniform(1, 2.6), 1)
color_num = np.random.randint(30, 70)
blur_num = np.random.randint(2, 5)
percent_trim = round(random.uniform(0.05, 0.11), 2)
scale_pers = round(random.uniform(0.04, 0.06), 3)

aug_light = iaa.SomeOf(np.random.randint(1, 2), [
        iaa.imgcorruptlike.MotionBlur(severity=severity),
        iaa.MultiplyElementwise(over_num),
        iaa.imgcorruptlike.Fog(severity=severity),

        #iaa.WithBrightnessChannels(iaa.Add(color_num)),
        iaa.imgcorruptlike.Contrast(severity=severity),

        iaa.imgcorruptlike.Spatter(severity=severity),
        #iaa.imgcorruptlike.Snow(severity=severity),

        iaa.imgcorruptlike.Frost(severity=severity),

        iaa.imgcorruptlike.GaussianNoise(severity=severity),
    ])


if __name__ == "__main__":
    img_files = glob.glob(os.path.join("/home/data/168", "*.jpg"))
    img_save = "/home/data/helmet/JPEGImages"
    anno_save = "/home/data/helmet/Annotations"
    if not os.path.exists(img_save):
        os.makedirs(img_save)
    if not os.path.exists(anno_save):
        os.makedirs(anno_save)
    cnt = 0

    batch_num = 20
    spilt_files = list_of_groups(img_files, batch_num)
    random.shuffle(spilt_files)

    for epoch in range(1):
        for index,childfiles in enumerate(spilt_files):
            #print(childfiles)
            images = read_more(childfiles)
            time_start = time.time()
            batches = [UnnormalizedBatch(images=images) for _ in range(batch_num)]  # 数据批次化
            batches_aug = list(aug_light.augment_batches(batches, background=True))
            time_end = time.time()
            cnt += 1
            print("IDX: %d Augmentation done in %.2fs" % (cnt, time_end - time_start,))
            #auged_images = batches_aug[0]
            for num in range(batch_num):
                try:
                    filename = os.path.basename(childfiles[num]).split('.')[0]
                    new_name = filename + "#aug_6#" + str(epoch) + "#" + str(index) + str(num)
                    cv2.imencode(".jpg", batches_aug[0].images_aug[num])[1].tofile(
                        os.path.join(img_save, new_name + ".jpg"))
                    shutil.copy(childfiles[num].replace(".jpg", ".xml"),
                                os.path.join(anno_save, new_name + ".xml"))

                except:
                    # 防止图片总数不为batch_num的倍数
                    pass



