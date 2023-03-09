import copy
from lxml.etree import Element, SubElement, tostring, ElementTree

import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import shutil

classes = ["shapan"]  # 类别 # TODO:
# classes = ["person", "car", "gray", "shapan"]  # 类别 # TODO:


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(input_path, image_id, save_path):
    in_file = open('%s/Annotations/%s.xml' % (input_path, image_id))

    label_path = os.path.join(save_path, "labels")
    image_path = os.path.join(save_path, "images")
    if not os.path.exists(save_path):
        os.makedirs(label_path)
        os.makedirs(image_path)
    out_file = open('%s/%s.txt' % (label_path, image_id), 'w')  # 生成txt格式文件
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        if bb[0] >=1 or bb[1] >= 1 or bb[2] >= 1 or bb[3] >= 1 :
            print("error error", image_id)
            break
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    shutil.copy('%s/JPEGImages/%s.jpg' % (input_path, image_id), image_path)

if __name__ == "__main__":
    voc_path = "data/vocbu-11-29"  # TODO:
    for oneset in ["train", "val"]:
        image_ids_train = open('%s/ImageSets/Main/%s.txt' % (voc_path, oneset)).read().strip().split()  # list格式只有000000 000001
        list_file_train = open('%s.txt' % (oneset), 'w')
        save_path = "data/vocbu-11-29/yolo/%s" % (oneset)  # TODO:
        for image_id in image_ids_train:
            list_file_train.write('%s/JPEGImages/%s.jpg\n' % (voc_path, image_id))
            convert_annotation(voc_path, image_id, save_path)
        print("%s dataset generated" % (oneset))
