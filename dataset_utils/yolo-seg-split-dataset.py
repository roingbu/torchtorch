import os
import glob
import shutil
import random

from pathlib import Path


def split_dataset():
    # 为防止数据混乱，执行此脚本前，先将'C:\Users\jianming_ge\Desktop\code\handle_dataset\water_street\yolov_format'清空
    """
    :return:
    """
    txt_path = "./new_dir"  # TODO 图片标签位置，图片标签放在一个文件夹中，文件名一致
    yolo_path = "coco-seg-cus"  # TODO 目标位置
    
    yolo_path = Path(yolo_path)
    txt_files = glob.glob(txt_path + "/*.txt")
    
    # 基础图片文件夹
    images_base_dir = Path("./%s/images"%yolo_path)
    # 基础标注文件夹
    labels_base_dir = Path("./%s/labels"%yolo_path)
    # mkdir
    if yolo_path.exists():
        shutil.rmtree(yolo_path)  # delete dir
    images_base_dir.mkdir(parents=True, exist_ok=True)
    labels_base_dir.mkdir(parents=True, exist_ok=True)    

    # 训练集图片文件夹
    images_train_dir = os.path.join(images_base_dir, "train")
    # 训练集标注文件夹
    labels_train_dir = os.path.join(labels_base_dir, "train")
    # 验证集图片文件夹
    images_val_dir = os.path.join(images_base_dir, "val")
    # 验证集标注文件夹
    labels_val_dir = os.path.join(labels_base_dir, "val")
    # 生成所需4个文件夹
    [Path(dir_path).mkdir(parents=True, exist_ok=True) for dir_path in [images_train_dir, labels_train_dir, images_val_dir, labels_val_dir]]
    # 验证集数据的比例,可以自定义成任何你所需要的比例
    val_rate = 0.6
    # print(txt_files)
    for txt_ori_path in txt_files:
        fpath, fname = os.path.split(txt_ori_path)  # 分离文件名和路径
        if random.randint(1, 10) == 10 * val_rate:
            # 验证集数据
            txt_dst_path = os.path.join(labels_val_dir, fname)
            img_dst_path = os.path.join(images_val_dir, fname.replace(".txt", ".jpg"))
        else:
            # 训练集
            txt_dst_path = os.path.join(labels_train_dir, fname)
            img_dst_path = os.path.join(images_train_dir, fname.replace(".txt", ".jpg"))
        # 执行复制
        # 图片都是jpg,且和原始txt文件在同一个目录，所以可以这么写
        img_ori_path = txt_ori_path.replace(".txt", ".jpg")
        
        print(txt_dst_path)
        
        # 移动标注文件
        shutil.copy(txt_ori_path, txt_dst_path)
        # 移动图片文件
        shutil.copy(img_ori_path, img_dst_path)
        

if __name__ == '__main__':
    split_dataset()
